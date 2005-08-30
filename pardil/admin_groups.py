#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config
import re

p = pardil_page()

p.name = 'pardil_admin_groups'
p.title = site_config['title']

# OLMAZSA OLMAZ!
if 'sid' not in p['session']:
  p.http.redirect('error.py?tag=login_required')
if not p.access('administrate'):
  p.http.redirect('error.py?tag=not_in_authorized_group')
# OLMAZSA OLMAZ!

def index():
  p['groups'] = []
  q = """SELECT gid, label
         FROM groups
         ORDER BY gid ASC
      """
  list = p.db.query(q)
  for i in list:
    l = {
         'gid': i[0],
         'label': i[1]
         }
    p['groups'].append(l)

  p.template = 'admin/groups.tpl'

def delete():
  try:
    p['gid'] = int(p.form['gid'])
  except:
    p.template = 'admin/groups.error.tpl'
    return

  q = """SELECT label
         FROM groups
         WHERE gid=%d
      """ % (p['gid'])
  p['label'] = p.db.scalar_query(q)

  if not p['label']:
    p.template = 'admin/groups.error.tpl'
  else:
    if 'confirm' in p.form:
      if p.form['confirm'] == 'yes':
        #p.db.query_com('DELETE FROM rel_groups WHERE gid=%d' % (p['gid']))
        #p.db.query_com('DELETE FROM rel_rights WHERE gid=%d' % (p['gid']))
        #p.db.query_com('DELETE FROM groups WHERE gid=%d' % (p['gid']))
        p.template = 'admin/groups.delete_yes.tpl'
      else:
        p.template = 'admin/groups.delete_no.tpl'
    else:
      p.template = 'admin/groups.delete_confirm.tpl'

def insert():
  if 'g_label' not in p.form or not len(p.form['g_label']):
    p['errors']['g_label'] = 'Grup adı boş bırakılamaz.'
  else:
    q = """SELECT Count(*)
           FROM groups
           WHERE label="%s"
        """ % (p.db.escape(p.form['g_label']))
    if p.db.scalar_query(q) > 0:
      p['errors']['g_label'] = 'Bu isimde bir grup zaten var.'
      
  if not len(p['errors']):
    p['label'] = p.form['g_label']

    list = {
            'label': p['label']
            }
    p['gid'] = p.db.insert('groups', list)
    
    p.template = 'admin/groups.insert.tpl'
  else:
    p.template = 'admin/groups.tpl'
    index()


p.actions = {
             'default': index,
             'delete': delete,
             'insert': insert
             }

p.build()

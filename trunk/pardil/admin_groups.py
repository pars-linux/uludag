#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config

p = pardil_page()

p.name = 'pardil_index'
p.title = site_config['title']

# OLMAZSA OLMAZ!
if 'sid' not in p['session']:
  p.http.redirect('error.py?tag=login_required')
if not p.access('administrate'):
  p.http.redirect('error.py?tag=not_in_authorized_group')
# OLMAZSA OLMAZ!

def index():
  p['groups'] = []
  list = p.db.query('SELECT gid, label FROM groups ORDER BY gid ASC')
  for i in list:
    p['groups'].append({'gid': i[0], 'label': i[1]})

  p.template = site_config['path'] + 'templates/admin/groups.tpl'

def delete():
  try:
    p['gid'] = int(p.form['delete'])
  except:
    p.template = site_config['path'] + 'templates/admin/groups.error.tpl'
  else:
    p['label'] = p.db.scalar_query('SELECT label FROM groups WHERE gid=%d' % (p['gid']))
    if not p['label']:
      p.template = site_config['path'] + 'templates/admin/groups.error.tpl'
    else:
      if 'confirm' in p.form:
        if p.form['confirm'] == 'yes':
          #p.db.query_com('DELETE FROM rel_groups WHERE gid=%d' % (p['gid']))
          #p.db.query_com('DELETE FROM rel_rights WHERE gid=%d' % (p['gid']))
          #p.db.query_com('DELETE FROM groups WHERE gid=%d' % (p['gid']))
          p.template = site_config['path'] + 'templates/admin/groups.delete_yes.tpl'
        else:
          p.template = site_config['path'] + 'templates/admin/groups.delete_no.tpl'
      else:
        p.template = site_config['path'] + 'templates/admin/groups.delete_confirm.tpl'

def insert():
  if not len(p.form['g_label']):
    p['errors']['g_label'] = 'Grup adı boş bırakılamaz.'
  elif p.db.scalar_query('SELECT Count(*) FROM groups WHERE label="%s"' % (p.db.escape(p.form['g_label'] ) )) > 0:
    p['errors']['g_label'] = 'Bu isimde bir grup zaten var.'
      
  if not len(p['errors']):
    p['label'] = p.form['g_label']
    p['gid'] = p.db.insert('groups', {'label': p['label']})
    p.template = site_config['path'] + 'templates/admin/groups.insert.tpl'
  else:
    p.template = site_config['path'] + 'templates/admin/groups.tpl'
    index()


p.actions = {'default': index,
             'delete': delete,
             'insert': insert}

p.build()

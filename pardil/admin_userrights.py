#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config
import re
from math import ceil

p = pardil_page()

p.name = 'pardil_admin_userrights'
p.title = site_config['title']

# OLMAZSA OLMAZ!
if 'sid' not in p['session']:
  p.http.redirect('error.py?tag=login_required')
if 'administrate_userrights' not in p['acl'] and not p.site_admin():
  p.http.redirect('error.py?tag=not_in_authorized_group')
# OLMAZSA OLMAZ!

# Sayfalama
p['pag_now'] = int(p.form.getvalue('start', '0'))
p['pag_total'] = ceil(float(p.db.scalar_query("SELECT Count(*) FROM rel_rights")) / float(site_config['pag_perpage']))

def index():
  p['rel_rights'] = []
  q = """SELECT
           rel_rights.relid,
           groups.label,
           rights.category,
           rights.keyword,
           rights.label
         FROM rel_rights
           INNER JOIN groups
             ON groups.gid=rel_rights.gid
          INNER JOIN rights
             ON rights.rid=rel_rights.rid
         ORDER BY rights.category, rights.keyword ASC
         LIMIT %d, %d
      """ % (p['pag_now'] * site_config['pag_perpage'], site_config['pag_perpage'])
  list = p.db.query(q)
  for i in list:
    l = {
         'relid': i[0],
         'group': i[1],
         'category': i[2],
         'keyword': i[3],
         'right': i[4]
         }
    p['rel_rights'].append(l)

  p['groups'] = []
  q = """SELECT
           gid,
           label
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

  p['rights'] = []
  q = """SELECT
           rid, category, label
         FROM rights
         ORDER BY category, label ASC
      """
  list = p.db.query(q)
  for i in list:
    l = {
         'rid': i[0],
         'category': i[1],
         'label': i[2]
         }
    p['rights'].append(l)

  p.template = 'admin/userrights.tpl'

def delete():
  try:
    p['relid'] = int(p.form.getvalue('relid'))
  except:
    p.template = 'admin/userrights.error.tpl'
    return

  q = """SELECT groups.label
         FROM groups
           INNER JOIN rel_rights
             ON rel_rights.gid=groups.gid
         WHERE rel_rights.relid=%d
      """ % (p['relid'])
  p['group'] = p.db.scalar_query(q)
  q = """SELECT rights.label
         FROM rights
           INNER JOIN rel_rights
             ON rel_rights.rid=rights.rid
         WHERE rel_rights.relid=%d
      """ % (p['relid'])
  p['right'] = p.db.scalar_query(q)
  if not p['group'] or not p['right']:
    p.template = 'admin/userrights.error.tpl'
  else:
    if 'confirm' in p.form:
      if p.form.getvalue('confirm', '') == 'yes':
        q = """DELETE FROM rel_rights
               WHERE relid=%d
            """ % (p['relid'])
        p.db.query_com(q)
        p.template = 'admin/userrights.delete_yes.tpl'
      else:
        p.template = 'admin/userrights.delete_no.tpl'
    else:
      p.template = 'admin/userrights.delete_confirm.tpl'

def insert():
  try:
    rid = int(p.form.getvalue('r_right'))
    gid = int(p.form.getvalue('r_group'))
  except:
    p['errors']['r_right'] = 'Geçersiz erişim hakkı numarası.'
  else:
    q1 = """SELECT Count(*)
            FROM rights
            WHERE rid=%d
         """ % (rid)
    q2 = """SELECT Count(*)
            FROM groups
            WHERE gid=%d
         """ % (gid)
    q3 = """SELECT Count(*)
            FROM rel_rights
            WHERE gid=%d AND rid=%d
         """ % (gid, rid)
    if p.db.scalar_query(q1) == 0:
      p['errors']['r_right'] = 'Geçersiz erişim hakkı numarası.'
    elif p.db.scalar_query(q2) == 0:
      p['errors']['r_group'] = 'Geçersiz grup numarası.'
    elif p.db.scalar_query(q3) > 0:
      p['errors']['r_right'] = 'Bu grup bu hakka zaten sahip.'
     
  if not len(p['errors']):
    p.template = 'admin/userrights.insert.tpl'
    
    q = """SELECT label
           FROM groups
           WHERE gid=%d
        """ % (gid)
    p['group'] = p.db.scalar_query(q)

    q = """SELECT label
           FROM rights
           WHERE rid=%d
        """ % (rid)
    p['right'] = p.db.scalar_query(q)

    list = {
            'gid': gid,
            'rid': rid
            }
    p['relid'] = p.db.insert('rel_rights', list)

  else:  
    p.template = 'admin/userrights.tpl'
    index()

p.actions = {
             'default': index,
             'delete': delete,
             'insert': insert
             }

p.build()

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
  p['rel_rights'] = []
  list = p.db.query('SELECT rel_rights.relid, groups.label, rights.category, rights.keyword, rights.label FROM rel_rights INNER JOIN groups ON groups.gid=rel_rights.gid INNER JOIN rights ON rights.rid=rel_rights.rid  ORDER BY rights.category, rights.keyword ASC')
  for i in list:
    p['rel_rights'].append({'relid': i[0], 'group': i[1], 'category': i[2], 'keyword': i[3], 'right': i[4]})

  p['groups'] = []
  list = p.db.query('SELECT gid, label FROM groups ORDER BY gid ASC')
  for i in list:
    p['groups'].append({'gid': i[0], 'label': i[1]})

  p['rights'] = []
  list = p.db.query('SELECT rid, label FROM rights ORDER BY category, keyword ASC')
  for i in list:
    p['rights'].append({'rid': i[0], 'label': i[1]})

  p.template = site_config['path'] + 'templates/admin/rights.tpl'

def delete():
  try:
    p['relid'] = int(p.form['delete'])
  except:
    p.template = site_config['path'] + 'templates/admin/rights.error.tpl'
  else:
    p['group'] = p.db.scalar_query('SELECT groups.label FROM groups INNER JOIN rel_rights ON rel_rights.gid=groups.gid WHERE rel_rights.relid=%d' % (p['relid']))
    p['right'] = p.db.scalar_query('SELECT rights.label FROM rights INNER JOIN rel_rights ON rel_rights.rid=rights.rid WHERE rel_rights.relid=%d' % (p['relid']))
    if not p['group'] or not p['right']:
      p.template = site_config['path'] + 'templates/admin/rights.error.tpl'
    else:
      if 'confirm' in p.form:
        if p.form['confirm'] == 'yes':
          p.db.query_com('DELETE FROM rel_rights WHERE relid=%d' % (p['relid']))
          p.template = site_config['path'] + 'templates/admin/rights.delete_yes.tpl'
        else:
          p.template = site_config['path'] + 'templates/admin/rights.delete_no.tpl'
      else:
        p.template = site_config['path'] + 'templates/admin/rights.delete_confirm.tpl'

def insert():
  try:
    rid = int(p.form['r_right'])
    gid = int(p.form['r_group'])
  except:
    p['errors']['r_right'] = 'Geçersiz erişim hakkı numarası.'
  else:
    if p.db.scalar_query('SELECT Count(*) FROM rights WHERE rid=%d' % (rid)) == 0:
      p['errors']['r_right'] = 'Geçersiz erişim hakkı numarası.'
    elif p.db.scalar_query('SELECT Count(*) FROM groups WHERE gid=%d' % (gid)) == 0:
      p['errors']['r_group'] = 'Geçersiz grup numarası.'
    elif p.db.scalar_query('SELECT Count(*) FROM rel_rights WHERE gid=%d AND rid=%d' % (gid, rid)) > 0:
      p['errors']['r_right'] = 'Bu grup bu hakka zaten sahip.'
     
  if not len(p['errors']):
    p.template = site_config['path'] + 'templates/admin/rights.insert.tpl'

    p['group'] = p.db.scalar_query('SELECT groups.label FROM groups WHERE gid=%d' % (gid))
    p['right'] = p.db.scalar_query('SELECT rights.label FROM rights WHERE rid=%d' % (rid))

    p['relid'] = p.db.insert('rel_rights', {'gid': gid, 'rid': rid})
  else:  
    p.template = site_config['path'] + 'templates/admin/rights.tpl'
    index()

p.actions = {'default': index,
             'delete': delete,
             'insert': insert}

p.build()

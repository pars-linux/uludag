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
  p['rel_groups'] = []
  list = p.db.query('SELECT rel_groups.relid, groups.label, users.username FROM rel_groups INNER JOIN groups ON groups.gid=rel_groups.gid INNER JOIN users ON users.uid=rel_groups.uid ORDER BY groups.label, users.username ASC')
  for i in list:
    p['rel_groups'].append({'relid': i[0], 'group': i[1], 'username': i[2]})

  p['groups'] = []
  list = p.db.query('SELECT gid, label FROM groups ORDER BY gid ASC')
  for i in list:
    p['groups'].append({'gid': i[0], 'label': i[1]})

  p['users'] = []
  list = p.db.query('SELECT uid, username FROM users ORDER BY username ASC')
  for i in list:
    p['users'].append({'uid': i[0], 'username': i[1]})

  p.template = site_config['path'] + 'templates/admin/usergroups.tpl'

def delete():
  try:
    p['relid'] = int(p.form['delete'])
  except:
    p.template = site_config['path'] + 'templates/admin/usergroups.error.tpl'
  else:
    p['group'] = p.db.scalar_query('SELECT groups.label FROM groups INNER JOIN rel_groups ON rel_groups.gid=groups.gid WHERE rel_groups.relid=%d' % (p['relid']))
    p['user'] = p.db.scalar_query('SELECT users.username FROM users INNER JOIN rel_groups ON rel_groups.uid=users.uid WHERE rel_groups.relid=%d' % (p['relid']))
    if not p['group'] or not p['user']:
      p.template = site_config['path'] + 'templates/admin/usergroups.error.tpl'
    else:
      if 'confirm' in p.form:
        if p.form['confirm'] == 'yes':
          p.db.query_com('DELETE FROM rel_groups WHERE relid=%d' % (p['relid']))
          p.template = site_config['path'] + 'templates/admin/usergroups.delete_yes.tpl'
        else:
          p.template = site_config['path'] + 'templates/admin/usergroups.delete_no.tpl'
      else:
        p.template = site_config['path'] + 'templates/admin/usergroups.delete_confirm.tpl'

def insert():
  try:
    uid = int(p.form['u_user'])
    gid = int(p.form['u_group'])
  except:
    p['errors']['u_user'] = 'Geçersiz kullanıcı numarası.'
  else:
    if p.db.scalar_query('SELECT Count(*) FROM users WHERE uid=%d' % (uid)) == 0:
      p['errors']['u_user'] = 'Geçersiz kullanıcı numarası.'
    elif p.db.scalar_query('SELECT Count(*) FROM groups WHERE gid=%d' % (gid)) == 0:
      p['errors']['u_group'] = 'Geçersiz grup numarası.'
    elif p.db.scalar_query('SELECT Count(*) FROM rel_groups WHERE gid=%d AND uid=%d' % (gid, uid)) > 0:
      p['errors']['u_user'] = 'Kullanıcı zaten bu gruba dahil.'
     
  if not len(p['errors']):
    p.template = site_config['path'] + 'templates/admin/usergroups.insert.tpl'

    p['group'] = p.db.scalar_query('SELECT groups.label FROM groups WHERE gid=%d' % (gid))
    p['user'] = p.db.scalar_query('SELECT users.username FROM users WHERE uid=%d' % (uid))

    p['relid'] = p.db.insert('rel_groups', {'gid': gid, 'uid': uid})
  else:  
    p.template = site_config['path'] + 'templates/admin/usergroups.tpl'
    index()

p.actions = {'default': index,
             'delete': delete,
             'insert': insert}

p.build()

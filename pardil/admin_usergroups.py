#!/usr/bin/python
from cfg_main import site_config
from lib_cheetah import build_page
from lib_std import page_init
from lib_sql import op_access

import cgi

def index():
  # Veritabanı bağlantısı kur, oturum aç, template bilgilerini yükle
  db, cookie, data = page_init()

  # OLMAZSA OLMAZ!
  if not data['session'].has_key('uid'):
    print 'Location: error.py?tag=login_required'
    print ''
    
  if not op_access(db, data['session']['uid'], 'administrate'):
    print 'Location: error.py?tag=not_in_authorized_group'
    print ''
  # OLMAZSA OLMAZ!

  form = cgi.FieldStorage()
  
  if form.has_key('delete'):
    try:
      data['relid'] = int(form.getvalue('delete'))
    except:
      data['status'] = 'error'
    else:
      data['group'] = db.scalar_query('SELECT groups.label FROM groups INNER JOIN rel_groups ON rel_groups.gid=groups.gid WHERE rel_groups.relid=%d' % (data['relid']))
      data['user'] = db.scalar_query('SELECT users.username FROM users INNER JOIN rel_groups ON rel_groups.uid=users.uid WHERE rel_groups.relid=%d' % (data['relid']))
      if not data['group'] or not data['user']:
        data['status'] = 'error'
      else:
        if form.has_key('confirm'):
          if form.getvalue('confirm') == 'yes':
            db.query_com('DELETE FROM rel_groups WHERE relid=%d' % (data['relid']))
            data['status'] = 'delete_yes'
          else:
            data['status'] = 'delete_no'
        else:
          data['status'] = 'delete_confirm'
  elif form.has_key('insert'):
    try:
      uid = int(form.getvalue('u_user'))
      gid = int(form.getvalue('u_group'))
    except:
      data['errors']['u_user'] = 'Geçersiz kullanıcı numarası.'

    if db.scalar_query('SELECT Count(*) FROM users WHERE uid=%d' % (uid)) == 0:
      data['errors']['u_user'] = 'Geçersiz kullanıcı numarası.'
    elif db.scalar_query('SELECT Count(*) FROM groups WHERE gid=%d' % (gid)) == 0:
      data['errors']['u_group'] = 'Geçersiz grup numarası.'
    elif db.scalar_query('SELECT Count(*) FROM rel_groups WHERE gid=%d AND uid=%d' % (gid, uid)) > 0:
      data['errors']['u_user'] = 'Kullanıcı zaten bu gruba dahil.'
      
    if not len(data['errors']):
      data['status'] = 'insert'

      data['group'] = db.scalar_query('SELECT groups.label FROM groups WHERE gid=%d' % (gid))
      data['user'] = db.scalar_query('SELECT users.username FROM users WHERE uid=%d' % (uid))

      data['relid'] = db.insert('rel_groups', {'gid': gid, 'uid': uid})
      data['status'] = 'insert'
    else:
      data['rel_groups'] = []
      list = db.query('SELECT rel_groups.relid, groups.label, users.username FROM rel_groups INNER JOIN groups ON groups.gid=rel_groups.gid INNER JOIN users ON users.uid=rel_groups.uid ORDER BY groups.label, users.username ASC')
      for i in list:
        data['rel_groups'].append({'relid': i[0], 'group': i[1], 'username': i[2]})

      data['groups'] = []
      list = db.query('SELECT gid, label FROM groups ORDER BY gid ASC')
      for i in list:
        data['groups'].append({'gid': i[0], 'label': i[1]})

      data['users'] = []
      list = db.query('SELECT uid, username FROM users ORDER BY username ASC')
      for i in list:
        data['users'].append({'uid': i[0], 'username': i[1]})
  else:
    data['rel_groups'] = []
    list = db.query('SELECT rel_groups.relid, groups.label, users.username FROM rel_groups INNER JOIN groups ON groups.gid=rel_groups.gid INNER JOIN users ON users.uid=rel_groups.uid ORDER BY groups.label, users.username ASC')
    for i in list:
      data['rel_groups'].append({'relid': i[0], 'group': i[1], 'username': i[2]})

    data['groups'] = []
    list = db.query('SELECT gid, label FROM groups ORDER BY gid ASC')
    for i in list:
      data['groups'].append({'gid': i[0], 'label': i[1]})

    data['users'] = []
    list = db.query('SELECT uid, username FROM users ORDER BY username ASC')
    for i in list:
      data['users'].append({'uid': i[0], 'username': i[1]})

  # Sayfayı derle.
  build_page(site_config['path'] + 'templates/admin/usergroups.tpl', data)


index()

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
      data['gid'] = int(form.getvalue('delete'))
    except:
      data['status'] = 'error'
    else:
      data['label'] = db.scalar_query('SELECT label FROM groups WHERE gid=%d' % (data['gid']))
      if not data['label']:
        data['status'] = 'error'
      else:
        if form.has_key('confirm'):
          if form.getvalue('confirm') == 'yes':
            db.query_com('DELETE FROM rel_groups WHERE gid=%d' % (data['gid']))
            db.query_com('DELETE FROM rel_rights WHERE gid=%d' % (data['gid']))
            db.query_com('DELETE FROM groups WHERE gid=%d' % (data['gid']))
            data['status'] = 'delete_yes'
          else:
            data['status'] = 'delete_no'
        else:
          data['status'] = 'delete_confirm'
  elif form.has_key('insert'):
    if not len(form.getvalue('g_label', '')):
      data['errors']['g_label'] = 'Grup adı boş bırakılamaz.'
    elif db.scalar_query('SELECT Count(*) FROM groups WHERE label="%s"' % (db.escape(form.getvalue('g_label') ) )) > 0:
      data['errors']['g_label'] = 'Bu isimde bir grup zaten var.'
      
    if not (data['errors']):
      data['label'] = form.getvalue('g_label')
      data['gid'] = db.insert('groups', {'label': data['label']})
      data['status'] = 'insert'
    else:
      data['status'] = 'list'
      data['groups'] = []
      list = db.query('SELECT gid, label FROM groups ORDER BY gid ASC')
      for i in list:
        data['groups'].append({'gid': i[0], 'label': i[1]})
  else:
    data['groups'] = []
    list = db.query('SELECT gid, label FROM groups ORDER BY gid ASC')
    for i in list:
      data['groups'].append({'gid': i[0], 'label': i[1]})

  # Sayfayı derle.
  build_page(site_config['path'] + 'templates/admin/groups.tpl', data)


index()

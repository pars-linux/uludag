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
      data['group'] = db.scalar_query('SELECT groups.label FROM groups INNER JOIN rel_rights ON rel_rights.gid=groups.gid WHERE rel_rights.relid=%d' % (data['relid']))
      data['right'] = db.scalar_query('SELECT rights.label FROM rights INNER JOIN rel_rights ON rel_rights.rid=rights.rid WHERE rel_rights.relid=%d' % (data['relid']))
      if not data['group'] or not data['right']:
        data['status'] = 'error'
      else:
        if form.has_key('confirm'):
          if form.getvalue('confirm') == 'yes':
            db.query_com('DELETE FROM rel_rights WHERE relid=%d' % (data['relid']))
            data['status'] = 'delete_yes'
          else:
            data['status'] = 'delete_no'
        else:
          data['status'] = 'delete_confirm'
  elif form.has_key('insert'):
    try:
      rid = int(form.getvalue('r_right'))
      gid = int(form.getvalue('r_group'))
    except:
      data['errors']['r_right'] = 'Geçersiz erişim hakkı numarası.'

    if db.scalar_query('SELECT Count(*) FROM rights WHERE rid=%d' % (rid)) == 0:
      data['errors']['r_right'] = 'Geçersiz erişim hakkı numarası.'
    elif db.scalar_query('SELECT Count(*) FROM groups WHERE gid=%d' % (gid)) == 0:
      data['errors']['r_group'] = 'Geçersiz grup numarası.'
    elif db.scalar_query('SELECT Count(*) FROM rel_rights WHERE gid=%d AND rid=%d' % (gid, rid)) > 0:
      data['errors']['r_right'] = 'Bu grup bu hakka zaten sahip.'
      
    if not len(data['errors']):
      data['status'] = 'insert'

      data['group'] = db.scalar_query('SELECT groups.label FROM groups WHERE gid=%d' % (gid))
      data['right'] = db.scalar_query('SELECT rights.label FROM rights WHERE rid=%d' % (rid))

      data['relid'] = db.insert('rel_rights', {'gid': gid, 'rid': rid})
      data['status'] = 'insert'
    else:
      data['status'] = 'list'
      data['rel_rights'] = []
      list = db.query('SELECT rel_rights.relid, groups.label, rights.category, rights.keyword, rights.label FROM rel_rights INNER JOIN groups ON groups.gid=rel_rights.gid INNER JOIN rights ON rights.rid=rel_rights.rid  ORDER BY rights.category, rights.keyword ASC')
      for i in list:
        data['rel_rights'].append({'relid': i[0], 'group': i[1], 'category': i[2], 'keyword': i[3], 'right': i[4]})

      data['groups'] = []
      list = db.query('SELECT gid, label FROM groups ORDER BY gid ASC')
      for i in list:
        data['groups'].append({'gid': i[0], 'label': i[1]})

      data['rights'] = []
      list = db.query('SELECT rid, label FROM rights ORDER BY category, keyword ASC')
      for i in list:
        data['rights'].append({'rid': i[0], 'label': i[1]})
  else:
    data['rel_rights'] = []
    list = db.query('SELECT rel_rights.relid, groups.label, rights.category, rights.keyword, rights.label FROM rel_rights INNER JOIN groups ON groups.gid=rel_rights.gid INNER JOIN rights ON rights.rid=rel_rights.rid  ORDER BY rights.category, rights.keyword ASC')
    for i in list:
      data['rel_rights'].append({'relid': i[0], 'group': i[1], 'category': i[2], 'keyword': i[3], 'right': i[4]})

    data['groups'] = []
    list = db.query('SELECT gid, label FROM groups ORDER BY gid ASC')
    for i in list:
      data['groups'].append({'gid': i[0], 'label': i[1]})

    data['rights'] = []
    list = db.query('SELECT rid, label FROM rights ORDER BY category, keyword ASC')
    for i in list:
      data['rights'].append({'rid': i[0], 'label': i[1]})

  # Sayfayı derle.
  build_page(site_config['path'] + 'templates/admin/rights.tpl', data)


index()

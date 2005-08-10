#!/usr/bin/python

from cfg_main import site_config

from lib_cheetah import build_page
from lib_std import page_init
from lib_sql import *

import re
import cgi

def index():
  # Veritabanı bağlantısı kur, oturum aç, template bilgilerini yükle
  db, cookie, data = page_init()

  data['revision'] = 0

  if not data['session'].has_key('uid'):
    print 'Location: error.py?tag=login_required'
    print ''

  form = cgi.FieldStorage()

  if not form.has_key('pid'):
    # Yeni öneri
    # Öneri ekleme hakkı olması yeterli.
    if not op_access(db, data['session']['uid'], 'proposals_add'):
      print 'Location: error.py?tag=not_in_authorized_group'
      print ''
  else:
    # Öneriyi düzenleme, ya da yeni sürüm ekleme
    # Öneri sorumlusu olma ve öneri ekleme hakkı olması gerekli.
    if not op_access(db, data['session']['uid'], 'proposals_add') or not is_maintainer(db, data['session']['uid'], form.getvalue('pid')):
      print 'Location: error.py?tag=not_maintainer'
      print ''
    else:
      data['revision'] = 1
      data['pid'] = int(form.getvalue('pid'))

      if form.has_key('version'):
        data['version'] = form.getvalue('version')
      else:
        data['version'] = db.scalar_query('SELECT version FROM proposals_versions WHERE pid=%d ORDER BY vid DESC LIMIT 1' % (data['pid']))

      row = db.row_query('SELECT version, title, content FROM proposals_versions WHERE pid=%d AND version="%s"' % (data['pid'], db.escape(data['version'])))

      data['posted_values']['p_version'] = row[0]
      data['posted_values']['p_title'] = row[1]
      data['posted_values']['p_content'] = row[2]

  # Form gönderildiyse...
  if form.has_key('new_proposal'):

    # Gönderilen verileri data['posted_values'] içine aktar.
    for i in form.keys():
      data['posted_values'][i] = form.getvalue(i)

    # Hata denetimi

    if not len(form.getvalue('p_title', '')):
      data['errors']['p_title'] = 'Başlık boş bırakılamaz.'
    elif len(form.getvalue('p_title')) > 100:
      data['errors']['p_title'] = 'Başlık en fazla 100 karakter olabilir.'
    
    if data['revision']:
      if not len(form.getvalue('p_version', '')):
        data['errors']['p_version'] = 'Sürüm numarası boş bırakılamaz.'

    # Hiç hata yoksa...
    if not len(data['errors']):

      # Veritabanına kayıt yap...
      #insert_list = {}
      #db.query_com(db.insert('users', insert_list))

      # İşlem durumunu "bitti" olarak belirle
      data['status'] = 'done'
      
  # Sayfayı derle.
  build_page(site_config['path'] + 'templates/new_proposal.tpl', data)

index()

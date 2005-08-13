#!/usr/bin/python
from cfg_main import site_config
from lib_cheetah import build_page
from lib_std import page_init
from lib_sql import op_access

def index():
  # Veritabanı bağlantısı kur, oturum aç, temel template bilgilerini yükle
  db, cookie, data = page_init()

  # OLMAZSA OLMAZ!
  if not data['session'].has_key('uid'):
    print 'Location: error.py?tag=login_required'
    print ''
    
  if not op_access(db, data['session']['uid'], 'administrate'):
    print 'Location: error.py?tag=not_in_authorized_group'
    print ''
  # OLMAZSA OLMAZ!

  # Sayfayı derle.
  build_page(site_config['path'] + 'templates/admin/index.tpl', data)

index()

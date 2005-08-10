#!/usr/bin/python

from cfg_main import site_config
from lib_cheetah import build_page
from lib_std import page_init

def index():
  # Veritabanı bağlantısı kur, oturum aç, template bilgilerini yükle
  db, cookie, data = page_init()

  # Oturum bilgilerini yoket.
  if data['session']:
    db.query_com('DELETE FROM sessions WHERE sid="%s"' % (db.escape(data['session']['sid'])))
    
    cookie.set('sid', '')
    cookie.save()
    
    data['session'] = {}

  # Sayfayı derle.
  build_page(site_config['path'] + 'templates/logout.tpl', data)

index()

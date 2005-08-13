#!/usr/bin/python
from cfg_main import site_config
from lib_cheetah import build_page
from lib_std import page_init

import cgi

def index():
  # Veritabanı bağlantısı kur, oturum aç, temel template bilgilerini yükle
  db, cookie, data = page_init()

  form = cgi.FieldStorage()
  data['keyword'] = form.getvalue('tag')

  # Sayfayı derle.
  build_page(site_config['path'] + 'templates/error.tpl', data)

index()

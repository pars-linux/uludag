#!/usr/bin/python

from cfg_main import site_config

from lib_cheetah import build_page
from lib_std import page_init
from lib_string import pass_hash, html_escape
from lib_date import *

import random
import re
import cgi

def index():
  # Veritabanı bağlantısı kur, oturum aç, template bilgilerini yükle
  db, cookie, data = page_init()

  sid = pass_hash('%d%f' % (now(), random.random()))
  uid = ''

  form = cgi.FieldStorage()

  # Form gönderildiyse...
  if form.has_key('login'):

    # Gönderilen verileri data['posted_values'] içine aktar.
    for i in form.keys():
      data['posted_values'][i] = form.getvalue(i)

    # Kullanıcı adını kontrol et.
    if not len(form.getvalue('l_username', '')):
      data['errors']['l_username'] = 'Kullanıcı adı boş bırakılamaz.'
    elif not re.match('^[a-zA-Z0-9]{4,32}$', form.getvalue('l_username')):
      data['errors']['l_username'] = 'Kullanıcı adı 4-32 karakter uzunlukta, alfanumerik olmalı.'
      
    if not len(form.getvalue('l_password', '')):
      data['errors']['l_password'] = 'Parola boş bırakılamaz.'
    else:
      uid = db.scalar_query('SELECT uid FROM users WHERE username="%s" AND password="%s"' % (db.escape(form.getvalue('l_username')), db.escape(pass_hash(form.getvalue('l_password')))))
      if not uid:
        data['errors']['l_password'] = 'Hatalı şifre ya da kullanıcı adı.'

    # Hiç hata yoksa...
    if not len(data['errors']):

      # Kullanıcı bilgilerini oturum bilgilerine iliştir
      if not data['session']:

        # Kullanıcı bilgilerini toparla
        data['session']['sid'] = sid
        data['session']['uid'] = uid
        data['session']['username'] = form.getvalue('l_username')

        # Veritabanına yaz...
        db.query_com('INSERT INTO sessions (sid, uid, timeB) VALUES ("%s", %d, %d)' % (sid, uid, now()))

        # Çerezlere yaz...
        cookie.set('sid', sid)
        cookie.save()

      # İşlem durumunu "bitti" olarak belirle
      data['status'] = 'done'
      
  # Sayfayı derle.
  build_page(site_config['path'] + 'templates/login.tpl', data)

index()

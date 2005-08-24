#!/usr/bin/python

from cfg_main import site_config

from lib_cheetah import build_page
from lib_std import page_init
from lib_string import pass_hash

import re
import cgi

def index():
  # Veritabanı bağlantısı kur, oturum aç, template bilgilerini yükle
  db, cookie, data = page_init()

  form = cgi.FieldStorage()

  # Form gönderildiyse...
  if form.has_key('register'):

    # Gönderilen verileri data['posted_values'] içine aktar.
    for i in form.keys():
      data['posted_values'][i] = form[i]
    # Kullanıcı adını kontrol et.
    if not len(form.getvalue('r_username', '')):
      data['errors']['r_username'] = 'Kullanıcı adı boş bırakılamaz.'
    elif not re.match('^[a-zA-Z0-9]{4,32}$', form.getvalue('r_username')):
      data['errors']['r_username'] = 'Kullanıcı adı 4-32 karakter uzunlukta, alfanumerik olmalı.'
    elif db.scalar_query('SELECT Count(*) FROM users WHERE username="%s"' % (db.escape(form.getvalue('r_username')))) > 0:
      data['errors']['r_username'] = 'Kullanıcı adı başkası tarafından kullanılıyor.'
   
    # E-posta adresini kontrol et.
    if not len(form.getvalue('r_email', '')):
      data['errors']['r_email'] = 'E-posta adresi boş bırakılamaz.'
    elif not re.match('^[a-z0-9_\.-]+@([a-z0-9]+(\-*[a-z0-9]+)*\.)+[a-z]{2,4}$', form.getvalue('r_email')):
      data['errors']['r_email'] = 'E-posta adresi geçerli formatta olmalı.'
    elif db.scalar_query('SELECT Count(*) FROM users WHERE email="%s"' % (db.escape(form.getvalue('r_email')))) > 0:
      data['errors']['r_email'] = 'E-posta adresi başkası tarafından kullanılıyor.'
      
    # Parolayı kontrol et.
    if not len(form.getvalue('r_password', '')):
      data['errors']['r_password'] = 'Parola boş bırakılamaz.'
    elif form.getvalue('r_password') != form.getvalue('r_password2'):
      data['errors']['r_password'] = 'İki parola, birbiriyle aynı olmalı.'
    elif not re.match('^.{6}$', form.getvalue('r_password')):
      data['errors']['r_password'] = 'Parola en az 6 karakter uzunlukta olmalı.'
      
    # Hiç hata yoksa...
    if not len(data['errors']):

      # Veritabanına kayıt yap...
      insert_list = {'username': form.getvalue('r_username'), 'password': pass_hash(form.getvalue('r_password')), 'email': form.getvalue('r_email')}
      uid = db.insert('users', insert_list)

      # İşlem durumunu "bitti" olarak belirle
      data['status'] = 'done'

  # Sayfayı derle.
  build_page(site_config['path'] + 'templates/register.tpl', data)

index()

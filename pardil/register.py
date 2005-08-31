#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config
from pyonweb.libstring import *
from pyonweb.libdate import *
from pyonweb.mail import sendmail

import re

p = pardil_page()

p.name = 'pardil_register'
p.title = site_config['title']

def index():
  p.template = 'register.tpl'

def register():
  p.template = 'register.tpl'

  # Kullanıcı adını kontrol et.
  if 'r_username' not in p.form or not len(p.form['r_username']):
    p['errors']['r_username'] = 'Kullanıcı adı boş bırakılamaz.'
  elif not re.match('^[a-zA-Z0-9]{4,32}$', p.form['r_username']):
    p['errors']['r_username'] = 'Kullanıcı adı 4-32 karakter uzunlukta, alfanumerik olmalı.'
  else:
    q = """SELECT Count(*)
           FROM users
           WHERE username="%s"
        """ % (p.db.escape(p.form['r_username']))
    if p.db.scalar_query(q) > 0:
      p['errors']['r_username'] = 'Kullanıcı adı başkası tarafından kullanılıyor.'
   
  # E-posta adresini kontrol et.
  if 'r_email' not in p.form or not len(p.form['r_email']):
    p['errors']['r_email'] = 'E-posta adresi boş bırakılamaz.'
  elif not re.match('^[a-z0-9_\.-]+@([a-z0-9]+(\-*[a-z0-9]+)*\.)+[a-z]{2,4}$', p.form['r_email']):
    p['errors']['r_email'] = 'E-posta adresi geçerli formatta olmalı.'
  else:
    q = """SELECT Count(*)
           FROM users
           WHERE email="%s"
        """ % (p.db.escape(p.form['r_email']))
    if p.db.scalar_query(q) > 0:
      p['errors']['r_email'] = 'E-posta adresi başkası tarafından kullanılıyor.'
      
  # Parolayı kontrol et.
  if 'r_password' not in p.form or \
     'r_password2' not in p.form or \
     not len(p.form['r_password']) or \
     not len(p.form['r_password2']):
    p['errors']['r_password'] = 'Parola boş bırakılamaz.'
  elif p.form['r_password'] != p.form['r_password2']:
    p['errors']['r_password'] = 'İki parola, birbiriyle aynı olmalı.'
  elif not re.match('^.{6,10}$', p.form['r_password']):
    p['errors']['r_password'] = 'Parola en az 6, en fazla 10 karakter uzunluğunda olmalı.'
      
  # Hiç hata yoksa...
  if not len(p['errors']):

    
    # "Users - Pending" tablosuna ekle
    act_code = pass_hash(str(time.time()))
    list = {
            'username': p.form['r_username'],
            'password': pass_hash(p.form['r_password']),
            'email': p.form['r_email'],
            'timeB': sql_datetime(now()),
            'code': act_code
            }
    p.db.insert('users_pending', list)


    # E-posta gönder

    t = "Pardil - Üyelik Aktivasyonu"
    link = site_config['url'] + 'activate.py?code=' + act_code
    b = "Merhaba,\n\nKayıt işlemini tamamlamak için aşağıdaki adresi ziyaret edin:\n%s\n\nPardil" % (link)
    sendmail(site_config['mail'], p.form['r_email'], t, b)

    p['debug'] = b
    p.template = "register.done.tpl"
    

p.actions = {
             'default': index,
             'register': register
             }

p.build()

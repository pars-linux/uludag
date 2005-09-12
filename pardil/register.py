#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config
from pyonweb.libstring import *
from pyonweb.libdate import *
from pyonweb.mail import sendmail
from pyonweb.template import build_template

import re
import random

p = pardil_page()

p.name = 'pardil_register'
p.title = site_config['title']

def index():
  p.template = 'register.tpl'

def register():
  p.template = 'register.tpl'

  # Kullanıcı adını kontrol et.
  if not len(p.form.getvalue('r_username', '')):
    p['errors']['r_username'] = 'Kullanıcı adı boş bırakılamaz.'
  elif not re.match('^[a-zA-Z0-9]{4,32}$', p.form.getvalue('r_username')):
    p['errors']['r_username'] = 'Kullanıcı adı 4-32 karakter uzunlukta, alfanumerik olmalı.'
  else:
    q = """SELECT Count(*)
           FROM users
           WHERE username="%s"
        """ % (p.db.escape(p.form.getvalue('r_username')))
    if p.db.scalar_query(q) > 0:
      p['errors']['r_username'] = 'Kullanıcı adı başkası tarafından kullanılıyor.'
   
  # E-posta adresini kontrol et.
  if not len(p.form.getvalue('r_email', '')):
    p['errors']['r_email'] = 'E-posta adresi boş bırakılamaz.'
  elif not re.match('^[A-Za-z0-9_\.-]+@([A-Za-z0-9]+(\-*[A-Za-z0-9]+)*\.)+[A-Za-z]{2,4}$', p.form.getvalue('r_email')):
    p['errors']['r_email'] = 'E-posta adresi geçerli formatta olmalı.'
  else:
    q = """SELECT Count(*)
           FROM users
           WHERE email="%s"
        """ % (p.db.escape(p.form.getvalue('r_email')))
    if p.db.scalar_query(q) > 0:
      p['errors']['r_email'] = 'E-posta adresi başkası tarafından kullanılıyor.'
      
  # Parolayı kontrol et.
  if not len(p.form.getvalue('r_password', '')) or not len(p.form.getvalue('r_password2', '')):
    p['errors']['r_password'] = 'Parola boş bırakılamaz.'
  elif p.form.getvalue('r_password') != p.form.getvalue('r_password2'):
    p['errors']['r_password'] = 'İki parola, birbiriyle aynı olmalı.'
  elif not re.match('^.{6,10}$', p.form.getvalue('r_password')):
    p['errors']['r_password'] = 'Parola en az 6, en fazla 10 karakter uzunluğunda olmalı.'
      
  # Hiç hata yoksa...
  if not len(p['errors']):

    
    # "Users - Pending" tablosuna ekle
    act_code = pass_hash(str(random.random()))
    list = {
            'username': p.form.getvalue('r_username'),
            'password': pass_hash(p.form.getvalue('r_password')),
            'email': p.form.getvalue('r_email'),
            'timeB': sql_datetime(now()),
            'code': act_code
            }
    p.db.insert('users_pending', list)


    # E-posta gönder

    t = "Pardil - Üyelik Aktivasyonu"
    list = {
            'link': site_config['url'] + 'activate.py?code=' + act_code,
            'time': num2str(site_config['activation_timeout'])
            }
    b = build_template(site_config['path'] + 'templates/email/register.tpl', list)
    sendmail(site_config['mail'], p.form.getvalue('r_email'), t, b)

    p['time'] = num2str(site_config['activation_timeout'])
    p.template = "register.done.tpl"
    

p.actions = {
             'default': index,
             'register': register
             }

p.build()

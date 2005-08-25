#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config

import re

p = pardil_page()

p.name = 'pardil_register'
p.title = site_config['title']

def index():
  p.template = site_config['path'] + 'templates/register.tpl'

def register():
  p.template = site_config['path'] + 'templates/register.tpl'

  # Kullanıcı adını kontrol et.
  if not len(p.form['r_username']):
    p['errors']['r_username'] = 'Kullanıcı adı boş bırakılamaz.'
  elif not re.match('^[a-zA-Z0-9]{4,32}$', p.form['r_username']):
    p['errors']['r_username'] = 'Kullanıcı adı 4-32 karakter uzunlukta, alfanumerik olmalı.'
  elif p.db.scalar_query('SELECT Count(*) FROM users WHERE username="%s"' % (p.db.escape(p.form['r_username']))) > 0:
    p['errors']['r_username'] = 'Kullanıcı adı başkası tarafından kullanılıyor.'
   
  # E-posta adresini kontrol et.
  if not len(p.form['r_email']):
    p['errors']['r_email'] = 'E-posta adresi boş bırakılamaz.'
  elif not re.match('^[a-z0-9_\.-]+@([a-z0-9]+(\-*[a-z0-9]+)*\.)+[a-z]{2,4}$', p.form['r_email']):
    p['errors']['r_email'] = 'E-posta adresi geçerli formatta olmalı.'
  elif p.db.scalar_query('SELECT Count(*) FROM users WHERE email="%s"' % (p.db.escape(p.form['r_email']))) > 0:
    p['errors']['r_email'] = 'E-posta adresi başkası tarafından kullanılıyor.'
      
  # Parolayı kontrol et.
  if not len(p.form['r_password']):
    p['errors']['r_password'] = 'Parola boş bırakılamaz.'
  elif p.form['r_password'] != p.form['r_password2']:
    p['errors']['r_password'] = 'İki parola, birbiriyle aynı olmalı.'
  elif not re.match('^.{6,10}$', p.form['r_password']):
    p['errors']['r_password'] = 'Parola en az 6, en fazla 10 karakter uzunluğunda olmalı.'
      
  # Hiç hata yoksa...
  if not len(p['errors']):
    # Veritabanına kayıt yap...
    insert_list = {'username': p.form['r_username'],
                   'password': p.pass_hash(p.form['r_password']),
                   'email': p.form['r_email']}
    uid = db.insert('users', insert_list)
    p.template = site_config['path'] + 'templates/register.done.tpl'


p.actions = {'default': index,
            'register': register}

p.build()

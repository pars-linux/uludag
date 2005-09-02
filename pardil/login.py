#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config

import re

p = pardil_page()

p.name = 'pardil_login'
p.title = site_config['title']

def index():
  p.template = 'login.tpl'

def login():
  p.template = 'login.tpl'

  if not len(p.form.getvalue('l_username', '')):
    p['errors']['l_username'] = 'Kullanıcı adı boş bırakılamaz.'
  elif not re.match('^[a-zA-Z0-9]{4,32}$', p.form.getvalue('l_username')):
    p['errors']['l_username'] = 'Kullanıcı adı 4-32 karakter uzunlukta, alfanumerik olmalı.'
      
  if not len(p.form.getvalue('l_password', '')):
    p['errors']['l_password'] = 'Parola boş bırakılamaz.'
  
  if not len(p['errors']):
    uid = p.login(p.form.getvalue('l_username'), p.form.getvalue('l_password'))
    if uid:
      p.template = 'login.done.tpl'
    else:
      p['errors']['l_password'] = 'Hatalı şifre ya da kullanıcı adı.'
      
def logout():
  p.logout()
  p.template = 'logout.tpl'

p.actions = {
            'default': index,
            'logout': logout,
            'login': login
            }

p.build()

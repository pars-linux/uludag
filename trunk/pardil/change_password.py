#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config

import re
import random
from pyonweb.libstring import *
from pyonweb.libdate import *
from pyonweb.mail import sendmail
from pyonweb.template import build_template

p = pardil_page()

p.name = 'pardil_change_password'
p.title = site_config['title']

def index():
  p['mode'] = 'code'
  p.template = 'change_password.tpl'

def code():
  p['mode'] = 'code'
  p.template = 'change_password.tpl'

  if 'post' not in p.form:
    return

  if not len(p.form.getvalue('c_username', '')):
    p['errors']['c_username'] = 'Kullanıcı adı boş bırakılamaz.'

  if not len(p.form.getvalue('c_email', '')):
    p['errors']['c_email'] = 'E-posta adresi boş bırakılamaz.'
  elif not re.match('^[A-Za-z0-9_\.-]+@([A-Za-z0-9]+(\-*[A-Za-z0-9]+)*\.)+[A-Za-z]{2,4}$', p.form.getvalue('c_email')):
    p['errors']['c_email'] = 'E-posta adresi geçerli formatta olmalı.'

  if not len(p['errors']):
    q = """SELECT uid
           FROM users
           WHERE
             email="%s" AND
             username="%s"
        """ % (p.db.escape(p.form.getvalue('c_email')), \
               p.db.escape(p.form.getvalue('c_username')))
    uid = p.db.scalar_query(q)
    if not uid:
      p['errors']['c_email'] = 'Hatalı e-posta adresi ya da kullanıcı adı.'
    else:
      acode = pass_hash(str(random.random()))
      list = {
              'uid': uid,
              'code': acode,
              'timeB': sql_datetime(now())
              }
      p.db.insert('users_passcodes', list)
      
      # E-posta gönder
      t = "Pardil - Şifre Değiştirme Kodu"
      list = {
              'link': site_config['url'] + 'change_password.py?action=change',
              'code': acode,
              'time': num2str(site_config['activation_timeout'])
              }
      b = build_template(site_config['path'] + 'templates/email/change_password.tpl', list)
      sendmail(site_config['mail'], p.form.getvalue('c_email'), t, b)

      p['time'] = num2str(site_config['activation_timeout'])
      p['mode'] = 'change'
      
def change():
  p['mode'] = 'change'
  p.template = 'change_password.tpl'

  if 'post' not in p.form:
    return

  if not len(p.form.getvalue('c_password', '')) or not len(p.form.getvalue('c_password2', '')):
    p['errors']['c_password'] = 'Parola boş bırakılamaz.'
  elif p.form.getvalue('c_password') != p.form.getvalue('c_password2'):
    p['errors']['c_password'] = 'İki parola, birbiriyle aynı olmalı.'
  elif not re.match('^.{6,10}$', p.form.getvalue('c_password')):
    p['errors']['c_password'] = 'Parola en az 6, en fazla 10 karakter uzunluğunda olmalı.'

  if not len(p.form.getvalue('c_code', '')):
    p['errors']['c_code'] = 'Şifre değiştirme kodu boş bırakılamaz.'

  if not len(p['errors']):
    q = """SELECT uid
           FROM users_passcodes
           WHERE code="%s"
        """ % (p.db.escape(p.form.getvalue('c_code')))
    uid = p.db.scalar_query(q)
    if not uid:
      p['errors']['c_code'] = 'Geçersiz kod.'
    else:
      q = """UPDATE users
             SET password="%s"
             WHERE uid=%s
          """ % (p.db.escape(pass_hash(p.form.getvalue('c_password'))), uid)
      p.db.query_com(q)
      q = """DELETE
             FROM users_passcodes
             WHERE uid=%s
          """ % (uid)
      p.db.query_com(q)
      p['mode'] = 'done'


p.actions = {
             'default': index,
             'change': change,
             'code': code
             }

p.build()

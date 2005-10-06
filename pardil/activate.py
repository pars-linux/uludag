#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config

p = pardil_page()

p.name = 'pardil_activate'
p.title = site_config['title']

def index():
  if len(p.form.getvalue('code', '')) == 32:
    q = """SELECT
             username, password, email
           FROM users_pending
           WHERE code=%s"""
    row = p.db.row_query(q, p.form.getvalue('code'))

    if row:
      # Üye kaydı yap...
      list = {
              'username': row[0],
              'password': row[1],
              'email': row[2]
              }
      uid = p.db.insert('users', list)

      # "Kullanıcılar" grubuna ekle
      # Kullanıcılar grubu silinemez bir gruptur ve numarası 2'dir
      list = {
              'uid': uid,
              'gid': 2
              }
      p.db.insert('rel_groups', list)

      # "Users - Pending" tablosundan sil
      q = """DELETE
             FROM users_pending
             WHERE code=%s"""
      p.db.query_com(q, p.form.getvalue('code'))

      p.template = 'activate.tpl'
    else:
      p.http.redirect('error.py?tag=wrong_activation_code')
  else:
    p.http.redirect('error.py?tag=wrong_activation_code')
    
p.actions = {'default': index}

p.build()

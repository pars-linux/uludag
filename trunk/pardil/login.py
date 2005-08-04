from cfg_main import site_config

from lib_cheetah import build_page
from lib_mysql import mysql_db
from lib_std import pass_hash

from mod_python import Session

import re
import md5

def index(req):
  # Veritabanı bağlantısı kur.
  db = mysql_db(site_config['db_host'], site_config['db_name'], site_config['db_user'], site_config['db_pass'])

  # Oturum yoksa yarat, varsa bilgileri yükle.
  sess = Session.Session(req)
  if not sess.is_new():
    sess.load()

  # Tema motoruna gönderilecek değişken sözlüğünü oluştur.
  data = {}
  data['site_title'] = site_config['title']
  data['site_path'] = site_config['path']

  data['errors'] = {}
  data['status'] = ''
  data['posted_values'] = {}

  # Form gönderildiyse...
  if req.form.has_key('login'):

    # Gönderilen verileri data['posted_values'] içine aktar.
    for i in req.form.keys():
      data['posted_values'][i] = req.form[i]

    # Kullanıcı adını kontrol et.
    if not len(req.form['l_username']):
      data['errors']['l_username'] = 'Kullanıcı adı boş bırakılamaz.'
    elif not re.match('^[a-zA-Z0-9]{4,32}$', req.form['l_username']):
      data['errors']['l_username'] = 'Kullanıcı adı 4-32 karakter uzunlukta, alfanumerik olmalı.'
    elif not db.scalar_query('SELECT Count(*) FROM users WHERE username="%s" AND password="%s"' % (db.escape(req.form['l_username']), db.escape(pass_hash(req.form['l_password'])))):
      data['errors']['l_password'] = 'Hatalı şifre ya da kullanıcı adı.'

    # Hiç hata yoksa...
    if not len(data['errors']):

      # İşlem durumunu "bitti" olarak belirle
      data['status'] = 'done'
      
  # Sayfayı derle.
  return build_page(site_config['path'] + 'templates/login.tpl', data)

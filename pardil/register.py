from cfg_main import site_config

from lib_cheetah import build_page
from lib_mysql import mysql_db

from mod_python import Session

import re

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
  data['posted_values'] = {}

  # Form gönderildiyse...
  if req.form.has_key('register'):

    # Gönderilen verileri data['posted_values'] içine aktar.
    for i in req.form.keys():
      data['posted_values'][i] = req.form[i]

    # Kullanıcı adını kontrol et.
    if not len(req.form['r_username']):
      data['errors']['r_username'] = 'Kullanıcı adı boş bırakılamaz.'
    elif not re.match('^[a-zA-Z0-9]{4,32}$', req.form['r_username']):
      data['errors']['r_username'] = 'Kullanıcı adı 4-32 karakter uzunlukta, alfanumerik olmalı.'
    # TODO:
    # Aynı isimde kullanıcı olup olmadığını kontrol et.
    
    # E-posta adresini kontrol et.
    if not len(req.form['r_email']):
      data['errors']['r_email'] = 'E-posta adresi boş bırakılamaz.'
    # TODO:
    # Aynı e-posta adresine sahip kullanıcı olup olmadığını kontrol et.
    # E-posta adresi formatına uyup uymadığını kontrol et.
      
    # Parolayı kontrol et.
    if not len(req.form['r_password']):
      data['errors']['r_password'] = 'Parola boş bırakılamaz.'
    elif req.form['r_password'] != req.form['r_password2']:
      data['errors']['r_password'] = 'İki parola, birbiriyle aynı olmalı.'
    elif not re.match('^.{6}$', req.form['r_password']):
      data['errors']['r_password'] = 'Parola en az 6 karakter uzunlukta olmalı.'
      
    # İsmi kontrol et.
    if not len(req.form['r_firstname']):
      data['errors']['r_firstname'] = 'İsim boş bırakılamaz.'
      
    # Soyismi kontrol et.
    if not len(req.form['r_lastname']):
      data['errors']['r_lastname'] = 'Soyisim boş bırakılamaz.'

    # Hiç hata yoksa...
    if not len(data['errors']):
      # Veritabanına kayıt yap...
      return "Eğer kod eksik olmasaydı, kaydınız yapılacaktı..."

  # Sayfayı derle.
  return build_page(site_config['path'] + 'templates/register.tpl', data)

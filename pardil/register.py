from cfg_main import site_config

from lib_cheetah import build_page
from lib_mysql import mysql_db
from lib_std import pass_hash, page_init

from mod_python import Session

import re

def index(req):
  # Veritabanı bağlantısı kur, oturum aç, template bilgilerini yükle
  db, sess, data = page_init(req)

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
    elif db.scalar_query('SELECT Count(*) FROM users WHERE username="%s"' % (db.escape(req.form['r_username']))) > 0:
      data['errors']['r_username'] = 'Kullanıcı adı başkası tarafından kullanılıyor.'
    
    # E-posta adresini kontrol et.
    if not len(req.form['r_email']):
      data['errors']['r_email'] = 'E-posta adresi boş bırakılamaz.'
    elif not re.match('^[a-z0-9_\.-]+@([a-z0-9]+(\-*[a-z0-9]+)*\.)+[a-z]{2,4}$', req.form['r_email']):
      data['errors']['r_email'] = 'E-posta adresi geçerli formatta olmalı.'
    elif db.scalar_query('SELECT Count(*) FROM users WHERE email="%s"' % (db.escape(req.form['r_email']))) > 0:
      data['errors']['r_email'] = 'E-posta adresi başkası tarafından kullanılıyor.'
      
    # Parolayı kontrol et.
    if not len(req.form['r_password']):
      data['errors']['r_password'] = 'Parola boş bırakılamaz.'
    elif req.form['r_password'] != req.form['r_password2']:
      data['errors']['r_password'] = 'İki parola, birbiriyle aynı olmalı.'
    elif not re.match('^.{6}$', req.form['r_password']):
      data['errors']['r_password'] = 'Parola en az 6 karakter uzunlukta olmalı.'
      
    """
    # İsmi kontrol et.
    if not len(req.form['r_firstname']):
      data['errors']['r_firstname'] = 'İsim boş bırakılamaz.'
      
    # Soyismi kontrol et.
    if not len(req.form['r_lastname']):
      data['errors']['r_lastname'] = 'Soyisim boş bırakılamaz.'
    """

    # Hiç hata yoksa...
    if not len(data['errors']):

      # Veritabanına kayıt yap...
      insert_list = {'username': req.form['r_username'], 'password': pass_hash(req.form['r_password']), 'email': req.form['r_email']}
      db.query_com(db.insert('users', insert_list))

      # İşlem durumunu "bitti" olarak belirle
      data['status'] = 'done'
      
  # Sayfayı derle.
  return build_page(site_config['path'] + 'templates/register.tpl', data)

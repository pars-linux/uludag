from cfg_main import site_config

from lib_cheetah import build_page
from lib_mysql import mysql_db

from mod_python import Session

def index(req):
  # Veritabanı bağlantısı kur.
  db = mysql_db(site_config['db_host'], site_config['db_name'], site_config['db_user'], site_config['db_pass'])

  # Tema motoruna gönderilecek değişken sözlüğünü oluştur.
  data = {}
  data['site_title'] = site_config['title']
  data['site_path'] = site_config['path']

  data['errors'] = {}
  data['status'] = ''
  data['posted_values'] = {}
  data['session'] = {}

  # Oturum yoksa yarat, varsa bilgileri yükle.
  sess = Session.Session(req)
  if not sess.is_new():
    sess.load()
    for i in sess.keys():
      data['session'][i] = sess[i]

  # Oturum bilgilerini kaydet.
  sess.save()

  # Sayfayı derle.
  return build_page(site_config['path'] + 'templates/index.tpl', data)

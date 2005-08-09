from cfg_main import site_config
from lib_cheetah import build_page
from lib_std import page_init

def index(req):
  # Veritabanı bağlantısı kur, oturum aç, template bilgilerini yükle
  db, sess, data = page_init(req)
  
  # Oturum bilgilerini kaydet.
  sess.save()

  # Sayfayı derle.
  return build_page(site_config['path'] + 'templates/index.tpl', data)

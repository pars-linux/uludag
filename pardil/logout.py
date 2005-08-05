from cfg_main import site_config

from lib_cheetah import build_page

from mod_python import Session

def index(req):

  # Oturum bilgilerini yoket.
  sess = Session.Session(req)
  sess.delete()

  # Tema motoruna gönderilecek değişken sözlüğünü oluştur.
  data = {}
  data['site_title'] = site_config['title']
  data['site_path'] = site_config['path']

  data['errors'] = {}
  data['status'] = ''
  data['posted_values'] = {}
  data['session'] = {}

  # Sayfayı derle.
  return build_page(site_config['path'] + 'templates/logout.tpl', data)

from lib_cheetah import build_page
from cfg_main import site_config

def index(req):
  data = {}
  data['site_title'] = site_config['title']
  return build_page(site_config['path'] + 'templates/index.tpl', data)

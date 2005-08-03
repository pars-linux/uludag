from cfg_main import site_config

from lib_cheetah import build_page
from lib_mysql import mysql_db

def index(req):
  db = mysql_db(site_config['db_host'], site_config['db_name'], site_config['db_user'], site_config['db_pass'])

  data = {}
  data['site_title'] = site_config['title']
  data['site_path'] = site_config['path']


  data['test'] = db.scalar_query('SELECT startup FROM proposals WHERE pid=1')
  data['test'] = data['test'].strftime('%Y-%m-%d')
  
  return build_page(site_config['path'] + 'templates/index.tpl', data)

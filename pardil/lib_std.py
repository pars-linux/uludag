from cfg_main import site_config
from lib_mysql import mysql_db
from mod_python import Session
from lib_cheetah import build_page
import md5
import time

def pass_hash(s):
  hash = md5.new(s).hexdigest()
  hash = md5.new(s + hash[2:]).hexdigest()
  return hash

def page_init(req):
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

  return [db, sess, data]

def op_access(d, uid, aname):
  str_q = """SELECT Count(*)
  FROM rel_rights
    INNER JOIN rights ON rights.rid=rel_rights.rid
    INNER JOIN rel_groups ON rel_groups.gid=rel_rights.gid
    INNER JOIN users ON users.uid=rel_groups.uid
  WHERE
    rel_rights.timeB <= %T AND %T <= rel_rights.timeE AND
    rel_groups.timeB <= %T AND %T <= rel_groups.timeE AND
    users.uid=%d AND rights.keyword="%s"
  """.replace('%T', time.strftime('%Y-%m-%d'))

  return d.scalar_query(str_q % (int(uid), aname))
  
def is_maintainer(d, uid, pid):
  str_q = """SELECT Count(*)
  FROM rel_maintainers
  WHERE
    rel_maintainers.timeB <= %T AND %T <= rel_maintainers.timeE AND
    rel_maintainers.uid=%d AND rel_maintainers.pid=%d
  """.replace('%T', time.strftime('%Y-%m-%d'))

  return d.scalar_query(str_q % (int(uid), int(pid)))

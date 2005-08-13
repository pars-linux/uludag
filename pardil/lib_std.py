from cfg_main import site_config
from lib_mysql import mysql_db
from lib_cookie import cookie
from lib_date import *

def page_init():
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

  # Oturum varsa bilgileri yükle.
  ck = cookie()
  if ck.get('sid'):
    row = db.row_query('SELECT users.uid, users.username FROM sessions INNER JOIN users ON users.uid = sessions.uid WHERE sessions.sid="%s"' % (db.escape(ck.get('sid'))))
    if row:
      data['session']['sid'] = ck.get('sid')
      data['session']['uid'] = int(row[0])
      data['session']['username'] = row[1]

      # Oturum zaman bilgisini güncelle
      db.query_com('UPDATE sessions SET timeB=%d WHERE sid="%s"' % (now(), db.escape(ck.get('sid'))))

      # Çerez bilgisini güncelle
      ck.set('sid', data['session']['sid'])
      ck.save()

  # Süresi geçen oturumları yoket
  db.query_com('DELETE FROM sessions WHERE %d-timeB > %s' % (now(), 1800))

  return [db, ck, data]

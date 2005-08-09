from cfg_main import site_config

from lib_cheetah import build_page
from lib_mysql import mysql_db
from lib_std import *

from mod_python import Session, util

import re

def index(req):
  # Veritabanı bağlantısı kur, oturum aç, template bilgilerini yükle
  db, sess, data = page_init(req)

  data['revision'] = 0

  if not data['session'].has_key('uid'):
    util.redirect(req, 'error.py?tag=login_required')

  if not req.form.has_key('pid'):
    # Yeni öneri
    # Öneri ekleme hakkı olması yeterli.
    if not op_access(db, data['session']['uid'], 'proposals_add'):
      util.redirect(req, 'error.py?tag=not_in_authorized_group')
  else:
    # Öneriyi düzenleme, ya da yeni sürüm ekleme
    # Öneri sorumlusu olma ve öneri ekleme hakkı olması gerekli.
    if not op_access(db, data['session']['uid'], 'proposals_add') or not is_maintainer(db, data['session']['uid'], req.form['pid']):
      util.redirect(req, 'error.py?tag=not_maintainer')
    else:
      data['revision'] = 1
      data['pid'] = int(req.form['pid'])

      if req.form.has_key('version'):
        data['version'] = req.form['version']
      else:
        data['version'] = db.scalar_query('SELECT version FROM proposals_versions WHERE pid=%d ORDER BY vid DESC LIMIT 1' % (data['pid']))

      row = db.row_query('SELECT version, title, content FROM proposals_versions WHERE pid=%d AND version="%s"' % (data['pid'], db.escape(data['version'])))

      data['posted_values']['p_version'] = row[0]
      data['posted_values']['p_title'] = row[1]
      data['posted_values']['p_content'] = row[2]

  # Form gönderildiyse...
  if req.form.has_key('new_proposal'):

    # Gönderilen verileri data['posted_values'] içine aktar.
    for i in req.form.keys():
      data['posted_values'][i] = req.form[i]

    # Hata denetimi

    if not len(req.form['p_title']):
      data['errors']['p_title'] = 'Başlık boş bırakılamaz.'
    
    if data['revision']:
      pass
    # Hiç hata yoksa...
    if not len(data['errors']):

      # Veritabanına kayıt yap...
      #insert_list = {}
      #db.query_com(db.insert('users', insert_list))

      # İşlem durumunu "bitti" olarak belirle
      data['status'] = 'done'
      
  # Sayfayı derle.
  return build_page(site_config['path'] + 'templates/new_proposal.tpl', data)

#!/usr/bin/python
from cfg_main import site_config
from lib_cheetah import build_page
from lib_std import page_init

import cgi

def index():
  # Veritabanı bağlantısı kur, oturum aç, template bilgilerini yükle
  db, cookie, data = page_init()

  form = cgi.FieldStorage()

  #if form.has_key('pid') and form.has_key('version'):
  try:
    pid = int(form.getvalue('pid'))
    version = form.getvalue('version')
  except:
    data['status'] = 'error'

  if pid and version:
    row = db.row_query('SELECT proposals.pid, proposals_versions.version, proposals_versions.title, proposals_versions.content FROM proposals INNER JOIN proposals_versions ON proposals.pid=proposals_versions.pid WHERE proposals.pid=%d AND proposals_versions.version="%s"' % (pid, version))

  if row:
    data['proposal'] = {}
    data['proposal']['pid'] = row[0]
    data['proposal']['version'] = row[1]
    data['proposal']['title'] = row[2]

    # FIXME:
    # Öneri içeriğinin hangi formatta kayıt edileceğine henüz karar vermedim.
    data['proposal']['content'] = row[3].replace("\n", "<br/>")

    # Sürüm geçmişi
    data['versions'] = db.query('SELECT proposals_versions.version FROM proposals_versions WHERE pid=%d ORDER BY vid DESC' % (pid))
    
    # Yorumlar
    data['comments'] = db.query('SELECT proposals_comments.cid, users.username, proposals_comments.title, proposals_comments.content FROM proposals_comments INNER JOIN users ON users.uid=proposals_comments.uid WHERE proposals_comments.pid=%d' % (pid))

  else:
    data['status'] = 'error'

  # Sayfayı derle.
  build_page(site_config['path'] + 'templates/viewproposal.tpl', data)

index()

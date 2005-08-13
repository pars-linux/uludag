#!/usr/bin/python
from cfg_main import site_config
from lib_cheetah import build_page
from lib_std import page_init
import sys

def index():
  # Veritabanı bağlantısı kur, oturum aç, template bilgilerini yükle
  db, cookie, data = page_init()


  # Önerilerin en yüksek sürüm numarasına sahip olanlarını listele

  versions = []
  for row in db.query('SELECT max(vid) FROM proposals_versions GROUP BY pid'):
    versions.append(str(row[0]))

  data['proposals'] = []
  if len(versions):
    list = db.query('SELECT proposals.pid AS _pid, proposals_versions.version, proposals_versions.title FROM proposals INNER JOIN proposals_versions ON proposals.pid=proposals_versions.pid WHERE proposals_versions.vid IN (%s) ORDER BY proposals.pid ASC' % (','.join(versions)))
    for i in list:
      data['proposals'].append({'pid': i[0], 'version': i[1], 'title': i[2]})

  # Sayfayı derle.
  build_page(site_config['path'] + 'templates/proposals.tpl', data)


index()

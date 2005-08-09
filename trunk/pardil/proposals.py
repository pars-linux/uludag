from cfg_main import site_config
from lib_cheetah import build_page
from lib_std import page_init

def index(req):
  # Veritabanı bağlantısı kur, oturum aç, template bilgilerini yükle
  db, sess, data = page_init(req)

  data['proposals'] = []

  # Önerilerin en yüksek sürüm numarasına sahip olanlarını listele
  list = db.query('SELECT proposals.pid AS _pid, proposals_versions.version, proposals_versions.title FROM proposals INNER JOIN proposals_versions ON proposals.pid=proposals_versions.pid WHERE proposals_versions.version = (SELECT MAX(version) FROM proposals_versions WHERE pid=_pid)')
  for i in list:
    data['proposals'].append({'pid': i[0], 'version': i[1], 'title': i[2]})
  
  # Oturum bilgilerini kaydet.
  sess.save()

  # Sayfayı derle.
  return build_page(site_config['path'] + 'templates/proposals.tpl', data)

from cfg_main import site_config
from lib_cheetah import build_page
from lib_std import page_init

def index(req):
  # Veritabanı bağlantısı kur, oturum aç, template bilgilerini yükle
  db, sess, data = page_init(req)

  if req.form.has_key('no') and req.form.has_key('version'):
    pid = int(req.form['no'])
    version = req.form['version']
  else:
    data['status'] = 'error'

  # FIXME:
  # Öneriyi gönderen kişinin adı yazılacak.
  row = db.row_query('SELECT proposals.pid, proposals_versions.version, proposals_versions.title, proposals_versions.content FROM proposals INNER JOIN proposals_versions ON proposals.pid=proposals_versions.pid WHERE proposals.pid=%d AND proposals_versions.version=%s' % (pid, version))

  if not row:
    data['status'] = 'error'
  else:
    data['proposal'] = {}
    data['proposal']['pid'] = row[0]
    data['proposal']['version'] = row[1]
    data['proposal']['title'] = row[2]

    # FIXME:
    # Öneri içeriğinin hangi formatta kayıt edileceğine henüz karar vermedim.
    data['proposal']['content'] = row[3].replace("\n", "<br/>")

    # TODO: 
    # Sürüm geçmişi eklenecek.
  
  # Oturum bilgilerini kaydet.
  sess.save()

  # Sayfayı derle.
  return build_page(site_config['path'] + 'templates/viewproposal.tpl', data)

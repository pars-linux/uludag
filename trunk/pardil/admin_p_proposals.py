#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config
from pyonweb.libstring import *
from pyonweb.libdate import *
import re
from math import ceil

p = pardil_page()

p.name = 'pardil_admin_p_proposals'
p.title = site_config['title']

# OLMAZSA OLMAZ!
if 'sid' not in p['session']:
  p.http.redirect('error.py?tag=login_required')
if 'administrate_pending' not in p['acl'] and not p.site_admin():
  p.http.redirect('error.py?tag=not_in_authorized_group')
# OLMAZSA OLMAZ!

# Sayfalama
p['pag_now'] = int(p.form.getvalue('start', '0'))
p['pag_total'] = ceil(float(p.db.scalar_query("SELECT Count(*) FROM proposals_pending")) / float(site_config['pag_perpage']))

def index():
  p['pending'] = []
  q = """SELECT
           tpid, title, timeB
         FROM proposals_pending
         ORDER BY tpid ASC
         LIMIT %d, %d
      """ % (p['pag_now'] * site_config['pag_perpage'], site_config['pag_perpage'])
  list = p.db.query(q)
  for i in list:
    l = {
         'tpid': i[0],
         'title': i[1]
         }
    p['pending'].append(l)
  p.template = 'admin/pending_proposals.tpl'

def view():
  try:
    tpid = int(p.form.getvalue('tpid'))
  except:
    p.template = 'admin/pending_proposals.error.tpl'
    return

  if tpid:
    q = """SELECT
             users.uid,
             users.username,
             proposals_pending.title,
             proposals_pending.summary,
             proposals_pending.content,
             proposals_pending.timeB
           FROM proposals_pending
             INNER JOIN users
               ON users.uid = proposals_pending.uid
           WHERE
             tpid=%d
        """ % (tpid)
    row = p.db.row_query(q)

    if row:
      p['posted'] = {
                     'p_title': html_escape(row[2]),
                     'p_summary': html_escape(row[3]),
                     'p_content': html_escape(row[4]),
                     'p_tpid': tpid,
                     'p_uid': row[0],
                     'p_username': row[1],
                     'p_timeB': row[5]
                     }
    p.template = 'admin/pending_proposals.view.tpl'
 
def publish():
    
  if not len(p.form.getvalue('p_uid', '')):
    p['errors']['p_uid'] = 'Kullanıcı numarası belirtilmemiş.'
    
  if not len(p.form.getvalue('p_title', '')):
    p['errors']['p_title'] = 'Başlık boş bırakılamaz.'

  if not len(p.form.getvalue('p_summary', '')):
    p['errors']['p_summary'] = 'Özet boş bırakılamaz.'

  if not len(p.form.getvalue('p_content', '')):
    p['errors']['p_content'] = 'Öneri detayları boş bırakılamaz.'

  # Hiç hata yoksa...
  if not len(p['errors']):

    # Öneri hemen yayınlansın mı...
    version = '1.0.0'
      
    # Öneriler tablosuna ekle
    list = {
            'uid': p.form.getvalue('p_uid'),
            'startup': sql_datetime(now())
            }
    pid = p.db.insert('proposals', list)

    # İlk sürümü ekle
    list = {
            'pid': pid,
            'version': version,
            'title': p.form.getvalue('p_title'),
            'content': p.form.getvalue('p_content'),
            'timeB': sql_datetime(now()),
            'changelog': "İlk sürüm."
            }
    vid = p.db.insert('proposals_versions', list)
    
    if 'p_maintainer' in p.form:
      # Kişiyi öneri sorumlusu olarak ata
      list = {
              'uid': p.form.getvalue('p_uid'),
              'pid': pid
              }
      p.db.insert('rel_maintainers', list)
      
    p['pid'] = pid
    p['version'] = version

    # Bekleyen öneriyi yoket
    q = """DELETE
           FROM proposals_pending
           WHERE tpid = %d
        """ % (int(p.form.getvalue('p_tpid')))
    p.db.query_com(q)
    
    p.template = 'admin/pending_proposals.publish.tpl'

  else:
    p.template = 'admin/pending_proposals.view.tpl'

def delete():
  # Bekleyen öneriyi yoket
  q = """DELETE
         FROM proposals_pending
         WHERE tpid = %d
      """ % (int(p.form.getvalue('p_tpid')))
  p.db.query_com(q)
    
  p.template = 'admin/pending_proposals.delete.tpl'

p.actions = { 
             'default': index,
             'publish': publish,
             'delete': delete,
             'view': view
             }

p.build()

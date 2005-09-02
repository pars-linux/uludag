#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config
from pyonweb.libstring import *
from pyonweb.libdate import *
import re

p = pardil_page()

p.name = 'pardil_admin_p_proposals'
p.title = site_config['title']

# OLMAZSA OLMAZ!
if 'sid' not in p['session']:
  p.http.redirect('error.py?tag=login_required')
if not p.access('administrate'):
  p.http.redirect('error.py?tag=not_in_authorized_group')
# OLMAZSA OLMAZ!

def index():
  p['pending'] = []
  q = """SELECT
           tpid, title, timeB
         FROM proposals_pending
         ORDER BY tpid ASC
      """
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
             proposals_pending.purpose,
             proposals_pending.content,
             proposals_pending.solution,
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
                     'p_summary': nl2br(html_escape(row[3])),
                     'p_purpose': nl2br(html_escape(row[4])),
                     'p_content': nl2br(html_escape(row[5])),
                     'p_solution': nl2br(html_escape(row[6])),
                     'p_tpid': tpid,
                     'p_uid': row[0],
                     'p_username': row[1],
                     'p_timeB': row[7]
                     }
    p.template = 'admin/pending_proposals.view.tpl'
 
def publish():
    
  if not len(p.form.getvalue('uid', '')):
    p['errors']['uid'] = 'Kullanıcı numarası belirtilmemiş.'
    
  if not len(p.form.getvalue('p_title', '')):
    p['errors']['p_title'] = 'Başlık boş bırakılamaz.'

  if not len(p.form.getvalue('p_summary', '')):
    p['errors']['p_summary'] = 'Özet boş bırakılamaz.'

  if not len(p.form.getvalue('p_purpose', '')):
    p['errors']['p_purpose'] = 'Amaç boş bırakılamaz.'
    
  if not len(p.form.getvalue('p_content', '')):
    p['errors']['p_content'] = 'Öneri detayları boş bırakılamaz.'

  if not len(p.form.getvalue('p_solution', '')):
    p['errors']['p_solution'] = 'Çözüm boş bırakılamaz.'

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
            'summary': p.form.getvalue('p_summary'),
            'purpose': p.form.getvalue('p_purpose'),
            'content': p.form.getvalue('p_content'),
            'solution': p.form.getvalue('p_solution'),
            'timeB': sql_datetime(now()),
            'changelog': p.form.getvalue('p_changelog')
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

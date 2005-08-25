#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config

from pyonweb.libstring import *
from lib_date import *

p = pardil_page()

p.name = 'pardil_viewproposals'
p.title = site_config['title']

def index():
  pid = int(p.form['pid'])
  version = p.form['version']

  if pid and version:
    q = """SELECT
             proposals.pid,
             proposals_versions.version,
             proposals_versions.title,
             proposals_versions.summary,
             proposals_versions.purpose,
             proposals_versions.content,
             proposals_versions.solution
           FROM proposals
             INNER JOIN proposals_versions ON proposals.pid=proposals_versions.pid
           WHERE
             proposals.pid=%d AND
             proposals_versions.version="%s"
        """ % (pid, version)
    row = p.db.row_query(q)

    if row:
      p['proposal'] = {}
      p['proposal']['pid'] = row[0]
      p['proposal']['version'] = html_escape(row[1])
      p['proposal']['title'] = html_escape(row[2])

      # FIXME:
      # Öneri içeriğinin hangi formatta kayıt edileceğine henüz karar vermedim.
      p['proposal']['summary'] = nl2br(html_escape(row[3]))
      p['proposal']['purpose'] = nl2br(html_escape(row[4]))
      p['proposal']['content'] = nl2br(html_escape(row[5]))
      p['proposal']['solution'] = nl2br(html_escape(row[6]))

      # Sürüm geçmişi
      q = """SELECT proposals_versions.version
             FROM proposals_versions
             WHERE pid=%d
             ORDER BY vid DESC
          """ % (pid)
      rows = p.db.query(q)
      
      p['versions'] = []
      for i in rows:
        p['versions'].append(i[0])
    
      # Yorumlar
      q = """SELECT
               proposals_comments.cid,
               users.username,
               proposals_comments.content
             FROM proposals_comments
               INNER JOIN users ON users.uid=proposals_comments.uid
             WHERE proposals_comments.pid=%d
          """ % (pid)
      rows = p.db.query(q)

      p['comments'] = []
      for i in rows:
        p['comments'].append({'user': i[1], 'comment': nl2br(html_escape(i[2]))})

      # Yorum ekleme
      if p.access('proposals_comment'):
        p['may_comment'] = 1
      else:
        p['may_comment'] = 0

      p.template = site_config['path'] + 'templates/viewproposal.tpl'
    else:
     p.template = site_config['path'] + 'templates/viewproposal.error.tpl'
  else:
    p.template = site_config['path'] + 'templates/viewproposal.error.tpl'

def comment():
  if 'sid' not in p['session']:
    p.http.redirect('error.py?tag=not_logged_in')
  if not p.access('proposals_comment'):
    p.http.redirect('error.py?tag=not_in_authorized_group')

  insert_list = {'pid': p.form['pid'],
                 'uid': p['session']['uid'],
                 'content': p.form['p_comment'],
                 'timeB': sql_datetime(now())}
  p.db.insert('proposals_comments', insert_list)

  p.http.redirect('viewproposal.py?pid=%s&version=%s' % (p.form['pid'], p.form['version']))

p.actions = {'default': index,
             'comment': comment}

p.build()

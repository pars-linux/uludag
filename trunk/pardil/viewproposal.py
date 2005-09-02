#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config

from pyonweb.libstring import *
from pyonweb.libdate import *

p = pardil_page()

p.name = 'pardil_viewproposals'
p.title = site_config['title']

def index():
  try:
    pid = int(p.form.getvalue('pid'))
    version = p.form.getvalue('version')
  except:
    p.template = 'viewproposal.error.tpl'
    return

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
             INNER JOIN proposals_versions
               ON proposals.pid=proposals_versions.pid
           WHERE
             proposals.pid=%d AND
             proposals_versions.version="%s"
        """ % (pid, version)
    row = p.db.row_query(q)

    if row:
      p['proposal'] = {
                       'pid': row[0],
                       'version': html_escape(row[1]),
                       'title': html_escape(row[2]),
                       'summary': nl2br(html_escape(row[3])),
                       'purpose': nl2br(html_escape(row[4])),
                       'content': nl2br(html_escape(row[5])),
                       'solution': nl2br(html_escape(row[6]))
                       }

      # Sürüm geçmişi
      q = """SELECT proposals_versions.version
             FROM proposals_versions
             WHERE
               pid=%d
             ORDER BY vid DESC
          """ % (pid)
      rows = p.db.query(q)
      
      p['versions'] = []
      for i in rows:
        p['versions'].append(i[0])

      # Sorumlular
      q = """SELECT
               users.uid,
               users.username
             FROM users
               INNER JOIN rel_maintainers
                 ON rel_maintainers.uid=users.uid
             WHERE
               rel_maintainers.pid=%d
             ORDER BY users.username ASC
          """ % (pid)
      rows = p.db.query(q)

      p['is_maintainer'] = 0
      p['maintainers'] = []
      for i in rows:
        if 'uid' in p['session'] and p['session']['uid'] == i[0]:
          p['is_maintainer'] = 1
        l = {
             'uid': i[0],
             'user': i[1]
             }
        p['maintainers'].append(l)
    
      # Yorumlar
      q = """SELECT
               proposals_comments.cid,
               users.username,
               proposals_comments.content
             FROM proposals_comments
               INNER JOIN users
                 ON users.uid=proposals_comments.uid
             WHERE proposals_comments.pid=%d
          """ % (pid)
      rows = p.db.query(q)

      p['comments'] = []
      for i in rows:
        l = {
             'user': i[1],
             'comment': nl2br(html_escape(i[2]))
             }
        p['comments'].append(l)

      # Yorum ekleme
      if p.access('proposals_comment'):
        p['may_comment'] = 1
      else:
        p['may_comment'] = 0

      p.template = 'viewproposal.tpl'
    else:
      p.template = 'viewproposal.error.tpl'
  else:
    p.template = 'viewproposal.error.tpl'

def comment():
  if 'sid' not in p['session']:
    p.http.redirect('error.py?tag=not_logged_in')
  if not p.access('proposals_comment'):
    p.http.redirect('error.py?tag=not_in_authorized_group')

  if not len(p.form.getvalue('p_comment', '')):
    p['errors']['p_comment'] = 'Yorum yazmadınız.'

  if not len(p.form.getvalue('pid', '')):
    p['errors']['p_comment'] = 'Hangi öneriye yorum yapıldığı belirsiz.'

  if not len(p['errors']):
    list = {
            'pid': p.form.getvalue('pid'),
            'uid': p['session']['uid'],
            'content': p.form.getvalue('p_comment'),
            'timeB': sql_datetime(now())
            }
    p.db.insert('proposals_comments', list)

    p.http.redirect('viewproposal.py?pid=%s&version=%s' % (p.form.getvalue('pid'), p.form.getvalue('version')))
  else:
    index()

p.actions = {
             'default': index,
             'comment': comment
             }

p.build()

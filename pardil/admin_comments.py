#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config
import re
from math import ceil

p = pardil_page()

p.name = 'pardil_admin_comments'
p.title = site_config['title']

# OLMAZSA OLMAZ!
if 'sid' not in p['session']:
  p.http.redirect('error.py?tag=login_required')
if not p.access('administrate_comments') and \
   not p.site_admin():
  p.http.redirect('error.py?tag=not_in_authorized_group')
# OLMAZSA OLMAZ!

# Sayfalama
p['pag_now'] = int(p.form.getvalue('start', '0'))
p['pag_total'] = ceil(float(p.db.scalar_query("SELECT Count(*) FROM proposals")) / float(site_config['pag_perpage']))

def index():
  versions = []
  q = """SELECT max(vid)
         FROM proposals_versions
         GROUP BY pid
      """
  for row in p.db.query(q):
    versions.append(str(row[0]))

  p['proposals'] = []
  if len(versions):
    q = """SELECT
             proposals.pid AS _pid,
             proposals_versions.title
           FROM proposals
             INNER JOIN proposals_versions
               ON proposals.pid=proposals_versions.pid
           WHERE proposals_versions.vid IN (%s)
           ORDER BY proposals.pid ASC
           LIMIT %d, %d
        """ % (','.join(versions), p['pag_now'] * site_config['pag_perpage'], site_config['pag_perpage'])
    list = p.db.query(q)
    for i in list:
      l = {
           'pid': i[0],
           'title': i[1]
           }
      p['proposals'].append(l)
  p.template = 'admin/comments.tpl'
  
def comments():
  try:
    p['pid'] = int(p.form.getvalue('pid'))
  except:
    p.template = 'admin/comments.error.tpl'
    return

  p['comments'] = []
  q = """SELECT
           proposals_comments.cid,
           proposals_comments.timeB,
           proposals_comments.content,
           users.username
         FROM proposals_comments
           INNER JOIN users
             ON users.uid=proposals_comments.uid
         WHERE proposals_comments.pid = %d
         ORDER BY proposals_comments.timeB ASC
      """ % (p['pid'])
  list = p.db.query(q)
  for i in list:
    p['comments'].append({'cid': i[0],
                          'date': i[1],
                          'content': i[2],
                          'user': i[3]})

  p.template = 'admin/comments.list.tpl'

def delete():
  try:
    p['cid'] = int(p.form.getvalue('cid'))
    p['pid'] = int(p.form.getvalue('pid'))
  except:
    p.template = 'admin/comments.error.tpl'
    return

  q = """SELECT users.username
         FROM users
           INNER JOIN proposals_comments
             ON proposals_comments.uid = users.uid
         WHERE cid=%d
      """ % (p['cid'])
  p['username'] = p.db.scalar_query(q)

  if not p['username']:
    p.template = 'admin/comments.error.tpl'
  else:
    if 'confirm' in p.form:
      if p.form.getvalue('confirm', '') == 'yes':
        q = """DELETE FROM proposals_comments
               WHERE cid=%d
            """ % (p['cid'])
        p.db.query_com(q)
        p.template = 'admin/comments.delete_yes.tpl'
      else:
        p.template = 'admin/comments.delete_no.tpl'
    else:
      p.template = 'admin/comments.delete_confirm.tpl'

p.actions = { 
             'default': index,
             'comments': comments,
             'delete': delete
             }

p.build()

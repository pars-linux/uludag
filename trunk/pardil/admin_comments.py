#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config

p = pardil_page()

p.name = 'pardil_index'
p.title = site_config['title']

# OLMAZSA OLMAZ!
if 'sid' not in p['session']:
  p.http.redirect('error.py?tag=login_required')
if not p.access('administrate'):
  p.http.redirect('error.py?tag=not_in_authorized_group')
# OLMAZSA OLMAZ!

def index():
  versions = []
  for row in p.db.query('SELECT max(vid) FROM proposals_versions GROUP BY pid'):
    versions.append(str(row[0]))

  p['proposals'] = []
  if len(versions):
    q = """SELECT
             proposals.pid AS _pid,
             proposals_versions.title
           FROM proposals
             INNER JOIN proposals_versions ON proposals.pid=proposals_versions.pid
           WHERE proposals_versions.vid IN (%s)
           ORDER BY proposals.pid ASC
        """ % (','.join(versions))
    list = p.db.query(q)
    for i in list:
      p['proposals'].append({'pid': i[0],
                             'title': i[1]})
  p.template = site_config['path'] + 'templates/admin/comments.tpl'
  
def comments():
  p['pid'] = int(p.form['pid'])
  p['comments'] = []
  q = """SELECT
           proposals_comments.cid,
           proposals_comments.timeB,
           proposals_comments.content,
           users.username
         FROM proposals_comments
           INNER JOIN users ON users.uid=proposals_comments.uid
         WHERE proposals_comments.pid = %d
         ORDER BY proposals_comments.timeB ASC
      """ % (p['pid'])
  list = p.db.query(q)
  for i in list:
    p['comments'].append({'cid': i[0],
                          'date': i[1],
                          'content': i[2],
                          'user': i[3]})

  p.template = site_config['path'] + 'templates/admin/comments.list.tpl'

def delete():
  try:
    p['cid'] = int(p.form['cid'])
    p['pid'] = int(p.form['pid'])
  except:
    p.template = site_config['path'] + 'templates/admin/comments.error.tpl'
  else:
    q = """SELECT users.username
           FROM users
             INNER JOIN proposals_comments ON proposals_comments.uid = users.uid
           WHERE cid=%d
        """ % (p['cid'])
    p['username'] = p.db.scalar_query(q)
    if not p['username']:
      p.template = site_config['path'] + 'templates/admin/comments.error.tpl'
    else:
      if 'confirm' in p.form:
        if p.form['confirm'] == 'yes':
          p.db.query_com('DELETE FROM proposals_comments WHERE cid=%d' % (p['cid']))
          p.template = site_config['path'] + 'templates/admin/comments.delete_yes.tpl'
        else:
          p.template = site_config['path'] + 'templates/admin/comments.delete_no.tpl'
      else:
        p.template = site_config['path'] + 'templates/admin/comments.delete_confirm.tpl'

p.actions = {'default': index,
             'comments': comments,
             'delete': delete}

p.build()

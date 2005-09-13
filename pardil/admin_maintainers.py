#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config
from pyonweb.libdate import *
import re
from math import ceil

p = pardil_page()

p.name = 'pardil_admin_maintainers'
p.title = site_config['title']

# OLMAZSA OLMAZ!
if 'sid' not in p['session']:
  p.http.redirect('error.py?tag=login_required')
if 'administrate_maintainers' not in p['acl'] and not p.site_admin():
  p.http.redirect('error.py?tag=not_in_authorized_group')
# OLMAZSA OLMAZ!

# Sayfalama
p['pag_now'] = int(p.form.getvalue('start', '0'))
p['pag_total'] = ceil(float(p.db.scalar_query("SELECT Count(*) FROM rel_maintainers")) / float(site_config['pag_perpage']))

def index():
  versions = []
  q = """SELECT max(vid)
         FROM proposals_versions
         GROUP BY pid
      """
  for row in p.db.query(q):
    versions.append(str(row[0]))

  p['rel_maintainers'] = []
  p['proposals'] = []

  if len(versions):
    q = """SELECT
             rel_maintainers.relid,
             proposals.pid,
             proposals_versions.title,
             users.username
           FROM rel_maintainers
             INNER JOIN proposals
               ON proposals.pid = rel_maintainers.pid
             INNER JOIN proposals_versions
               ON proposals_versions.pid = proposals.pid
             INNER JOIN users
               ON users.uid = rel_maintainers.uid
             WHERE
               proposals_versions.vid IN (%s)
           ORDER BY proposals.pid, users.username ASC
           LIMIT %d, %d
        """ % (','.join(versions), p['pag_now'] * site_config['pag_perpage'], site_config['pag_perpage'])

    list = p.db.query(q)
    for i in list:
      l = {
           'relid': i[0],
           'pid': i[1],
           'proposal': i[2],
           'username': i[3]
           }
      p['rel_maintainers'].append(l)

    q = """SELECT
             proposals.pid AS _pid,
             proposals_versions.version,
             proposals_versions.title
           FROM proposals
             INNER JOIN proposals_versions
               ON proposals.pid=proposals_versions.pid
           WHERE
             proposals_versions.vid IN (%s)
           ORDER BY proposals.pid ASC
        """ % (','.join(versions))
    list = p.db.query(q)
    for i in list:
      l = {
           'pid': i[0],
           'version': i[1],
           'title': i[2]
           }
      p['proposals'].append(l)

  p['users'] = []
  q = """SELECT
           uid, username
         FROM users
         ORDER BY username ASC
      """
  list = p.db.query(q)
  for i in list:
    p['users'].append({'uid': i[0], 'username': i[1]})

  p.template = 'admin/maintainers.tpl'

def delete():
  try:
    p['relid'] = int(p.form.getvalue('relid'))
  except:
    p.template = 'admin/maintainers.error.tpl'
    return

  q1 = """SELECT pid
          FROM rel_maintainers
          WHERE relid=%d
       """ % (p['relid'])
  q2 = """SELECT
            users.username
          FROM users
            INNER JOIN rel_maintainers
              ON rel_maintainers.uid=users.uid
          WHERE rel_maintainers.relid=%d
       """ % (p['relid'])

  p['pid'] = p.db.scalar_query(q1)
  p['user'] = p.db.scalar_query(q2)
  if not p['pid'] or not p['user']:
    p.template = 'admin/maintainers.error.tpl'
  else:
    if 'confirm' in p.form:
      if p.form.getvalue('confirm', '') == 'yes':
        q = """DELETE FROM rel_maintainers
               WHERE relid=%d
            """ % (p['relid'])
        p.db.query_com(q)
        p.template = 'admin/maintainers.delete_yes.tpl'
      else:
        p.template = 'admin/maintainers.delete_no.tpl'
    else:
      p.template = 'admin/maintainers.delete_confirm.tpl'

def insert():
  try:
    uid = int(p.form.getvalue('m_user'))
    pid = int(p.form.getvalue('m_proposal'))
  except:
    p['errors']['m_user'] = 'Geçersiz kullanıcı numarası.'
  else:
    q1 = """SELECT Count(*)
            FROM users
            WHERE uid=%d
         """  % (uid)
    q2 = """SELECT Count(*)
            FROM proposals
            WHERE pid=%d
         """  % (pid)
    q3 = """SELECT Count(*)
            FROM rel_maintainers
            WHERE pid=%d AND uid=%d
         """ % (pid, uid)
    if p.db.scalar_query(q1) == 0:
      p['errors']['m_user'] = 'Geçersiz kullanıcı numarası.'
    elif p.db.scalar_query(q2) == 0:
      p['errors']['m_proposal'] = 'Geçersiz öneri numarası.'
    elif p.db.scalar_query(q3) > 0:
      p['errors']['m_user'] = 'Kullanıcı zaten bu önerinin sorumlusu.'
     
  if not len(p['errors']):
    p.template = 'admin/maintainers.insert.tpl'

    p['pid'] = pid

    q = """SELECT username
           FROM users
           WHERE uid=%d
        """ % (uid)
    p['user'] = p.db.scalar_query(q)

    list = {
            'pid': pid,
            'uid': uid
            }
    p['relid'] = p.db.insert('rel_maintainers', list)

  else:  
    p.template = 'admin/maintainers.tpl'
    index()

p.actions = {
             'default': index,
             'delete': delete,
             'insert': insert
             }

p.build()

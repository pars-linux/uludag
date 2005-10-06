#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config
import re
from math import ceil

p = pardil_page()

p.name = 'pardil_admin_usergroups'
p.title = site_config['title']

# OLMAZSA OLMAZ!
if 'sid' not in p['session']:
  p.http.redirect('error.py?tag=login_required')
if 'administrate_usergroups' not in p['acl'] and not p.site_admin():
  p.http.redirect('error.py?tag=not_in_authorized_group')
# OLMAZSA OLMAZ!

# Sayfalama
p['pag_now'] = int(p.form.getvalue('start', '0'))
p['pag_total'] = ceil(float(p.db.scalar_query("SELECT Count(*) FROM rel_groups")) / float(site_config['pag_perpage']))

def index():
  p['rel_groups'] = []
  q = """SELECT
           rel_groups.relid, groups.label, users.username
         FROM rel_groups
           INNER JOIN groups
             ON groups.gid=rel_groups.gid
           INNER JOIN users
             ON users.uid=rel_groups.uid
         ORDER BY groups.gid, users.username ASC
         LIMIT %d, %d
      """ % (p['pag_now'] * site_config['pag_perpage'], site_config['pag_perpage'])
  list = p.db.query(q)
  for i in list:
    l = {
         'relid': i[0],
         'group': i[1],
         'username': i[2]
         }
    p['rel_groups'].append(l)

  p['groups'] = []
  q = """SELECT
           gid, label
         FROM groups
         ORDER BY gid ASC"""
  list = p.db.query(q)
  for i in list:
    l = {
         'gid': i[0],
         'label': i[1]
         }
    p['groups'].append(l)

  p['users'] = []
  q = """SELECT
           uid, username
         FROM users
         ORDER BY username ASC"""
  list = p.db.query(q)
  for i in list:
    p['users'].append({'uid': i[0], 'username': i[1]})

  p.template = 'admin/usergroups.tpl'

def delete():
  try:
    p['relid'] = int(p.form.getvalue('relid'))
  except:
    p.template = 'admin/usergroups.error.tpl'
    return

  # 1. kullanıcı-grup kaydı silinemez :)
  if p['relid'] in [1]:
    p.template = 'admin/usergroups.error.tpl'
    return

  q1 = """SELECT
            groups.label
          FROM groups
            INNER JOIN rel_groups
             ON rel_groups.gid=groups.gid
          WHERE rel_groups.relid=%s"""
  q2 = """SELECT
            users.username
          FROM users
            INNER JOIN rel_groups
              ON rel_groups.uid=users.uid
          WHERE rel_groups.relid=%s"""

  p['group'] = p.db.scalar_query(q1, p['relid'])
  p['user'] = p.db.scalar_query(q2, p['relid'])
  if not p['group'] or not p['user']:
    p.template = 'admin/usergroups.error.tpl'
  else:
    if 'confirm' in p.form:
      if p.form.getvalue('confirm', '') == 'yes':
        q = """DELETE FROM rel_groups
               WHERE relid=%s"""
        p.db.query_com(q, p['relid'])
        p.template = 'admin/usergroups.delete_yes.tpl'
      else:
        p.template = 'admin/usergroups.delete_no.tpl'
    else:
      p.template = 'admin/usergroups.delete_confirm.tpl'

def insert():
  try:
    uid = int(p.form.getvalue('u_user'))
    gid = int(p.form.getvalue('u_group'))
  except:
    p['errors']['u_user'] = 'Geçersiz kullanıcı numarası.'
  else:
    q1 = """SELECT Count(*)
            FROM users
            WHERE uid=%s"""
    q2 = """SELECT Count(*)
            FROM groups
            WHERE gid=%s"""
    q3 = """SELECT Count(*)
            FROM rel_groups
            WHERE gid=%s AND uid=%s"""
    if p.db.scalar_query(q1, uid) == 0:
      p['errors']['u_user'] = 'Geçersiz kullanıcı numarası.'
    elif p.db.scalar_query(q2, gid) == 0:
      p['errors']['u_group'] = 'Geçersiz grup numarası.'
    elif p.db.scalar_query(q3, (gid, uid)) > 0:
      p['errors']['u_user'] = 'Kullanıcı zaten bu gruba dahil.'
     
  if not len(p['errors']):
    p.template = 'admin/usergroups.insert.tpl'

    q = """SELECT label
           FROM groups
           WHERE gid=%s"""
    p['group'] = p.db.scalar_query(q, gid)
    q = """SELECT username
           FROM users
           WHERE uid=%s"""
    p['user'] = p.db.scalar_query(q, uid)

    list = {
            'gid': gid,
            'uid': uid
            }
    p['relid'] = p.db.insert('rel_groups', list)

  else:  
    p.template = 'admin/usergroups.tpl'
    index()

p.actions = {
             'default': index,
             'delete': delete,
             'insert': insert
             }

p.build()

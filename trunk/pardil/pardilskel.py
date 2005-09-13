# -*- coding: utf-8 -*-

# Copyright (C) 2005, Bahadır Kandemir
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

from pyonweb.page import page
from pyonweb.cookie import cookie
from pyonweb.mysql import mysql
from pyonweb.http import http
from pyonweb.libstring import *
from pyonweb.libdate import *
from pyonweb.template import build_template

from cfg_main import site_config

import time
import md5
import sys

class pardil_page(page):

  def init(self):
    # DB
    self.db = mysql(site_config['db_host'],
                    site_config['db_name'],
                    site_config['db_user'],
                    site_config['db_pass'])
    
    # Cookie
    self.cookie = cookie()
    
    # HTTP Lib
    self.http = http()

    # Session
    self.init_session()

    # Remove expired sessions
    q = """DELETE
           FROM sessions
           WHERE unix_timestamp("%s") - unix_timestamp(timeB) > %d
        """ % (sql_datetime(now()), site_config['session_timeout'])
    self.db.query_com(q)

    # Remove expired password reset codes
    q = """DELETE
           FROM users_passcodes
           WHERE unix_timestamp("%s") - unix_timestamp(timeB) > %d
        """ % (sql_datetime(now()), site_config['passcode_timeout'])
    self.db.query_com(q)

    # Remove expired registration data
    q = """DELETE
           FROM users_pending
           WHERE unix_timestamp("%s") - unix_timestamp(timeB) > %d
        """ % (sql_datetime(now()), site_config['activation_timeout'])
    self.db.query_com(q)

    # Access list
    self.data['acl'] = self.access_list()
    self.data['site_admin'] = self.site_admin()

    # Posted
    self.data['posted'] = {}
    for i in self.form:
      if not self.form[i].file:
        self.data['posted'][i] = html_escape(self.form.getvalue(i, ''))

    # Errors
    self.data['errors'] = {}

    self.data['site_path'] = site_config['path']
    self.data['site_url'] = site_config['url']
    self.template = ''

  def init_session(self):
    self.data['session'] = {}
    if self.cookie['sid'] != '':
      sid = self.db.escape(self.cookie['sid'])
      q = """SELECT users.uid, users.username
             FROM users
               INNER JOIN sessions
                 ON sessions.uid = users.uid
             WHERE sessions.sid = "%s"
          """ % (sid)
      r = self.db.row_query(q)
      if r:
        self.data['session'] = {
                                'sid': self.cookie['sid'],
                                'uid': int(r[0]),
                                'username': r[1]
                                }
        q = """UPDATE sessions
               SET timeB="%s"
               WHERE sid = "%s"
            """ % (sql_datetime(now()), sid)
        self.db.query_com(q)
    
  def login(self, u, p):
    u = self.db.escape(u)
    p = pass_hash(self.db.escape(p))
    q = """SELECT uid
           FROM users
           WHERE username = "%s" AND password = "%s"
        """ % (u, p)
    uid = self.db.scalar_query(q)
    if uid:
      sid = pass_hash(str(time.time()))
      d = {'sid': sid,
           'uid': int(uid),
           'timeB': sql_datetime(now())}
      self.db.insert('sessions', d)
      self.cookie['sid'] = sid
    self.init_session()
    return uid

  def logged(self):
    return 'sid' in self.data['session']

  def site_admin(self):
    if not self.logged():
      return 0
    q = """SELECT Count(*)
           FROM rel_groups
           WHERE
             uid=%d AND
             gid=1
        """ % (self.data['session']['uid'])
    return self.db.scalar_query(q)
    
  def access_list(self):
    list = []
    if not self.logged():
      return list
    q = """SELECT rights.keyword
           FROM rel_rights
             INNER JOIN rights
               ON rights.rid=rel_rights.rid
             INNER JOIN rel_groups
               ON rel_groups.gid=rel_rights.gid
             INNER JOIN users
               ON users.uid=rel_groups.uid
           WHERE
             users.uid=%d
        """ % (self.data['session']['uid'])
    rows = self.db.query(q)
    for r in rows:
      list.append(r[0])
    return list

  def access(self, key):
    if not self.logged():
      return 0
    key = self.db.escape(key)
    q = """SELECT Count(*)
           FROM rel_rights
             INNER JOIN rights
               ON rights.rid=rel_rights.rid
             INNER JOIN rel_groups
               ON rel_groups.gid=rel_rights.gid
             INNER JOIN users
               ON users.uid=rel_groups.uid
           WHERE
             users.uid=%d AND rights.keyword="%s"
        """ % (self.data['session']['uid'], key)
    return self.db.scalar_query(q)
    
  def logout(self):
    if 'sid' in self.data['session']:
      sid = self.db.escape(self.data['session']['sid'])
      q = """DELETE FROM sessions
             WHERE sid = "%s"
          """ % (sid)
      self.db.query_com(q)
      
      self.cookie['sid'] = ''

    self.init_session()

  def build(self):
    self.run()

    tpl = site_config['path'] + 'templates/' + self.template
  
    print 'Content-type: text/html'
    print ''
    print build_template(tpl, self.data)

  def begin(self):
    self.data['site_title'] = self.title
  
  def end(self):
    if len(self.cookie):
      self.cookie.save()

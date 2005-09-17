#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config

from pyonweb.libstring import *
from pyonweb.libdate import *

import re
import glob
import os
from math import ceil

p = pardil_page()

p.name = 'pardil_admin_news'
p.title = site_config['title']

# OLMAZSA OLMAZ!
if 'sid' not in p['session']:
  p.http.redirect('error.py?tag=login_required')
if 'administrate_news' not in p['acl'] and not p.site_admin():
  p.http.redirect('error.py?tag=not_in_authorized_group')
# OLMAZSA OLMAZ!

# Sayfalama
p['pag_now'] = int(p.form.getvalue('start', '0'))
p['pag_total'] = ceil(float(p.db.scalar_query("SELECT Count(*) FROM news")) / float(site_config['pag_perpage']))

def index():
  p['news'] = []
  q = """SELECT nid, title, timeB
         FROM news
         ORDER BY nid DESC
         LIMIT %d, %d
      """ % (p['pag_now'] * site_config['pag_perpage'], site_config['pag_perpage'])
  list = p.db.query(q)
  for i in list:
    l = {
         'nid': i[0],
         'title': i[1],
         'date': i[2]
         }
    p['news'].append(l)

  p.template = 'admin/news.tpl'

def delete():
  try:
    p['nid'] = int(p.form.getvalue('nid'))
  except:
    p.template = 'admin/news.error.tpl'
    return

  q = """SELECT title
         FROM news
         WHERE nid=%d
      """ % (p['nid'])
  p['title'] = p.db.scalar_query(q)

  if not p['title']:
    p.template = 'admin/news.error.tpl'
  else:
    if 'confirm' in p.form:
      if p.form.getvalue('confirm', '') == 'yes':
        p.db.query_com('DELETE FROM news WHERE nid=%d' % (p['nid']))
        p.template = 'admin/news.delete_yes.tpl'
      else:
        p.template = 'admin/news.delete_no.tpl'
    else:
      p.template = 'admin/news.delete_confirm.tpl'

def insert():
  p['mode'] = ''
  p.template = 'admin/news.insert.tpl'

  p['icons'] = [os.path.basename(i) for i in glob.glob("images/icons/*")]

  if p.form.getvalue('post', ''):
    if not len(p.form.getvalue('n_title', '')):
      p['errors']['n_title'] = 'Başlık boş bırakılamaz.'
    if not len(p.form.getvalue('n_body', '')):
      p['errors']['n_body'] = 'İçerik boş bırakılamaz.'
    if not len(p.form.getvalue('n_icon', '')) or p.form.getvalue('n_icon') not in p['icons']:
      p['errors']['n_icon'] = 'Geçersiz simge.'

    if not len(p['errors']):
      p['title'] = p.form.getvalue('n_title')

      list = {
              'title': p['title'],
              'uid': p['session']['uid'],
              'content': p.form.getvalue('n_body'),
              'icon': p.form.getvalue('n_icon'),
              'timeB': sql_datetime(now())
            }
      p['nid'] = p.db.insert('news', list)
    
      p['mode'] = 'done'
    else:
      p['mode'] = 'error'

def edit():
  p['mode'] = ''
  p.template = 'admin/news.edit.tpl'

  try:
    p['nid'] = int(p.form.getvalue('nid'))
  except:
    p.template = 'admin/news.error.tpl'
    return

  p['icons'] = [os.path.basename(i) for i in glob.glob("images/icons/*")]

  if p.form.getvalue('post', ''):
    if not len(p.form.getvalue('nid', '')):
      p['errors']['nid'] = 'Başlık boş bırakılamaz.'
    if not len(p.form.getvalue('n_title', '')):
      p['errors']['n_title'] = 'Başlık boş bırakılamaz.'
    if not len(p.form.getvalue('n_body', '')):
      p['errors']['n_body'] = 'İçerik boş bırakılamaz.'
    if not len(p.form.getvalue('n_icon', '')) or p.form.getvalue('n_icon') not in p['icons']:
      p['errors']['n_icon'] = 'Geçersiz simge.'

    if not len(p['errors']):
      p['title'] = p.form.getvalue('n_title')

      q = """UPDATE news
             SET
               title="%s",
               content="%s",
               icon="%s"
             WHERE nid=%d
          """ % (p.db.escape(p['title']),
                 p.db.escape(p.form.getvalue('n_body')),
                 p.db.escape(p.form.getvalue('n_icon')),
                 p['nid'])
      p.db.query_com(q)
    
      p['mode'] = 'done'
    else:
      p['mode'] = 'error'
  else:
    q = """SELECT title, content, icon
           FROM news
           WHERE nid=%d
        """ % (p['nid'])
    row = p.db.row_query(q)

    p['posted'] = {
                   'n_title': html_escape(row[0]),
                   'n_body': html_escape(row[1]),
                   'n_icon': html_escape(row[2])
                   }

p.actions = {
             'default': index,
             'delete': delete,
             'edit': edit,
             'insert': insert
             }

p.build()

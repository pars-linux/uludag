#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config

from pyonweb.libstring import *
from pyonweb.libdate import *
import re

p = pardil_page()

p.name = 'pardil_editproposal'
p.title = site_config['title']

if 'sid' not in p['session']:
  p.http.redirect('error.py?tag=login_required')

def index():
  try:
    p['pid'] = int(p.form.getvalue('pid'))
    p['version'] = p.form.getvalue('version')
  except:
    p.http.redirect('error.py?tag=proposal_not_found')
   
  # Bildiri sorumlusu mu?
  q = """SELECT Count(*)
         FROM rel_maintainers
         WHERE
           uid=%s AND pid=%s"""
  if not p.db.scalar_query(q, (p['session']['uid'], p['pid'])):
    p.http.redirect('error.py?tag=not_maintainer')

  q = """SELECT
           version, title, summary, content
         FROM proposals_versions
         WHERE
           pid=%s AND version=%s"""
  row = p.db.row_query(q, (p['pid'], p['version']))

  p['posted'] = {
                 'p_version': html_escape(row[0]),
                 'p_title': html_escape(row[1]),
                 'p_summary': html_escape(row[2]),
                 'p_content': html_escape(row[3]),
                 }
  
  p.template = 'edit_proposal.tpl'

def edit():
  try:
    p['pid'] = int(p.form.getvalue('pid'))
    p['version'] = p.form.getvalue('version')
  except:
    p.http.redirect('error.py?tag=proposal_not_found')

  # Bildiri sorumlusu mu?
  q = """SELECT Count(*)
         FROM rel_maintainers
         WHERE
           uid=%s AND pid=%s"""
  if not p.db.scalar_query(q, (p['session']['uid'], p['pid'])):
    p.http.redirect('error.py?tag=not_maintainer')

  p.template = 'edit_proposal.tpl'

  if not len(p.form.getvalue('p_title', '')):
    p['errors']['p_title'] = 'Başlık boş bırakılamaz.'

  if not len(p.form.getvalue('p_summary', '')):
    p['errors']['p_summary'] = 'Özet boş bırakılamaz.'

  if not len(p.form.getvalue('p_content', '')):
    p['errors']['p_content'] = 'Bildiri detayları boş bırakılamaz.'

  if int(p.form.getvalue('p_version', 0)) not in range(1, 4):
    p['errors']['p_version'] = 'Değişiklik derecesi geçerli değil.'

  if not len(p.form.getvalue('p_changelog', '')):
    p['errors']['p_changelog'] = 'Sürüm notları boş bırakılamaz.'

  # Hiç hata yoksa...
  if not len(p['errors']):

    version = p['version'].split('.')
    for k,v in enumerate(version):
      if p.form.getvalue('p_version', '') == str(k + 1):
        version[k] = str(int(v) + 1)
    version = '.'.join(version)

    list = {
            'pid': p['pid'],
            'version': version,
            'title': p.form.getvalue('p_title'),
            'summary': p.form.getvalue('p_summary'),
            'content': p.form.getvalue('p_content'),
            'timeB': sql_datetime(now()),
            'changelog': p.form.getvalue('p_changelog')
            }
    vid = p.db.insert('proposals_versions', list)

    p['version'] = version
    p.template = 'edit_proposal.done.tpl'

p.actions = {
             'default': index,
             'edit': edit
             }
p.build()

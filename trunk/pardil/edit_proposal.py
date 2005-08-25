#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config

from pyonweb.libstring import *
from lib_date import *

p = pardil_page()

p.name = 'pardil_editproposal'
p.title = site_config['title']

# FIXME:
# Erişim kontrolü değiştirilmeli...
if 'sid' not in p['session']:
  p.http.redirect('error.py?tag=login_required')
if not p.access('proposals_add'):
  p.http.redirect('error.py?tag=not_in_authorized_group')

def index():
  p['pid'] = int(p.form['pid'])
  p['version'] = p.form['version']

  q = """SELECT
           version, title, summary, purpose, content, solution
         FROM proposals_versions
         WHERE
           pid=%d AND version="%s"
      """ % (p['pid'], p.db.escape(p['version']))
  row = p.db.row_query(q)

  p['posted']['p_version'] = html_escape(row[0])
  p['posted']['p_title'] = html_escape(row[1])
  p['posted']['p_summary'] = html_escape(row[2])
  p['posted']['p_purpose'] = html_escape(row[3])
  p['posted']['p_content'] = html_escape(row[4])
  p['posted']['p_solution'] = html_escape(row[5])
  
  p.template = site_config['path'] + 'templates/edit_proposal.tpl'

def edit():
  p['pid'] = int(p.form['pid'])
  p['version'] = p.form['version']

  p.template = site_config['path'] + 'templates/edit_proposal.tpl'

  if not len(p.form['p_title']):
    p['errors']['p_title'] = 'Başlık boş bırakılamaz.'
  elif len(p.form['p_title']) > 100:
    p['errors']['p_title'] = 'Başlık en fazla 100 karakter olabilir.'
    
  if int(p.form['p_version']) not in range(1, 4):
    p['errors']['p_version'] = 'Değişiklik derecesi geçerli değil.'

  if not len(p.form['p_changelog']):
    p['errors']['p_changelog'] = 'Sürüm notları boş bırakılamaz.'

  # Hiç hata yoksa...
  if not len(p['errors']):

    version = p['version'].split('.')
    for k,v in enumerate(version):
      if p.form['p_version'] == str(k + 1):
        version[k] = str(int(v) + 1)
    version = '.'.join(version)

    insert_list = {'pid': p['pid'],
                   'version': version,
                   'title': p.form['p_title'],
                   'summary': p.form['p_summary'],
                   'purpose': p.form['p_purpose'],
                   'content': p.form['p_content'],
                   'solution': p.form['p_solution'],
                   'timeB': sql_datetime(now()),
                   'changelog': p.form['p_changelog']}
    vid = p.db.insert('proposals_versions', insert_list)

    p['version'] = version
    p.template = site_config['path'] + 'templates/edit_proposal.done.tpl'

p.actions = {'default': index,
             'edit': edit}
p.build()

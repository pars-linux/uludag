#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config

from lib_date import *
import re

p = pardil_page()

p.name = 'pardil_newproposal'
p.title = site_config['title']

def new():
  p.template = site_config['path'] + 'templates/new_proposal.tpl'

  # FIXME:
  # Erişim kontrolü değiştirilmeli...
  if 'sid' not in p['session']:
    p.http.redirect('error.py?tag=login_required')
  if not p.access('proposals_add'):
    p.http.redirect('error.py?tag=not_in_authorized_group')

  if not re.match('^.{10,100}$', p.form['p_title']):
    p['errors']['p_title'] = 'Başlık 10-100 karakter arası olmalı.'

  # Hiç hata yoksa...
  if not len(p['errors']):
    version = '1.0.0'

    insert_list = {'uid': p['session']['uid'],
                   'startup': sql_datetime(now())}
    pid = p.db.insert('proposals', insert_list)
    
    insert_list = {'pid': pid,
                   'version': version,
                   'title': p.form['p_title'],
                   'summary': p.form['p_summary'],
                   'purpose': p.form['p_purpose'],
                   'content': p.form['p_content'],
                   'solution': p.form['p_solution'],
                   'timeB': sql_datetime(now()),
                   'changelog': p.form['p_changelog']}
    vid = p.db.insert('proposals_versions', insert_list)

    p['pid'] = pid
    p['version'] = version
    p.template = site_config['path'] + 'templates/new_proposal.done.tpl'

def index():
  p.template = site_config['path'] + 'templates/new_proposal.tpl'

p.actions = {'default': index,
             'new': new}
p.build()

#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config

from pyonweb.libdate import *
import re

p = pardil_page()

p.name = 'pardil_newproposal'
p.title = site_config['title']

if 'sid' not in p['session']:
  p.http.redirect('error.py?tag=login_required')
if not p.access('proposals_add'):
  p.http.redirect('error.py?tag=not_in_authorized_group')

def new():
  p.template = 'new_proposal.tpl'

  if 'p_title' not in p.form or not len(p.form['p_title']):
    p['errors']['p_title'] = 'Başlık boş bırakılamaz.'

  if 'p_summary' not in p.form or not len(p.form['p_summary']):
    p['errors']['p_summary'] = 'Özet boş bırakılamaz.'

  if 'p_purpose' not in p.form or not len(p.form['p_purpose']):
    p['errors']['p_purpose'] = 'Amaç boş bırakılamaz.'
    
  if 'p_content' not in p.form or not len(p.form['p_content']):
    p['errors']['p_content'] = 'Öneri detayları boş bırakılamaz.'

  if 'p_solution' not in p.form or not len(p.form['p_solution']):
    p['errors']['p_solution'] = 'Çözüm boş bırakılamaz.'

  # Hiç hata yoksa...
  if not len(p['errors']):


    # Öneri hemen yayınlansın mı...
    if p.access('proposals_publish'):
      version = '1.0.0'
      list = {
              'uid': p['session']['uid'],
              'startup': sql_datetime(now())
              }
      pid = p.db.insert('proposals', list)
      list = {
              'pid': pid,
              'version': version,
              'title': p.form['p_title'],
              'summary': p.form['p_summary'],
              'purpose': p.form['p_purpose'],
              'content': p.form['p_content'],
              'solution': p.form['p_solution'],
              'timeB': sql_datetime(now()),
              'changelog': p.form['p_changelog']
              }
      vid = p.db.insert('proposals_versions', list)
      p['pid'] = pid
      p['version'] = version
    else:
      list = {
              'uid': p['session']['uid'],
              'title': p.form['p_title'],
              'summary': p.form['p_summary'],
              'purpose': p.form['p_purpose'],
              'content': p.form['p_content'],
              'solution': p.form['p_solution'],
              'timeB': sql_datetime(now())
              }
      p.db.insert('proposals_pending', list)
      p['pid'] = 0
      p['version'] = 0
      
    p.template = 'new_proposal.done.tpl'

def index():
  p.template = 'new_proposal.tpl'

p.actions = {
             'default': index,
             'new': new
             }
p.build()

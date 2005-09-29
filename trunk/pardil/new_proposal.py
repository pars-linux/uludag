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
if 'proposals_add' not in p['acl'] and not p.site_admin():
  p.http.redirect('error.py?tag=not_in_authorized_group')

def new():
  p.template = 'new_proposal.tpl'

  if not len(p.form.getvalue('p_title', '')):
    p['errors']['p_title'] = 'Başlık boş bırakılamaz.'

  if not len(p.form.getvalue('p_summary', '')):
    p['errors']['p_summary'] = 'Özet boş bırakılamaz.'

  if not len(p.form.getvalue('p_content', '')):
    p['errors']['p_content'] = 'Öneri detayları boş bırakılamaz.'

  # Hiç hata yoksa...
  if not len(p['errors']):


    # Öneri hemen yayınlansın mı...
    if 'proposals_publish' in p['acl']:
      version = '1.0.0'
      
      # Öneriler tablosuna ekle
      list = {
              'uid': p['session']['uid'],
              'startup': sql_datetime(now())
              }
      pid = p.db.insert('proposals', list)

      # İlk sürümü ekle
      list = {
              'pid': pid,
              'version': version,
              'title': p.form.getvalue('p_title'),
              'summary': p.form.getvalue('p_summary'),
              'content': p.form.getvalue('p_content'),
              'timeB': sql_datetime(now()),
              'changelog': "İlk sürüm."
              }
      vid = p.db.insert('proposals_versions', list)
      
      # Kişiyi öneri sorumlusu olarak ata
      list = {
              'uid': p['session']['uid'],
              'pid': pid
              }
      p.db.insert('rel_maintainers', list)
      
      p['pid'] = pid
      p['version'] = version
    else:
      list = {
              'uid': p['session']['uid'],
              'title': p.form.getvalue('p_title'),
              'summary': p.form.getvalue('p_summary'),
              'content': p.form.getvalue('p_content'),
              'timeB': sql_datetime(now())
              }
      p.db.insert('proposals_pending', list)
      p['pid'] = 0
      p['version'] = 0
      
    p.template = 'new_proposal.done.tpl'

def index():
  p['posted'] = {
                 'p_content': "Amaç\n====\n\nYazı\n\nDetaylar\n========\n\nYazı",
                 }
  p.template = 'new_proposal.tpl'

p.actions = {
             'default': index,
             'new': new
             }
p.build()

#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config

from pyonweb.libstring import *
from pyonweb.textutils import formatText

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

  try:
    t_pid = int(p.form.getvalue('p_pid', 0))
  except:
    p['errors']['p_pid'] = 'Bildiri numarası rakamlardan oluşmalı.'
  else:
    q = """SELECT Count(*)
           FROM proposals
           WHERE pid=%s"""
    if p.db.scalar_query(q, t_pid):
      p['errors']['p_pid'] = 'Bu numaraya sahip bir bildiri var.'
    
  if not len(p.form.getvalue('p_title', '')):
    p['errors']['p_title'] = 'Başlık boş bırakılamaz.'

  if not len(p.form.getvalue('p_summary', '')):
    p['errors']['p_summary'] = 'Özet boş bırakılamaz.'

  if not len(p.form.getvalue('p_content', '')):
    p['errors']['p_content'] = 'Bildiri detayları boş bırakılamaz.'

  # Hiç hata yoksa...
  if not len(p['errors']):


    # Bildiri hemen yayınlansın mı...
    if 'proposals_publish' in p['acl']:
      version = '1.0.0'
      
      # Bildiriler tablosuna ekle
      list = {
              'uid': p['session']['uid'],
              'startup': sql_datetime(now())
              }
      if t_pid:
        list['pid'] = t_pid
        p.db.insert('proposals', list)
        pid = t_pid
      else:
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
      
      # Kişiyi bildiri sorumlusu olarak ata
      list = {
              'uid': p['session']['uid'],
              'pid': pid
              }
      p.db.insert('rel_maintainers', list)
      
      p['pid'] = pid
      p['version'] = version
    else:
      list = {
              'pid': t_pid,
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

def preview():

  try:
    t_pid = int(p.form.getvalue('p_pid', 0))
  except:
    p['errors']['p_pid'] = 'Bildiri numarası rakamlardan oluşmalı.'
  else:
    q = """SELECT Count(*)
           FROM proposals
           WHERE pid=%s"""
    if p.db.scalar_query(q, t_pid):
      p['errors']['p_pid'] = 'Bu numaraya sahip bir bildiri var.'
    
  if not len(p.form.getvalue('p_title', '')):
    p['errors']['p_title'] = 'Başlık boş bırakılamaz.'

  if not len(p.form.getvalue('p_summary', '')):
    p['errors']['p_summary'] = 'Özet boş bırakılamaz.'

  if not len(p.form.getvalue('p_content', '')):
    p['errors']['p_content'] = 'Bildiri detayları boş bırakılamaz.'

  # Hiç hata yoksa...
  if not len(p['errors']):
      p.template = 'previewproposal.tpl'

      p['proposal'] = {
                   'title': html_escape(p.form.getvalue("p_title", "")),
                   'summary': nl2br(html_escape(p.form.getvalue("p_summary", ""))),
                   'content': formatText(p.form.getvalue("p_content", ""))
                   }
  else:
    p.template = 'new_proposal.tpl'

p.actions = {
             'default': index,
             'new': new,
             'preview': preview
             }
p.build()

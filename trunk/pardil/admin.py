#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config

p = pardil_page()

p.name = 'pardil_index'
p.title = site_config['title']

def index():
  # OLMAZSA OLMAZ!
  if 'sid' not in p['session']:
    p.http.redirect('error.py?tag=login_required')
  if not p.access('administrate'):
    p.http.redirect('error.py?tag=not_in_authorized_group')
  # OLMAZSA OLMAZ!

  p.template = site_config['path'] + 'templates/admin/index.tpl'

p.actions = {'default': index}

p.build()

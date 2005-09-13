#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config

p = pardil_page()

p.name = 'pardil_admin'
p.title = site_config['title']

# OLMAZSA OLMAZ!
if 'sid' not in p['session']:
  p.http.redirect('error.py?tag=login_required')
if 'administrate' not in p['acl'] and not p.site_admin():
  p.http.redirect('error.py?tag=not_in_authorized_group')
# OLMAZSA OLMAZ!

def index():
  p.template = 'admin/index.tpl'

p.actions = {'default': index}

p.build()

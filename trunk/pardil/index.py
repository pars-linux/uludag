#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config

p = pardil_page()

p.name = 'pardil_index'
p.title = site_config['title']

def index():
  p['news'] = []
  p['news'].append({'title': 'Pardil', 'content': '...', 'icon': 'images/icons/bell.png'})
  p['news'].append({'title': 'Pardil', 'content': '...', 'icon': 'images/icons/bell.png'})
  p['news'].append({'title': 'Pardil', 'content': '...', 'icon': 'images/icons/bell.png'})
  p['news'].append({'title': 'Pardil', 'content': '...', 'icon': 'images/icons/bell.png'})

  p.template = site_config['path'] + 'templates/index.tpl'

p.actions = {'default': index}

p.build()

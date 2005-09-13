#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config

p = pardil_page()

p.name = 'pardil_index'
p.title = site_config['title']

def index():
  p['news'] = []
  n = {
       'title': 'Pardil',
       'content': '...',
       'icon':'images/icons/news.png'
       }
  p['news'].append(n)

  p.template = 'index.tpl'

p.actions = {'default': index}

p.build()

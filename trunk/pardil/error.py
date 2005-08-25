#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config

p = pardil_page()

p.name = 'pardil_error'
p.title = site_config['title']

def index():

  p['keyword'] = p.form['tag']

  p.template = site_config['path'] + 'templates/error.tpl'

p.actions = {'default': index}

p.build()

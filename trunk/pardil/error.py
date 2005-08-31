#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config

p = pardil_page()

p.name = 'pardil_error'
p.title = site_config['title']

def index():

  errors = {
            'login_required': 'Bu işlemi yapmadan önce giriş yapmalısınız.',
            'not_in_authorized_group': 'Bu işlemi yapma yetkisine sahip bir gruba üye olmalısınız.'
            }

  if p.form['tag'] in errors:
    p['keyword'] = errors[p.form['tag']]
  else:
    p['keyword'] = p.form['tag']

  p.template = 'error.tpl'

p.actions = {'default': index}

p.build()

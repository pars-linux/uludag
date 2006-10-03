#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config

p = pardil_page()

p.name = 'pardil_index'
p.title = site_config['title']

def index():
  p['news'] = []
  q = """SELECT
           news.title,
           news.content,
           news.icon,
           news.timeB,
           users.username
         FROM news
           INNER JOIN users
             ON users.uid=news.uid
         ORDER BY nid DESC
         LIMIT 10"""
  list = p.db.query(q)
  for i in list:
    n = {
         'title': i[0],
         'content': i[1],
         'icon': 'images/icons/' + i[2],
         'date': i[3],
         'user': i[4]
         }
    p['news'].append(n)

  p.template = 'index.tpl'

p.actions = {'default': index}

p.build()

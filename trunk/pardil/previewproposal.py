#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config

from pyonweb.libstring import *
from pyonweb.textutils import formatText
from pyonweb.libdate import *

p = pardil_page()

p.name = 'pardil_previewproposals'
p.title = site_config['title']

def index():
  p.template = 'previewproposal.tpl'

  p['proposal'] = {
                   'title': html_escape(p.form.getvalue("p_title", "0")),
                   'summary': nl2br(html_escape(p.form.getvalue("p_summary", "0"))),
                   'content': formatText(p.form.getvalue("p_content", "0"))
                   }

p.actions = {
             'default': index
             }

p.build()

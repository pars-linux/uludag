#!/usr/bin/env python
# -- coding: utf-8 --

import sys
import os

sys.path.append(os.getcwd() + '/../ajax_base')

import xhr
import time
import md5

def login(o):
  if o['user'] == 'Pardus' and o['pass'] == u'Linüks':
    return {'session': md5.new(str(time.time())).hexdigest(), 'user': o['user']}
  return 'h'

x = xhr.xhr()
x.register(login)
x.handle()

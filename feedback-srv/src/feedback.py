#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2005, Bahadır Kandemir
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

from config import site_config
from mysql import mysql

import cgi
import time
import os

# DB connection
sql = mysql(site_config['db_host'], \
            site_config['db_name'], \
            site_config['db_user'], \
            site_config['db_pass'])

# 

form = cgi.FieldStorage()

data = {
        'ip':  os.environ['REMOTE_ADDR'],
        'submitdate': time.strftime('%Y-%m-%d %H:%M'),
        'exp': form.getvalue('exp', '0'),
        'purpose': form.getvalue('purpose', '0'),
        'use_where': form.getvalue('usage', '0'),
        'question': form.getvalue('question', '0'),
        'opinion': form.getvalue('opinion', ''),
        'email': form.getvalue('email', ''),
        'email_announce': form.getvalue('email_announce', 'F')
        }
sql.insert('feedback', data)

print "Content-type: text/html"
print
print "1"

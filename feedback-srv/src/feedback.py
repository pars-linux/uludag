#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2005, 2006 TÜBİTAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

from config import site_config
from mysql import mysql

import time

def index(req, exp='0', purpose='0', usage='0', \
          question='0', opinion='', email='', email_announce='F'):
    # DB connection
    sql = mysql(site_config['db_host'], \
                site_config['db_name'], \
                site_config['db_user'], \
                site_config['db_pass'])

    data = {
            'ip':  req.get_remote_host(),
            'submitdate': time.strftime('%Y-%m-%d %H:%M'),
            'exp': exp,
            'purpose': purpose,
            'use_where': usage,
            'question': question,
            'opinion': opinion,
            'email': email,
            'email_announce': email_announce
            }
    sql.insert('feedback', data)

    return "1"

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

from simplejson import loads as json_decode

import time

def index(req, data=""):

    _SUCCESS = "0"
    _DATAFORMAT = 1
    _VERSION = 2
    _MISSING = 3
    _DATABASE = 4
    _FLOOD = 5

    # Decode submitted data
    try:
        data = json_decode(data)
    except:
        return _DATAFORMAT
    
    # Check feedback version
    if "version" not in data:
        return _VERSION

    # DB connection
    try:
        sql = mysql(site_config['db_host'], \
                    site_config['db_name'], \
                    site_config['db_user'], \
                    site_config['db_pass'])
    except:
        return _DATABASE

    # Check required fields
    s1 = set(["experience", "question"])
    s2 = set(data.keys())

    if len(s1 - s2) != 0:
        return _MISSING

    # An IP may submit only one feedback in 10 minutes.
    submissions = sql.scalar_query("SELECT Count(*) FROM feedback WHERE ip=%s AND now()-submitdate < 600", req.get_remote_host())
    if submissions > 0:
        return _FLOOD

    if "hw" in data:
        s1 = set(["memtotal", "swaptotal", "cpu_model", "cpu_speed", "kernel"])
        s2 = set(data["hw"].keys())

        if len(s1 - s2) != 0:
            return _MISSING

    values = {
              "ip": req.get_remote_host(),
              "submitdate": time.strftime('%Y-%m-%d %H:%M'),
              "experience": data.get("experience", "0"),
              "purpose": data.get("purpose", "0"),
              "use_where": data.get("usage", "0"),
              "question": data.get("question", ""),
              "opinion": data.get("opinion", ""),
              "email": data.get("email", ""),
              "email_announce": data.get("email_announce", "F")
              }
    fb = sql.insert("feedback", values)

    if "hw" in data:
        values = {
                  "feedback": fb,
                  "memtotal": data["hw"]["memtotal"],
                  "swaptotal": data["hw"]["swaptotal"],
                  "cpu_model": data["hw"]["cpu_model"],
                  "cpu_speed": data["hw"]["cpu_speed"],
                  "kernel": data["hw"]["kernel"]
                  }
        hw = sql.insert("hardware", values)

    return _SUCCESS

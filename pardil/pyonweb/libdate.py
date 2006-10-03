# -*- coding: utf-8 -*-

# Copyright (C) 2005, Bahadır Kandemir
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

import time

def now():
  return int(time.time())

def sql_date(t):
  return time.strftime('%Y-%m-%d', time.gmtime(t))

def sql_datetime(t):
  return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(t))

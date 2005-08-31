# -*- coding: utf-8 -*-

# Copyright (C) 2005, Bahadır Kandemir
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

import smtplib

def sendmail(fr, to, ti, bo):
  msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s" % (fr, to, ti, bo)
  s = smtplib.SMTP('localhost')
  #s.login()
  s.sendmail(fr, to, msg)
  s.quit()

#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import os
import string
from qt import *

class Actions(QTextEdit):
	def __init__(self, *args):
		QTextEdit.__init__(self, *args)
	
	def edit_actions(self, fname):
		try:
			f = file(fname)
			lines = f.readlines()
			f.close()
			self.setText(string.join(lines, ""))
		except:
			pass

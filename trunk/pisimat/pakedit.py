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

import string
from qt import *
import source

class PakEdit(QMainWindow):
	def __init__(self, *args):
		QMainWindow.__init__(self, *args)
		self.setMinimumSize(540, 320)
		vb = QVBoxLayout(self, 6)
		tab = QTabWidget(self)
		self.src = source.Source(self)
		tab.addTab(self.src, "Source")
		tab.addTab(QLabel("Packages", self), "Packages")
		self.acts = QTextEdit(self)
		tab.addTab(self.acts, "Actions")
		tab.addTab(QLabel("Config", self), "Config")
		vb.addWidget(tab)
	
	def edit_pak(self, dirname):
		aname = dirname[:dirname.rfind("/") + 1] + "actions.py"
		try:
			f = file(aname)
			lines = f.readlines()
			f.close()
			self.acts.setText(string.join(lines, ""))
		except:
			pass
		self.src.update(dirname)

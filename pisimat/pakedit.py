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
from qt import *
import source
import actions
import subpaks

class PakEdit(QMainWindow):
	def __init__(self, *args):
		QMainWindow.__init__(self, *args)
		self.setMinimumSize(540, 320)
		vb = QVBoxLayout(self, 6)
		tab = QTabWidget(self)
		self.src = source.Source(self)
		tab.addTab(self.src, "Source")
		self.paks = subpaks.SubPaks(self)
		tab.addTab(self.paks, "Packages")
		self.acts = actions.Actions(self)
		tab.addTab(self.acts, "Actions")
		tab.addTab(QLabel("Config", self), "Config")
		vb.addWidget(tab)
	
	def edit_pak(self, pdir):
		self.pak_dir = pdir
		self.src.edit_pak(pdir)
		self.paks.edit_paks(pdir)
		self.acts.edit_actions(os.path.join(pdir, "actions.py"))

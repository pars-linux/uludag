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
import xml.dom
import xml.dom.minidom
from qt import *

class SubPaks(QWidget):
	def __init__(self, *args):
		QWidget.__init__(self, *args)
		hb = QHBoxLayout(self)
		vb = QVBoxLayout(self)
		self.list = QListView(self)
		self.list.addColumn("Package")
		vb.addWidget(self.list)
		b = QPushButton("Add Package", self)
		self.connect(b, SIGNAL("clicked()"), self.add_pak)
		vb.addWidget(b)
		b = QPushButton("Remove Package", self)
		self.connect(b, SIGNAL("clicked()"), self.rem_pak)
		vb.addWidget(b)
		hb.addLayout(vb)
		vb = QVBoxLayout(self)
		vb.addWidget(QLabel("Name", self))
		vb.addWidget(QLabel("Files", self))
		self.list2 = QListView(self)
		vb.addWidget(self.list2)
		vb.addWidget(QLabel("etc...", self))
		hb.addLayout(vb)
	
	def add_pak(self):
		pass
	
	def rem_pak(self):
		pass
	
	def edit_paks(self, pdir):
		self.fname = os.path.join(pdir, "pspec.xml")
		try:
			doc = xml.dom.minidom.parse(self.fname)
		except:
			return
		for pak in doc.getElementsByTagName("Package"):
			QListViewItem(self.list, pak.getElementsByTagName("Name")[0].firstChild.data)
		doc.unlink()

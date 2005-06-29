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

def get_cdata(node, tag):
	try:
		c = node.getElementsByTagName(tag)[0].firstChild.data
	except:
		c = ""
	return c

class Patches(QWidget):
	def __init__(self, *args):
		QWidget.__init__(self, *args)
		vb = QVBoxLayout(self)
		self.list = QListView(self)
		self.list.addColumn("Patch")
		vb.addWidget(self.list)
		hb = QHButtonGroup(self)
		vb.addWidget(hb)
		b = QPushButton("Add Patch", hb)
		self.connect(b, SIGNAL("clicked()"), self.add_patch)
		b = QPushButton("Remove Patch", hb)
		self.connect(b, SIGNAL("clicked()"), self.rem_patch)
	
	def add_patch(self):
		pass
	
	def rem_patch(self):
		pass
	
	def edit_patches(self, node):
		for p in node.getElementsByTagName("Patch"):
			QListViewItem(self.list, p.firstChild.data)

class Source(QWidget):
	def __init__(self, *args):
		QWidget.__init__(self, *args)
		vb = QVBoxLayout(self, 6)
		g = QGridLayout(vb, 4, 2, 6)
		lab = QLabel("Name", self)
		g.addWidget(lab, 0, 0)
		lab = QLabel("Homepage", self)
		g.addWidget(lab, 1, 0)
		lab = QLabel("License", self)
		g.addWidget(lab, 2, 0)
		lab = QLabel("Archive", self)
		g.addWidget(lab, 3, 0)
		self.name = QLineEdit(self)
		g.addWidget(self.name, 0, 1)
		self.home = QLineEdit(self)
		g.addWidget(self.home, 1, 1)
		self.license = QLineEdit(self)
		g.addWidget(self.license, 2, 1)
		self.archive = QLineEdit(self)
		g.addWidget(self.archive, 3, 1)
		self.patches = Patches(self)
		vb.addWidget(self.patches)
	
	def edit_pak(self, pdir):
		self.fname = os.path.join(pdir, "pspec.xml")
		try:
			doc = xml.dom.minidom.parse(self.fname)
		except:
			return
		src = doc.getElementsByTagName("Source")[0]
		self.name.setText(get_cdata(src, "Name"))
		self.home.setText(get_cdata(src, "Homepage"))
		self.license.setText(get_cdata(src, "License"))
		self.archive.setText(get_cdata(src, "Archive"))
		p = src.getElementsByTagName("Patches")
		if p != []:
			self.patches.edit_patches(p[0])
		doc.unlink()

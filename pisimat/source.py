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

import xml.dom
import xml.dom.minidom
from qt import *

def get_cdata(node, tag):
	try:
		c = node.getElementsByTagName(tag)[0].firstChild.data
	except:
		c = ""
	return c

class Source(QWidget):
	def __init__(self, *args):
		QWidget.__init__(self, *args)
		g = QGridLayout(self, 4, 2, 6)
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
	
	def update(self, dirname):
		doc = xml.dom.minidom.parse(dirname)
		src = doc.getElementsByTagName("Source")[0]
		self.name.setText(get_cdata(src, "Name"))
		self.home.setText(get_cdata(src, "Homepage"))
		self.license.setText(get_cdata(src, "License"))
		self.archive.setText(get_cdata(src, "Archive"))
		doc.unlink()

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

import sys, time
import os
import codecs
import ConfigParser
from qt import *

class GreetWindow(QDialog):
	def __init__(self, *args):
		QDialog.__init__(self, *args)
		self.setCaption("Welcome")
		vb = QVBoxLayout(self, 6)
		g = QGridLayout(vb, 3, 2, 6)
		lab = QLabel("Name", self)
		g.addWidget(lab, 0, 0)
		lab = QLabel("Email", self)
		g.addWidget(lab, 1, 0)
		lab = QLabel("Pkg dir", self)
		g.addWidget(lab, 2, 0)
		self.name = QLineEdit(self)
		g.addWidget(self.name, 0, 1)
		self.email = QLineEdit(self)
		g.addWidget(self.email, 1, 1)
		hb = QHBoxLayout(self, 1)
		self.dir = QLineEdit(self)
		hb.addWidget(self.dir)
		b = QPushButton("...", self)
		self.connect(b, SIGNAL("clicked()"), self.ask_file)
		hb.addWidget(b)
		g.addLayout(hb, 2, 1)
		b = QPushButton("OK", self)
		b.setDefault(True)
		self.connect(b, SIGNAL("clicked()"), self.accept)
		vb.addWidget(b)
	
	def ask_file(self):
		s = QFileDialog.getExistingDirectory(self.dir.text(), self, "lala", "Choose packages directory", False)
		self.dir.setText(s)
	
	def accept(self):
		if self.name.text() == "" or self.email.text() == "" or self.dir.text() == "":
			return
		QDialog.accept(self)
	
	def reject(self):
		sys.exit(0)

def writeU(fname, data):
	f = codecs.open(fname, "w", "utf-8")
	f.writelines(data)
	f.close()

def readU(fname):
	f = codecs.open(fname, "r", "utf-8")
	data = f.readlines()
	f.close()
	return data

def greet(parent, force=0):
	d = GreetWindow(parent)
	d.setModal(True)
	if force != 1:
		try:
			s = readU(os.path.join(os.getenv("HOME"), ".pisimat"))
			s1 = s[0].rstrip("\n")
			s2 = s[1].rstrip("\n")
			s3 = s[2].rstrip("\n")
			d.name.setText(s1)
			d.email.setText(s2)
			d.dir.setText(s3)
			return ( s1, s2, s3 )
		except:
			d.dir.setText(os.getenv("HOME", "/"))
	d.show()
	if QDialog.Accepted == d.exec_loop():
		s1 = unicode(d.name.text())
		s2 = unicode(d.email.text())
		s3 = unicode(d.dir.text())
		writeU(os.path.join(os.getenv("HOME"), ".pisimat"), (s1 + "\n", s2 + "\n", s3 + "\n"))
		return ( s1, s2, s3 )

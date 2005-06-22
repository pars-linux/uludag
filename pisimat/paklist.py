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
import os.path
from qt import *
import pakedit

class Pak(QListViewItem):
	def __init__(self, list, specpath):
		self.path = specpath
		dirs = specpath.split("/")
		pn = dirs[-1]
		parent = list
		if len(dirs) > 1:
			for d in dirs[:-1]:
				if d != "":
					parent = self.get_parent(parent, d)
		QListViewItem.__init__(self, parent, pn)
	
	def get_parent(self, parent, item):
		t = parent.firstChild()
		while t:
			if t.text(0) == item:
				return t
			t = t.nextSibling()
		return QListViewItem(parent, item)

class PakList(QVBoxLayout):
	def __init__(self, *args):
		QVBoxLayout.__init__(self, *args)
		self.list = QListView(*args)
		list = self.list
		list.setRootIsDecorated(True)
		list.addColumn("Package")
		self.connect(list, SIGNAL("selectionChanged()"), self.change)
		self.addWidget(list)
		hb = QHButtonGroup(*args)
		self.addWidget(hb)
		self.bt_edit = QPushButton("Edit Package", hb)
		self.bt_edit.setDisabled(True)
		self.connect(self.bt_edit, SIGNAL("clicked()"), self.edit)
		b = QPushButton("Create New Package", hb)
		self.connect(b, SIGNAL("clicked()"), self.create)
		self.winlist = []
	
	def scan_dir(self, dirname):
		# this func needs luv
		# reset
		self.main_path = dirname
		self.list.clear()
		# populate the list
		for root, dirs, files in os.walk(dirname):
			for f in files:
				if ".pspec" in f:
					Pak(self.list, os.path.join(root, f)[len(self.main_path):])
					# found a package, dont go deeper
					for d in dirs:
						dirs.remove(d)
			# dont walk into the versioned stuff
			if "CVS" in dirs:
				dirs.remove("CVS")
			if ".svn" in dirs:
				dirs.remove(".svn")
	
	def change(self):
		item = self.list.selectedItem()
		if item == None:
			self.bt_edit.setDisabled(True)
		else:
			self.bt_edit.setEnabled(True)
	
	def edit(self):
		item = self.list.selectedItem()
		if item == None:
			return
		p = pakedit.PakEdit(None)
		p.edit_pak(os.path.join(self.main_path, str(item.path)))
		p.show()
		self.winlist.append(p)
	
	def create(self):
		print "not implemented"

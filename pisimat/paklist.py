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
import xml.dom
import xml.dom.minidom
from qt import *
import pakedit

class PakList(QVBoxLayout):
	def __init__(self, *args):
		QVBoxLayout.__init__(self, *args)
		self.list = QListView(*args)
		list = self.list
		list.setRootIsDecorated(True)
		list.addColumn("Package")
		list.addColumn("Version")
		self.connect(list, SIGNAL("selectionChanged()"), self._change)
		self.addWidget(list)
		hb = QHButtonGroup(*args)
		self.addWidget(hb)
		self.bt_edit = QPushButton("Edit Package", hb)
		self.bt_edit.setDisabled(True)
		self.connect(self.bt_edit, SIGNAL("clicked()"), self.edit)
		b = QPushButton("Create New Package", hb)
		self.connect(b, SIGNAL("clicked()"), self.create)
		self.winlist = []
	
	def _change(self):
		item = self.list.selectedItem()
		if item == None or item.path == None:
			self.bt_edit.setDisabled(True)
		else:
			self.bt_edit.setEnabled(True)
	
	def _get_version(self, pdir):
		try:
			doc = xml.dom.minidom.parse(os.path.join(pdir, "pspec.xml"))
			src = doc.getElementsByTagName("Source")[0]
			history = src.getElementsByTagName("History")[0]
			upd = history.getElementsByTagName("Update")[0]
			vers = upd.getElementsByTagName("Version")[0]
			v = vers.firstChild.data[:]
			doc.unlink()
			return v
		except:
			return ""
	
	def _get_parent(self, parent, item):
		t = parent.firstChild()
		while t:
			if t.text(0) == item:
				return t
			t = t.nextSibling()
		return QListViewItem(parent, item)
	
	def _add_pak(self, dir):
		t = dir[len(self.main_path):].split("/")
		pn = t[-1]
		parent = self.list
		if len(t) > 1:
			for d in t[:-1]:
				if d != "":
					parent = self._get_parent(parent, d)
					parent.path = None
		p = QListViewItem(parent, pn, self._get_version(dir))
		p.path = dir
	
	def scan_dir(self, dirname):
		# reset
		self.main_path = dirname
		self.list.clear()
		# populate the list
		for root, dirs, files in os.walk(dirname):
			if "pspec.xml" in files:
				self._add_pak(root)
				# found a package, dont go deeper
				for d in dirs:
					dirs.remove(d)
			# dont walk into the versioned stuff
			if ".svn" in dirs:
				dirs.remove(".svn")
	
	def edit(self):
		item = self.list.selectedItem()
		if item == None or item.path == None:
			return
		p = pakedit.PakEdit(None)
		p.edit_pak(item.path)
		p.show()
		self.winlist.append(p)
	
	def _getpath(self):
		item = self.list.selectedItem()
		if item == None:
			return self.main_path
		if item.path != None:
			item = item.parent()
		t = ""
		while item != None:
			t = os.path.join(str(item.text(0)), t)
			item = item.parent()
		return os.path.join(self.main_path, t)
	
	def create(self):
		t = QInputDialog.getText("Create a new package", "Name", QLineEdit.Normal)
		if t[1] == False:
			return
		pname = str(t[0])
		pdir = os.path.join(self._getpath(), pname)
		if os.path.exists(pdir):
			print "Doh!"
			return
		os.mkdir(pdir)
		self._add_pak(pdir)
		p = pakedit.PakEdit(None)
		p.edit_pak(pdir)
		p.show()
		self.winlist.append(p)

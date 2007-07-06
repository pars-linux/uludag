#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

import os

from qt import *

class DirView(QListView):
    def __init__(self, parent, dirname, folders):
        QListView.__init__(self, parent)
        self.addColumn("Name", 500)
        self.addColumn("Size", 60)
        self.setRootIsDecorated(True)
        self.roots = []
        for text, path in folders:
            root = DirViewItem(self, path)
            root.setText(0, text)
            root.addChildren()
            self.roots.append(root)
        
        self.connect(self, SIGNAL("expanded(QListViewItem*)"), self.expand)
        self.connect(self, SIGNAL("collapsed(QListViewItem*)"), self.collapse)
        
    def expand(self, item):
        item.expand()
        
    def collapse(self, item):
        item.collapse()

class DirViewItem(QCheckListItem):
    ignoreList = ["desktop.ini", "thumbs.db", "$Recycled.Bin"]
    def __init__(self, parent, name):
        QCheckListItem.__init__(self, parent, name, QCheckListItem.CheckBoxController)
        self.name = name
        self.setText(0, os.path.basename(name).decode("utf-8"))
        self.setTristate(True)
        self.children = []
        self.size = 0
        if os.path.isdir(self.name):
            self.type = "dir"
            self.pix = QPixmap("/usr/share/icons/Tulliana-2.0/16x16/actions/folder.png")
        else:
            self.type = "file"
            self.pix = QPixmap("/usr/share/icons/Tulliana-2.0/16x16/mimetypes/empty.png")
            self.size = os.path.getsize(self.name)
            self.writeSize()
        self.setPixmap(0, self.pix)
        
    def addChildren(self):
        if os.path.isdir(self.name):
            filelist = os.listdir(self.name)
            for thefile in filelist:
                if thefile in DirViewItem.ignoreList:
                    continue
                realname = os.path.join(self.name, thefile)
                child = DirViewItem(self, realname)
                self.children.append(child)
                
    def expand(self):
        self.setOpen(1)
        self.setPixmap(0, QPixmap("/usr/share/icons/Tulliana-2.0/16x16/actions/fileopen.png"))
        # Add grand children:
        for child in self.children:
            if not child.childCount():
                child.addChildren()
                
    def key(self, col, asc):
        if self.type == "dir":
            return "a"+self.name
        else:
            return "b"+self.name
        
    def collapse(self):
        self.setPixmap(0, QPixmap("/usr/share/icons/Tulliana-2.0/16x16/actions/folder.png"))
        
    def writeSize(self):
        if self.size >= 1024 * 1024:
            self.setText(1, "%.1f MB" % (self.size / 1024.0 / 1024))
        elif self.size >= 1024:
            self.setText(1, "%.1f KB" % (self.size / 1024.0))
        elif self.size:
            self.setText(1, "%d B" % self.size)
        
    def selectedFiles(self):
        files = []
        if self.state() == QCheckListItem.Off:
            return []
        elif self.state() == QCheckListItem.On:
            return [self.name]
        else:
            child = self.firstChild()
            while child:
                files.extend(child.selectedFiles())
                child = child.nextSibling()
            return files

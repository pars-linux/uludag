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

# General Modules
import os

# KDE-Qt Modules
from qt import *
from kdecore import *
from kdeui import *

# Utility Modules
import utility.files


class DirView(QListView):
    "an improved tree-like widget to show files and folders with checkbox"
    def __init__(self, parent):
        "creates view and adds root items"
        QListView.__init__(self, parent)
        self.addColumn(i18n("Name"), 350)
        self.addColumn(i18n("Size"), 80)
        self.setRootIsDecorated(True)
    
        self.connect(self, SIGNAL("expanded(QListViewItem*)"), self.expand)
        self.connect(self, SIGNAL("collapsed(QListViewItem*)"), self.collapse)
    
    def expand(self, item):
        "calls when user expands an item which represents a folder"
        item.expand()
    
    def collapse(self, item):
        "calls when user collapses an item which represents a folder"
        item.collapse()


class DirViewItem(QCheckListItem):
    "an element of DirView which represents a file or directory"
    def __init__(self, parent, path):
        "creates item and sets needed variables like type and size"
        QCheckListItem.__init__(self, parent, path, QCheckListItem.CheckBoxController)
        self.path = path
        self.setText(0, os.path.basename(path).decode("utf-8"))
        self.setTristate(True)
        self.children = []
        self.size = 0
        if os.path.isdir(self.path):
            self.type = "dir"
            self.pix = KGlobal.iconLoader().loadIcon("folder", KIcon.Small)
        elif os.path.isfile(self.path):
            self.type = "file"
            self.pix = KGlobal.iconLoader().loadIcon("file", KIcon.Small)
            self.size = os.path.getsize(self.path)
            self.writeSize()
        self.setPixmap(0, self.pix)
    
    def expand(self):
        "calls when user expands the item"
        self.setOpen(1)
        self.setPixmap(0, KGlobal.iconLoader().loadIcon("fileopen", KIcon.Small))
        # Add grand children:
        for child in self.children:
            if not child.childCount():
                child.addChildren()
    
    def collapse(self):
        "calls when user collapses the item"
        self.setPixmap(0, KGlobal.iconLoader().loadIcon("folder", KIcon.Small))
    
    def activate(self):
        "calls when user click the checkbox"
        KApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        QCheckListItem.activate(self)
        KApplication.restoreOverrideCursor()
    
    def addChildren(self):
        "adds child items of the item"
        KApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        if os.path.isdir(self.path):
            filelist = os.listdir(self.path)
            for thefile in filelist:
                if thefile in utility.files.ignoreList:
                    continue
                realname = os.path.join(self.path, thefile)
                child = DirViewItem(self, realname)
                if self.state() == QCheckListItem.On:
                    child.setState(QCheckListItem.On)
                self.children.append(child)
        KApplication.restoreOverrideCursor()
    
    def compare(self, item2, col, asc):
        "overrides compare function to properly sort files"
        if self.type == "dir" and item2.type != "dir":
            return -1
        elif self.type != "dir" and item2.type == "dir":
            return 1
        else:
            if col == 1:
                return self.size-item2.size
            else:
                return QCheckListItem.compare(self, item2, col, asc)
    
    def writeSize(self):
        "writes human readable version of items size to second column"
        if self.size >= 1024 * 1024:
            self.setText(1, "%.1f MB" % (self.size / 1024.0 / 1024))
        elif self.size >= 1024:
            self.setText(1, "%.1f KB" % (self.size / 1024.0))
        elif self.size:
            self.setText(1, "%d B" % self.size)
    
    def selectedFiles(self):
        "returns a list of selected children of an item"
        files = []
        if self.state() == QCheckListItem.Off:
            return []
        elif self.state() == QCheckListItem.On:
            return [self.path]
        else:
            child = self.firstChild()
            while child:
                files.extend(child.selectedFiles())
                child = child.nextSibling()
            return files


class DirViewRoot(DirViewItem):
    "root folders for DirView class"
    def __init__(self, parent, path, name, localname):
        DirViewItem.__init__(self, parent, path)
        self.setText(0, localname)
        self.name = name
        self.localname = localname
        self.path = path
        self.addChildren()


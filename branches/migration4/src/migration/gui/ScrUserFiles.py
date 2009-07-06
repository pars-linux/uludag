#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
import os
from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyKDE4.kdecore import i18n, KGlobal


from migration.gui.ScreenWidget import ScreenWidget
from migration.gui.ui.userFilesWidget import Ui_userFilesWidget


class DirectoryViewItem(QtGui.QTreeWidgetItem):
    "an element of DirView which represents a file or directory"
    def __init__(self, parent, path):
        "creates item and sets needed variables like type and size"
        QtGui.QTreeWidgetItem.__init__(self, parent, path)
        self.path = path
        self.setText(0, os.path.basename(path).decode("utf-8"))
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

    def setChecked(self, checked):
        if checked:
            self.setCheckState(0, Qt.Checked)
        else:
            self.setCheckState(0, Qt.Unchecked)

    def isChecked(self):
        return self.checkState(0) == Qt.Checked

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
        QtGui.QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        self.setChecked(True)
        QtGui.QApplication.restoreOverrideCursor()

    def addChildren(self):
        "adds child items of the item"
        QtGui.QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        if os.path.isdir(self.path):
            filelist = os.listdir(self.path)
            for thefile in filelist:
                if thefile in utility.files.ignoreList:
                    continue
                realname = os.path.join(self.path, thefile)
                child = DirectoryViewItem(self, realname)
                if self.isChecked():
                    child.setChecked(True)
                self.children.append(child)
        QtGui.QApplication.restoreOverrideCursor()

    def compare(self, item2, col, asc):
        "overrides compare function to properly sort files"
        if self.type == "dir" and item2.type != "dir":
            return -1
        elif self.type != "dir" and item2.type == "dir":
            return 1
        else:
            if col == 1:
                return self.size-item2.size
            #else:
                #TODO:TreeWidgetItem compare

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
        if self.isChecked():
            return [self.path]
        elif not self.isChecked():
            return []
        else:
            childCount = self.childCount()
            for i in range(childCount):
                files.append(self.child(i))
            return files

class DirectoryViewRoot(DirectoryViewItem):
    "root folders for DirView class"
    def __init__(self, parent, path, name, localname):
        DirectoryViewItem.__init__(self, parent, path)
        self.setText(0, localname)
        self.name = name
        self.localname = localname
        self.path = path
        self.addChildren()

class Widget(QtGui.QWidget, ScreenWidget):
    title = i18n("Selecting Files")
    desc = i18n("Welcome to Migration Tool Wizard :)")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_userFilesWidget()
        self.ui.setupUi(self)

        self.connect(self.ui.copy, SIGNAL("clicked(bool checked = false)"), self.slotRadiosClicked)
        self.connect(self.ui.nothing, SIGNAL("clicked(bool checked = false)"), self.slotRadiosClicked)
        self.connect(self.ui.link, SIGNAL("clicked(bool checked = false)"), self.slotRadiosClicked)


    def slotRadiosClicked(self):
        if self.ui.copy.isClicked():
            self.ui.destination.setEnabled(True)
            self.ui.dirview.setEnabled(True)
        elif self.ui.nothing.isClicked():
            self.ui.destination.setEnabled(False)
            self.ui.dirview.setEnabled(False)
        elif self.ui.link.isClicked():
            self.ui.destination.setEnabled(False)
            self.ui.dirview.setEnabled(False)

    def creator(self):
        # Add folders:
        folders = []
        acceptList = [("Personal Path", "My Documents", i18n("My Documents")),
                      ("Desktop Path", "Desktop", i18n("Desktop")),
                      ("My Music Path", "My Music", i18n("My Music")),
                      ("My Pictures Path", "My Pictures", i18n("My Pictures")),
                      ("My Video Path", "My Video", i18n("My Video"))]

        for key, name, localname in acceptList:
            if sources.has_key(key):
                path = sources[key]
                folders.append((path, name, unicode(localname)))

        # Check if one dir includes another:
        for index, (path, name, localname) in enumerate(folders):
            unique = True
            for index2, (path2, name2, localname2) in enumerate(folders):
                # If this is a child, skip
                if path.find(path2) == 0 and index != index2:
                    unique = False
                    break
            if unique:
                DirectoryViewRoot(self.dirview, path, name, localname)

    def getOptions(self):
        options = {}
        if self.ui.link.isChecked():
            links = []
            for index in xrange(self.ui.dirview.topLevelItemCount()):
                child = self.ui.dirview.topLevelItem(index)
                if child.isChecked():
                    child.setHidden(False)
                    links.append({"path":child.path, "name":child.name, "localname":child.localname})

            options["links"] = links

        elif self.copy.isChecked():
            folders = []
            for index in xrange(self.ui.dirview.topLevelItemCount()):
                child = self.ui.dirview.topLevelItem(index)
                if child.isChecked():
                    child.setHidden(False)
                    files = child.selectedFiles()
                    folders.append({"name":child.name, "localname":child.localname, "source":child.path, "files":files})

            options["folders"] = folders
            options["copy destination"] = unicode(self.destination.text())
        return options

    def shown(self):
        pass

    def execute(self):
        self.options = self.getOptions()

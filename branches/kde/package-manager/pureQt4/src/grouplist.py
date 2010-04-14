#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

from PyQt4 import QtGui
from PyQt4.QtCore import *

import backend

from context import *

UPDATE_TYPES = backend.pm.UPDATE_TYPES

class GroupList(QtGui.QListWidget):
    def __init__(self, parent=None):
        QtGui.QListWidget.__init__(self, parent)
        self.lastSelected = None
        self.iface = backend.pm.Iface()
        self.connect(self, SIGNAL("itemClicked(QListWidgetItem*)"), self.groupChanged)

    def setState(self, state):
        self.state = state

    def addGroups(self, groups):
        for name in groups:
            self.createGroupItem(name)
        self.sortItems()
        self.moveAllToFirstLine()
        self.ensureGroupSelected()

    def createGroupItem(self, name):
        if not name.startswith('type:'):
            group = self.iface.getGroup(name)
            localName, icon_path = unicode(group.localName), group.icon
            package_count = len(self.state.groupPackages(name))
            if package_count == 0:
                return
        else:
            localName, icon_path = unicode(UPDATE_TYPES[name][0]), UPDATE_TYPES[name][1]
            package_count = 22
            if package_count == 0:
                return

        icon = KIcon(icon_path, KIconLoader.SizeSmallMedium)
        item = QtGui.QListWidgetItem(icon, "%s (%d)" % (localName, package_count), self)
        item.setData(Qt.UserRole, QVariant(unicode(name)))
        item.setSizeHint(QSize(0, KIconLoader.SizeMedium))

        if str(self.lastSelected) == name:
            self.selectLastSelected(item)

    def selectLastSelected(self, item):
        self.setCurrentItem(item)

    def moveAllToFirstLine(self):
        if not self.count():
            return
        for i in range(self.count()):
            key = self.item(i).data(Qt.UserRole).toString()
            if key == "all":
                item = self.takeItem(i)
                self.insertItem(0, item)
            elif key in UPDATE_TYPES.keys():
                item = self.takeItem(i)
                self.insertItem(UPDATE_TYPES.keys().index(key), item)

    def ensureGroupSelected(self):
        if self.currentRow() == -1 and self.count():
            self.selectLastSelected(self.itemAt(0, 0))

    def currentGroup(self):
        if not self.count():
            return None
        return unicode(self.currentItem().data(Qt.UserRole).toString())

    def groupChanged(self):
        self.lastSelected = self.currentGroup()
        self.emit(SIGNAL("groupChanged()"))

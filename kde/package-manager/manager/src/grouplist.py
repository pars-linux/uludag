#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009-2010, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import backend

from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QSize
from PyQt4.QtCore import QVariant

from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QListWidget
from PyQt4.QtGui import QListWidgetItem

from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

from statemanager import StateManager

class GroupList(QListWidget):
    def __init__(self, parent=None):
        QListWidget.__init__(self, parent)
        self.iface = backend.pm.Iface()
        self.defaultIcon = QIcon(KIcon('applications-other').pixmap(
                            KIconLoader.SizeSmallMedium))
        self.connect(self, SIGNAL("itemClicked(QListWidgetItem*)"),
                            self.groupChanged)

    def setState(self, state):
        self.state = state

    def addGroups(self, groups):
        if groups:
            for name in groups:
                self.createGroupItem(name)
        else:
            self.createGroupItem('all',
                    (i18n('All'), 'media-optical', len(self.state.packages())))
        self.sortItems()
        self.moveAllToFirstLine()
        self.setCurrentItem(self.itemAt(0, 0))

    def createGroupItem(self, name, content = None):
        if not content:
            group = self.iface.getGroup(name)
            localName, icon_path = unicode(group.localName), group.icon
            package_count = len(self.state.groupPackages(name))
            if package_count <= 0:
                return
        else:
            localName, icon_path = content[0], content[1]
            package_count = content[2]

        icon = QIcon(KIcon(icon_path).pixmap(KIconLoader.SizeSmallMedium))
        if icon.isNull():
            icon = self.defaultIcon
        item = QListWidgetItem(icon, "%s (%d)" % (localName, package_count),
                               self)
        item.setData(Qt.UserRole, QVariant(unicode(name)))
        item.setSizeHint(QSize(0, KIconLoader.SizeMedium))

    def moveAllToFirstLine(self):
        if not self.count():
            return

        for i in range(self.count()):
            key = self.item(i).data(Qt.UserRole).toString()
            if key == "all":
                item = self.takeItem(i)
                self.insertItem(0, item)

    def currentGroup(self):
        if not self.count():
            return
        if self.currentItem():
            return unicode(self.currentItem().data(Qt.UserRole).toString())

    def groupChanged(self):
        self.emit(SIGNAL("groupChanged()"))


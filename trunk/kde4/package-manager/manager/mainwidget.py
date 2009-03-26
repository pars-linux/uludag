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

from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

from ui_mainwidget import Ui_MainWidget

from packageproxy import PackageProxy
from packagemodel import PackageModel, GroupRole
from packagedelegate import PackageDelegate

import backend

class MainWidget(QtGui.QWidget, Ui_MainWidget):
    def __init__(self, parent, standAlone=True):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.iface = backend.pm.Iface()
        self.initialize()

    def initialize(self):
        self.initializePackageList()
        self.initializeComponentList()
        self.connect(self.searchLine, SIGNAL("textChanged(const QString&)"), self.packageFilter)

    def initializePackageList(self):
        self.packageList.setModel(PackageProxy(self))
        self.packageList.model().setSourceModel(PackageModel(self))
        self.packageList.setItemDelegate(PackageDelegate(self))
        self.packageList.setColumnWidth(0, 32)
        self.packageList.setAlternatingRowColors(True)

    def initializeComponentList(self):
        self.componentList.setAlternatingRowColors(True)
        self.componentList.setIconSize(QSize(KIconLoader.SizeLarge, KIconLoader.SizeLarge))
        for group in self.iface.getGroups():
            self.createComponentItem(group)
        self.connect(self.componentList, SIGNAL("itemClicked(QListWidgetItem*)"), self.componentFilter)

    def createComponentItem(self, group):
        name, icon_path = group["name"], group["icon"]
        package_count = len(self.iface.getGroupPackages(name))
        icon = QtGui.QIcon(KIconLoader().loadMimeTypeIcon(icon_path, KIconLoader.Desktop, KIconLoader.SizeSmallMedium))
        item = QtGui.QListWidgetItem(icon, "%s (%d)" % (name, package_count), self.componentList)
        item.setData(Qt.UserRole, QVariant(unicode(name)))
        item.setSizeHint(QSize(0, KIconLoader.SizeMedium))

    def packageFilter(self, text):
        self.packageList.model().setFilterRole(Qt.DisplayRole)
        self.packageList.model().setFilterRegExp(QRegExp(unicode(text), Qt.CaseInsensitive, QRegExp.FixedString))

    def componentFilter(self, item):
        packages = self.iface.getGroupPackages(item.data(Qt.UserRole).toString())
        self.packageList.model().setFilterRole(GroupRole)
        self.packageList.model().setFilterPackages(packages)

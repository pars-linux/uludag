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

# Qt Stuff
from PyQt4 import QtGui
from PyQt4.QtCore import *

# PyKDE4 Stuff
from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

# Application Stuff
from uimain import Ui_MainManager
from uiitem import Ui_PackageWidget

from packageproxy import PackageProxy
from packagemodel import PackageModel, GroupRole
from packagedelegate import PackageDelegate

import pmtools

class MainManager(QtGui.QWidget):
    def __init__(self, parent, standAlone=True):
        QtGui.QWidget.__init__(self, parent)

        # Create the ui
        self.ui = Ui_MainManager()

        if standAlone:
            self.ui.setupUi(self)
        else:
            self.ui.setupUi(parent)

        self.iface = pmtools.Iface()

        # Initialize
        self.initialize()

    def initializePackageList(self):
        abstractModel = PackageProxy(self)
        abstractModel.setSourceModel(PackageModel(self))
        self.ui.packageList.setModel(abstractModel)
        self.ui.packageList.setItemDelegate(PackageDelegate(self))
        self.ui.packageList.setColumnWidth(0, 32)
        self.ui.packageList.setAlternatingRowColors(True)

    def initializeComponentList(self):
        self.ui.componentList.setAlternatingRowColors(True)
        self.ui.componentList.setIconSize(QSize(KIconLoader.SizeLarge, KIconLoader.SizeLarge))
        for group in self.iface.getGroups():
            name, icon_path = group["name"], group["icon"]
            package_count = len(self.iface.getGroupPackages(name))
            icon = QtGui.QIcon(KIconLoader().loadMimeTypeIcon(icon_path, KIconLoader.Desktop, KIconLoader.SizeSmallMedium))
            item = QtGui.QListWidgetItem(icon, "%s (%d)" % (name, package_count), self.ui.componentList)
            item.setData(Qt.UserRole, QVariant(unicode(name)))
            item.setSizeHint(QSize(0, KIconLoader.SizeMedium))
        self.connect(self.ui.componentList, SIGNAL("itemClicked(QListWidgetItem*)"), self.componentFilter)

    def initialize(self):
        self.initializePackageList()
        self.initializeComponentList()
        self.connect(self.ui.searchLine, SIGNAL("textChanged(const QString&)"), self.packageFilter)

    def packageFilter(self, text):
        text = unicode(text)
        self.ui.packageList.model().setFilterRole(Qt.DisplayRole)
        self.ui.packageList.model().setFilterRegExp(QRegExp(text, Qt.CaseInsensitive, QRegExp.FixedString))

    def componentFilter(self, item):
        packages = self.iface.getGroupPackages(item.data(Qt.UserRole).toString())
        self.ui.packageList.model().setFilterRole(GroupRole)
        self.ui.packageList.model().setFilterPackages(packages)

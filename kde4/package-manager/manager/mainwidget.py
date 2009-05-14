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
from statemanager import StateManager

from pmutils import *

class MainWidget(QtGui.QWidget, Ui_MainWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.state = StateManager(self)
        self.lastSelectedGroup = None
        self.initialize()

        self.connect(self.searchLine, SIGNAL("textChanged(const QString&)"), self.packageFilter)
        self.connect(self.packageList.model(), SIGNAL("dataChanged(QModelIndex,QModelIndex)"), self.selectionChanged)
        self.connect(self.groupList, SIGNAL("itemClicked(QListWidgetItem*)"), self.componentFilter)

    def initialize(self):
        self.initializePackageList()
        self.initializeComponentList()
        self.ensureGroupSelected()

    def initializePackageList(self):
        self.packageList.setModel(PackageProxy(self))
        self.packageList.model().setSourceModel(PackageModel(self))
        self.packageList.setItemDelegate(PackageDelegate(self))
        self.packageList.setColumnWidth(0, 32)
        self.packageList.setAlternatingRowColors(True)
        self.packageList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.packageList.setPackages(self.state.packages())

    def initializeComponentList(self):
        self.groupList.clear()
        self.groupList.setAlternatingRowColors(True)
        self.groupList.setIconSize(QSize(KIconLoader.SizeLarge, KIconLoader.SizeLarge))

        for group in self.state.groups():
            self.createComponentItem(group)

    def createComponentItem(self, group):
        name, icon_path = group["name"], group["icon"]

        package_count = len(self.state.groupPackages(name))
        if package_count == 0:
            return

        icon = QtGui.QIcon(KIconLoader().loadMimeTypeIcon(icon_path, KIconLoader.Desktop, KIconLoader.SizeSmallMedium))
        item = QtGui.QListWidgetItem(icon, "%s (%d)" % (name, package_count), self.groupList)
        item.setData(Qt.UserRole, QVariant(unicode(name)))
        item.setSizeHint(QSize(0, KIconLoader.SizeMedium))

        if str(self.lastSelectedGroup) == name:
            self.selectLastGroup(item)

    def selectLastGroup(self, item):
        self.groupList.setCurrentItem(item)
        self.componentFilter(item)

    def ensureGroupSelected(self):
        if self.groupList.currentRow() == -1 and self.groupList.count():
            self.selectLastGroup(self.groupList.itemAt(0, 0))

    def packageFilter(self, text):
        self.packageList.model().setFilterRole(Qt.DisplayRole)
        self.packageList.model().setFilterRegExp(QRegExp(unicode(text), Qt.CaseInsensitive, QRegExp.FixedString))

    def componentFilter(self, item):
        self.lastSelectedGroup = item.data(Qt.UserRole).toString()
        packages = self.state.groupPackages(self.lastSelectedGroup)
        self.packageList.model().setFilterRole(GroupRole)
        self.packageList.model().setFilterPackages(packages)

    def selectionChanged(self):
        self.emit(SIGNAL("selectionChanged(QModelIndexList)"), self.packageList.selectionModel().selectedIndexes())

    def switchState(self, state):
        try:
            waitCursor()
            self.state.setState(state)
            self.initialize()
        finally:
            restoreCursor()

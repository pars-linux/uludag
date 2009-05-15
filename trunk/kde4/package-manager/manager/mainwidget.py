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
        self.initialize()

        self.connect(self.actionButton, SIGNAL("clicked()"), self.takeAction)
        self.connect(self.searchLine, SIGNAL("textChanged(const QString&)"), self.packageFilter)
        self.connect(self.groupList, SIGNAL("groupChanged()"), self.groupFilter)
        self.connect(self.packageList.model(), SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                     lambda:self.emit(SIGNAL("selectionChanged(QModelIndexList)"),
                            self.packageList.selectionModel().selectedIndexes()))

    def initialize(self):
        self.initializePackageList()
        self.initializeGroupList()

    def initializePackageList(self):
        self.packageList.setModel(PackageProxy(self))
        self.packageList.model().setSourceModel(PackageModel(self))
        self.packageList.setItemDelegate(PackageDelegate(self))
        self.packageList.setColumnWidth(0, 32)
        self.packageList.setAlternatingRowColors(True)
        self.packageList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.packageList.setPackages(self.state.packages())

    def initializeGroupList(self):
        self.groupList.clear()
        self.groupList.setAlternatingRowColors(True)
        self.groupList.setIconSize(QSize(KIconLoader.SizeLarge, KIconLoader.SizeLarge))
        self.groupList.setState(self.state)
        self.groupList.addGroups(self.state.groups())
        self.groupFilter()

    def packageFilter(self, text):
        self.packageList.model().setFilterRole(Qt.DisplayRole)
        self.packageList.model().setFilterRegExp(QRegExp(unicode(text), Qt.CaseInsensitive, QRegExp.FixedString))

    def groupFilter(self):
        packages = self.state.groupPackages(self.groupList.currentGroup())
        self.packageList.model().setFilterRole(GroupRole)
        self.packageList.model().setFilterPackages(packages)

    def setActionButton(self):
        self.actionButton.setText(self.state.getActionName())
        self.actionButton.setIcon(self.state.getActionIcon())

    def takeAction(self):
        self.state.takeAction(self.packageList.selectedPackages())
        self.switchState(self.state.getState())

    def switchState(self, state):
        try:
            waitCursor()
            self.state.setState(state)
            self.setActionButton()
            self.initialize()
        finally:
            restoreCursor()

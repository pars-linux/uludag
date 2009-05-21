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
from progressdialog import ProgressDialog
from statemanager import StateManager
from operationmanager import OperationManager

from pmutils import *

class MainWidget(QtGui.QWidget, Ui_MainWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.state = StateManager(self)
        self.operation = OperationManager(self.state)
        self.progressDialog = ProgressDialog(self.state)
        self.initialize()
        self.connectMainSignals()
        self.connectOperationSignals()

    def connectMainSignals(self):
        self.connect(self.actionButton, SIGNAL("clicked()"), self.actionStart)
        self.connect(self.searchLine, SIGNAL("textChanged(const QString&)"), self.packageFilter)
        self.connect(self.groupList, SIGNAL("groupChanged()"), self.groupFilter)
        self.connect(self.packageList.model(), SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                     lambda:self.emit(SIGNAL("selectionChanged(QModelIndexList)"),
                            self.packageList.selectionModel().selectedIndexes()))

    def connectOperationSignals(self):
        self.connect(self.operation, SIGNAL("finished(QString)"), self.actionFinished)
        self.connect(self.operation, SIGNAL("started()"), self.progressDialog.enableCancel)
        self.connect(self.operation, SIGNAL("started()"), self.progressDialog.show)
        self.connect(self.operation, SIGNAL("progress(int)"), self.progressDialog.updateProgress)
        self.connect(self.operation, SIGNAL("operationChanged(QString,QString)"), self.progressDialog.updateOperation)
        self.connect(self.operation, SIGNAL("packageChanged(int, int, QString)"), self.progressDialog.updateStatus)

    def initialize(self):
        waitCursor()
        self.initializePackageList()
        self.initializeGroupList()
        restoreCursor()

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
        waitCursor()
        self.packageList.model().setFilterPackages(packages)
        restoreCursor()

    def setActionButton(self):
        self.actionButton.setText(self.state.getActionName())
        self.actionButton.setIcon(self.state.getActionIcon())

    def actionStart(self):
        self.progressDialog.show()
        self.state.operationAction(self.packageList.selectedPackages())

    def actionFinished(self, operation):
        self.progressDialog.hide()
        self.initialize()

    def switchState(self, state):
        self.state.setState(state)
        self.setActionButton()
        self.state.stateAction()

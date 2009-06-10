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
from summarydialog import SummaryDialog
from operationmanager import OperationManager
from basketdialog import BasketDialog

from pmutils import *

class MainWidget(QtGui.QWidget, Ui_MainWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.state = StateManager(self)
        self.basket = BasketDialog(self.state)
        self.initialize()
        self.setSelectAll()
        self.actionButton.setIcon(self.state.getActionIcon())
        self.operation = OperationManager(self.state)
        self.progressDialog = ProgressDialog(self.state)
        self.summaryDialog = SummaryDialog(self.operation, self.state)
        self.connectMainSignals()
        self.connectOperationSignals()

    def connectMainSignals(self):
        self.connect(self.actionButton, SIGNAL("clicked()"), self.basket.show)
        self.connect(self.searchLine, SIGNAL("textEdited(const QString&)"), self.packageFilter)
        self.connect(self.groupList, SIGNAL("groupChanged()"), self.groupFilter)
        self.connect(self.selectAll, SIGNAL("leftClickedUrl(const QString&)"), self.toggleSelectAll)

    def connectOperationSignals(self):
        self.connect(self.operation, SIGNAL("finished(QString)"), self.actionFinished)
        self.connect(self.operation, SIGNAL("started(QString)"), self.actionStarted)
        self.connect(self.operation, SIGNAL("started(QString)"), self.progressDialog.updateActionLabel)
        self.connect(self.operation, SIGNAL("progress(int)"), self.progressDialog.updateProgress)
        self.connect(self.operation, SIGNAL("operationChanged(QString,QString)"), self.progressDialog.updateOperation)
        self.connect(self.operation, SIGNAL("packageChanged(int, int, QString)"), self.progressDialog.updateStatus)
        self.connect(self.operation, SIGNAL("elapsedTime(QString)"), self.progressDialog.updateRemainingTime)
        self.connect(self.operation, SIGNAL("downloadInfoChanged(QString, QString, QString)"), self.progressDialog.updateCompletedInfo)

    def initialize(self):
        waitCursor()
        self.initializePackageList()
        self.initializeGroupList()
        self.initializeBasket()
        self.emit(SIGNAL("selectionStatusChanged(QString)"), self.selectedStatus())
        restoreCursor()

    def initializeBasket(self):
        self.basket.setModel(self.packageList.model().sourceModel())

    def initializePackageList(self):
        self.packageList.setModel(PackageProxy(self))
        self.packageList.model().setSourceModel(PackageModel(self))
        self.packageList.setItemDelegate(PackageDelegate(self))
        self.packageList.setColumnWidth(0, 32)
        self.packageList.setAlternatingRowColors(True)
        self.packageList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.packageList.setPackages(self.state.packages())
        self.connect(self.packageList.model(), SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                     lambda:self.emit(SIGNAL("selectionStatusChanged(QString)"), self.selectedStatus()))

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
        self.setSelectAll()
        packages = self.state.groupPackages(self.groupList.currentGroup())
        self.packageList.model().setFilterRole(GroupRole)
        waitCursor()
        self.packageList.model().setFilterPackages(packages)
        restoreCursor()

    def setActionButton(self):
        self.actionButton.setEnabled(False)
        self.actionButton.setText(self.state.getActionName())
        self.actionButton.setIcon(self.state.getActionIcon())

    def actionStarted(self, operation):
        totalPackages = self.packageList.packageCount()
        self.operation.setTotalPackages(totalPackages)
        self.progressDialog.reset()
        self.progressDialog.updateStatus(0, totalPackages, self.state.toBe())
        self.progressDialog.show()
        self.progressDialog.enableCancel()

    def actionFinished(self, operation):
        self.searchLine.clear()
        self.state.reset()
        self.progressDialog.hide()
        if self.state.infoNeeded(operation):
            self.summaryDialog.show()
        self.initialize()

    def setActionEnabled(self):
        enabled = bool(self.packageList.packageCount())
        self.actionButton.setEnabled(enabled)
        self.basket.setActionEnabled(enabled)

    def switchState(self, state):
        self.setSelectAll()
        self.searchLine.clear()
        self.state.setState(state)
        self.setActionButton()
        self.state.stateAction()

    def selectedStatus(self):
        waitCursor()
        status = self.state.selectedStatus(self.packageList.model().sourceModel())
        self.setActionEnabled()
        restoreCursor()
        return status

    def setSelectAll(self, packages=None):
        if packages:
            self.packageList.reverseSelection(packages)
        self.selectAll.setText(i18n("Select all packages in this group"))
        self.selectAll.setUrl("All")

    def setReverseAll(self, packages=None):
        if packages:
            self.packageList.selectAll(packages)
        self.selectAll.setText(i18n("Reverse package selections"))
        self.selectAll.setUrl("Reverse")

    def toggleSelectAll(self, text):
        packages = self.state.groupPackages(self.groupList.currentGroup())
        if text == "All":
            self.setReverseAll(packages)
        else:
            self.setSelectAll(packages)
        self.emit(SIGNAL("selectionStatusChanged(QString)"), self.selectedStatus())

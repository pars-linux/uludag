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

from context import *
from context import _time

if Pds.session == pds.Kde4:
    from ui_mainwidget_kde4 import Ui_MainWidget
else:
    from ui_mainwidget_x11 import Ui_MainWidget

from packageproxy import PackageProxy
from packagemodel import PackageModel, GroupRole
from packagedelegate import PackageDelegate
from progressdialog import ProgressDialog
from statemanager import StateManager
from summarydialog import SummaryDialog
from operationmanager import OperationManager
from basketdialog import BasketDialog
from statusupdater import StatusUpdater

from pmutils import *
import config

UPDATE_TYPES = [['normal',   i18n('All Updates'), 'system-software-update'],
                ['security', i18n('Security Updates'),    'security-medium'],
                ['critical', i18n('Critical Updates'),    'security-low']]

class MainWidget(QtGui.QWidget, Ui_MainWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.searchButton.setIcon(KIcon("edit-find"))
        self.statusUpdater = StatusUpdater()
        self.state = StateManager(self)
        self.basket = BasketDialog(self.state)
        self.initialize()
        self.updateSettings()
        self.actionButton.setIcon(self.state.getActionIcon())
        self.operation = OperationManager(self.state)
        self.progressDialog = ProgressDialog(self.state)
        self.summaryDialog = SummaryDialog()
        self.connectMainSignals()
        self.connectOperationSignals()

    def connectMainSignals(self):
        self.connect(self.actionButton, SIGNAL("clicked()"), self.showBasket)
        self.connect(self.searchButton, SIGNAL("clicked()"), self.searchActivated)
        self.connect(self.searchLine, SIGNAL("textEdited(const QString&)"), self.searchLineChanged)
        self.connect(self.searchLine, SIGNAL("returnPressed()"), self.searchActivated)
        self.connect(self.searchLine, SIGNAL("clearButtonClicked()"), self.groupFilter)
        self.connect(self.typeCombo, SIGNAL("activated(int)"), self.typeFilter)
        self.connect(self.groupList, SIGNAL("groupChanged()"), self.groupFilter)
        self.connect(self.groupList, SIGNAL("groupChanged()"), self.searchLine.clear)
        self.connect(self.groupList, SIGNAL("groupChanged()"), lambda:self.searchButton.setEnabled(False))
        self.connect(self.selectAll, SIGNAL("toggled(bool)"), self.toggleSelectAll)
        self.connect(self.statusUpdater, SIGNAL("selectedInfoChanged(int, QString, int, QString)"), self.emitStatusBarInfo)
        self.connect(self.statusUpdater, SIGNAL("finished()"), self.statusUpdated)

    def connectOperationSignals(self):
        self.connect(self.operation, SIGNAL("exception(QString)"), self.exceptionCaught)
        self.connect(self.operation, SIGNAL("finished(QString)"), self.actionFinished)
        self.connect(self.operation, SIGNAL("started(QString)"), self.actionStarted)
        self.connect(self.operation, SIGNAL("started(QString)"), self.progressDialog.updateActionLabel)
        self.connect(self.operation, SIGNAL("operationCancelled()"), self.progressDialog.hide)
        self.connect(self.operation, SIGNAL("progress(int)"), self.progressDialog.updateProgress)
        self.connect(self.operation, SIGNAL("operationChanged(QString,QString)"), self.progressDialog.updateOperation)
        self.connect(self.operation, SIGNAL("packageChanged(int, int, QString)"), self.progressDialog.updateStatus)
        self.connect(self.operation, SIGNAL("elapsedTime(QString)"), self.progressDialog.updateRemainingTime)
        self.connect(self.operation, SIGNAL("downloadInfoChanged(QString, QString, QString)"), self.progressDialog.updateCompletedInfo)

    def initialize(self):
        waitCursor()
        self._last_packages = None
        self.state.reset()
        self.initializeUpdateTypeList()
        self.initializePackageList()
        self.initializeGroupList()
        self.initializeStatusUpdater()
        self.statusChanged()
        restoreCursor()
        QTimer.singleShot(1, self.initializeBasket)

    def initializeUpdateTypeList(self):
        self.typeCombo.clear()
        for type in UPDATE_TYPES:
            self.typeCombo.addItem(KIcon(type[2], KIconLoader.SizeSmallMedium), type[1], QVariant(type[0]))

    def initializeStatusUpdater(self):
        self.statusUpdater.setModel(self.packageList.model().sourceModel())

    def initializeBasket(self):
        waitCursor()
        self.basket.setModel(self.packageList.model().sourceModel())
        restoreCursor()

    def initializePackageList(self):
        model = PackageModel(self)
        proxy = PackageProxy(self)
        proxy.setSourceModel(model)
        self.packageList.setModel(proxy)
        self.packageList.setItemDelegate(PackageDelegate(self))
        self.packageList.setColumnWidth(0, 32)
        self.packageList.setPackages(self.state.packages())
        self.connect(self.packageList.model(), SIGNAL("dataChanged(QModelIndex,QModelIndex)"), self.statusChanged)

    def updateSettings(self):
        self.packageList.showComponents = config.PMConfig().showComponents()
        self.packageList.setFocus()

    def searchLineChanged(self, text):
        self.searchButton.setEnabled(bool(text))

    def statusUpdated(self):
        if self.statusUpdater.needsUpdate:
            self.statusUpdater.needsUpdate = False
            self.statusChanged()

    def statusChanged(self):
        self.setActionEnabled()
        if self.statusUpdater.isRunning():
            self.statusUpdater.needsUpdate = True
        else:
            self.emit(SIGNAL("updatingStatus()"))
            self.statusUpdater.start()

    def initializeGroupList(self):
        self.groupList.clear()
        self.groupList.setAlternatingRowColors(True)
        self.groupList.setIconSize(QSize(KIconLoader.SizeLarge, KIconLoader.SizeLarge))
        self.groupList.setState(self.state)
        self.groupList.addGroups(self.state.groups())
        if self.state.state == self.state.UPGRADE:
            self.typeCombo.show()
        else:
            self.typeCombo.hide()
            self.state._typeFilter = 'normal'
        self.groupFilter()

    def packageFilter(self, text):
        self.packageList.model().setFilterRole(Qt.DisplayRole)
        self.packageList.model().setFilterRegExp(QRegExp(unicode(text), Qt.CaseInsensitive, QRegExp.FixedString))

    def typeFilter(self, index):
        if self.state.state == self.state.UPGRADE:
            filter = self.typeCombo.itemData(index).toString()
            if not self.state._typeFilter == filter:
                self.state._typeFilter = filter
                self.initializeGroupList()

    def groupFilter(self):
        self.packageList.resetMoreInfoRow()
        packages = self.state.groupPackages(self.groupList.currentGroup())
        self.packageList.model().setFilterRole(GroupRole)
        waitCursor()
        self.packageList.model().setFilterPackages(packages)
        restoreCursor()

    def searchActivated(self):
        self.packageList.resetMoreInfoRow()
        waitCursor()
        sourceModel = self.packageList.model().sourceModel()
        searchText  = str(self.searchLine.text()).split()
        self.state.cached_packages = sourceModel.search(searchText)
        self.initializeGroupList()
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
        if self.isVisible():
            if operation in ["System.Manager.updateRepository", "System.Manager.updateAllRepositories"]:
                self.progressDialog.repoOperationView()
            self.progressDialog.show()
        self.progressDialog.enableCancel()

    def exceptionCaught(self, message):
        self.progressDialog.hide()

        if "urlopen error" in message or "Socket Error" in message:
            errorTitle = i18n("Network Error")
            errorMessage = i18n("Please check your network connections and try again.")
        elif "Access denied" in message or "tr.org.pardus.comar.Comar.PolicyKit" in message:
            errorTitle = i18n("Authorization Error")
            errorMessage = i18n("You are not authorized for this operation.")
        elif "HTTP Error 404":
            errorTitle = i18n("Pisi Error")
            errorMessage = i18n("Package not found. It may be upgraded in or removed from the repository. Please try upgrading repository informations.")
        else:
            errorTitle = i18n("Pisi Error")
            errorMessage = message

        self.messageBox = QtGui.QMessageBox(errorTitle, errorMessage, QtGui.QMessageBox.Critical, QtGui.QMessageBox.Ok, 0, 0)
        self.messageBox.show()

    def actionFinished(self, operation):
        self.searchLine.clear()
        self.state.reset()
        self.progressDialog.hide()
        if operation == "System.Manager.installPackage":
            self.showSummary()
        if operation in ("System.Manager.installPackage", "System.Manager.removePackage", "System.Manager.updatePackage"):
            self.notifyFinished()
        if operation in ("System.Manager.updateRepository", "System.Manager.updateAllRepositories"):
            self.emit(SIGNAL("repositoriesUpdated()"))
        self.initialize()

    def notifyFinished(self):
        # Since we can not identify the caller yet
        if not self.operation.totalPackages:
            return
        if Pds.session == pds.Kde4:
            from PyKDE4.kdeui import KNotification
            from PyKDE4.kdecore import KComponentData
            KNotification.event("Summary",
                    self.state.getSummaryInfo(self.operation.totalPackages),
                    QtGui.QPixmap(),
                    None,
                    KNotification.CloseOnTimeout,
                    KComponentData("package-manager", "package-manager", KComponentData.SkipMainComponentRegistration)
                    )
        else:
            Pds.notify(i18n('Package Manager'), self.state.getSummaryInfo(self.operation.totalPackages))

    def showSummary(self):
        self.summaryDialog.setDesktopFiles(self.operation.desktopFiles)
        if self.summaryDialog.hasApplication():
            self.summaryDialog.show()

    def setActionEnabled(self):
        enabled = self.packageList.isSelected()
        self.actionButton.setEnabled(enabled)
        self.basket.setActionEnabled(enabled)

    def switchState(self, state, action=True):
        self.searchLine.clear()
        self.state.setState(state)
        self.setActionButton()
        if action:
            self.state.stateAction()

    def emitStatusBarInfo(self, packages, packagesSize, extraPackages, extraPackagesSize):
        self.emit(SIGNAL("selectionStatusChanged(QString)"), self.state.statusText(packages, packagesSize, extraPackages, extraPackagesSize))

    def setSelectAll(self, packages=None):
        if packages:
            self.packageList.reverseSelection(packages)

    def setReverseAll(self, packages=None):
        if packages:
            self.packageList.selectAll(packages)

    def toggleSelectAll(self, toggled):
        if toggled:
            if not self._last_packages:
                self._last_packages = self.packageList.model().getFilteredPackages()
            self.setReverseAll(self._last_packages)
        else:
            self._last_packages = self.packageList.model().getFilteredPackages()
            self.setSelectAll(self._last_packages)
        # A hacky solution to repaint the list to take care of selection changes
        # FIXME Later
        self.packageList.setFocus()

        self.statusChanged()

    def showBasket(self):
        waitCursor()
        self.statusUpdater.wait()
        self.basket.show()
        restoreCursor()

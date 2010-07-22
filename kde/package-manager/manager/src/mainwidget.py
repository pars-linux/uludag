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

from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import qApp

from PyQt4.QtCore import Qt
from PyQt4.QtCore import QSize
from PyQt4.QtCore import QTimer
from PyQt4.QtCore import QVariant
from PyQt4.QtCore import QRegExp
from PyQt4.QtCore import SIGNAL

from context import *
from context import _time

from ui_mainwidget_v3 import Ui_MainWidget

from packageproxy import PackageProxy
from packagemodel import PackageModel
from packagemodel import GroupRole
from packagedelegate import PackageDelegate
from progressdialog import ProgressDialog
from statemanager import StateManager
from summarydialog import SummaryDialog
from operationmanager import OperationManager
from basketdialog import BasketDialog
from statusupdater import StatusUpdater

import config
from pmutils import waitCursor
from pmutils import restoreCursor

class MainWidget(QWidget, Ui_MainWidget):
    def __init__(self, parent=None, silence = False):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self._selectedGroups = []
        self.state = StateManager(self)
        self.lastState = self.state.state
        self.state.silence = silence
        if not silence:
            self.searchButton.setIcon(KIcon("edit-find"))
            self.statusUpdater = StatusUpdater()
            self.basket = BasketDialog(self.state)
            self.searchUsed = False
            self.initializeInfoBox()
            self.initialize()
            self.updateSettings()
            self.actionButton.setIcon(self.state.getActionIcon())
            self.connectMainSignals()
        self.operation = OperationManager(self.state)
        self.progressDialog = ProgressDialog(self.state)
        self.summaryDialog = SummaryDialog()
        self.connectOperationSignals()

        self.typeFilter.addItem(KIcon("view-refresh"), i18n("Show Installable Packages"))
        self.typeFilter.addItem(KIcon("list-remove"), i18n("Show Installed Packages"))
        self.typeFilter.addItem(KIcon("list-add"), i18n("Show Upgradable Packages"))
        self.typeFilter.activated.connect(self.switchState)

    def initializeInfoBox(self):
        # An info label to show a proper information,
        # if there is no updates available.
        self.info = QLabel(self)
        self.info.setText(i18n("All Packages are up to date"))
        self.info.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        self.info.setStyleSheet("background-color:rgba(0,0,0,220); \
                                 color:white; \
                                 border: 1px solid white; \
                                 border-top-left-radius: 10px; \
                                 border-top-right-radius: 10px; \
                                ")
        self.info.resize(self.size())
        self.info.hide()

    #def resizeEvent(self, event):
        # info label should be resized automatically,
        # if the mainwindow resized.
        #width = self.width()
        #height = 40
        #self.info.resize(QSize(width, height))
        #self.info.move(0,self.height()-height)#self.width() / 2 - 170, self.height() / 2 - 40)

    def connectMainSignals(self):
        self.connect(self.actionButton, SIGNAL("clicked()"), self.showBasket)
        self.connect(self.searchButton, SIGNAL("clicked()"), self.searchActivated)
        self.connect(self.searchLine, SIGNAL("textEdited(const QString&)"), self.searchLineChanged)
        self.connect(self.searchLine, SIGNAL("returnPressed()"), self.searchActivated)
        self.connect(self.searchLine, SIGNAL("clearButtonClicked()"), self.groupFilter)
        # self.connect(self.typeCombo, SIGNAL("activated(int)"), self.typeFilter)
        self.connect(self.groupList, SIGNAL("groupChanged()"), self.groupFilter)
        self.connect(self.groupList, SIGNAL("groupChanged()"), lambda:self.searchButton.setEnabled(False))
        self.connect(self.selectAll, SIGNAL("clicked(bool)"), self.toggleSelectAll)
        self.connect(self.statusUpdater, SIGNAL("selectedInfoChanged(int, QString, int, QString)"), self.emitStatusBarInfo)
        self.connect(self.statusUpdater, SIGNAL("selectedInfoChanged(QString)"), lambda message: self.emit(SIGNAL("selectionStatusChanged(QString)"), message))
        self.connect(self.statusUpdater, SIGNAL("finished()"), self.statusUpdated)

    def connectOperationSignals(self):
        self.connect(self.operation, SIGNAL("exception(QString)"), self.exceptionCaught)
        self.connect(self.operation, SIGNAL("finished(QString)"), self.actionFinished)
        self.connect(self.operation, SIGNAL("started(QString)"), self.actionStarted)
        self.connect(self.operation, SIGNAL("started(QString)"), self.progressDialog.updateActionLabel)
        self.connect(self.operation, SIGNAL("operationCancelled()"), self.actionCancelled)
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
        self._selectedGroups = []
        self.selectAll.setChecked(False)
        restoreCursor()
        QTimer.singleShot(1, self.initializeBasket)

    def initializeUpdateTypeList(self):
        self.typeCombo.clear()
        UPDATE_TYPES = [['normal', i18n('All Updates'), 'system-software-update'],
                        ['security', i18n('Security Updates'), 'security-medium'],
                        ['critical', i18n('Critical Updates'), 'security-low']]

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
        if text == '' and self.searchUsed:
            self.searchActivated()

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

        # Show the info label if there are updates available
        # otherwise hide it.
        """
        if self.state.inUpgrade() and self.groupList.count() == 0:
            self.info.show()
        else:
            self.info.hide()
        """

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
        self.packageList.scrollToTop()
        self.selectAll.setChecked(self.groupList.currentGroup() in self._selectedGroups)
        restoreCursor()

    def searchActivated(self):
        self.packageList.resetMoreInfoRow()
        waitCursor()
        searchText  = str(self.searchLine.text()).split()
        if searchText:
            sourceModel = self.packageList.model().sourceModel()
            self.state.cached_packages = sourceModel.search(searchText)
            self.groupList.lastSelected = None
            self.searchUsed = True
        else:
            self.state.cached_packages = None
            self.state.packages()
            self.searchUsed = False
        self.initializeGroupList()
        restoreCursor()

    def setActionButton(self):
        self.actionButton.setEnabled(False)
        self.actionButton.setText(self.state.getActionName())
        self.actionButton.setIcon(self.state.getActionIcon())

    def actionStarted(self, operation):
        if self.state.silence:
            totalPackages = len(self.state._selected_packages)
            if not any(package.endswith('.pisi') for package in self.state._selected_packages):
                totalPackages += len(self.state.iface.getExtras(self.state._selected_packages))

        self.progressDialog.reset()
        if not operation in ["System.Manager.updateRepository", "System.Manager.updateAllRepositories"]:
            if not self.state.silence:
                totalPackages = self.packageList.packageCount()
            self.operation.setTotalPackages(totalPackages)
            self.progressDialog.updateStatus(0, totalPackages, self.state.toBe())
        if self.isVisible():
            if operation in ["System.Manager.updateRepository", "System.Manager.updateAllRepositories"]:
                self.progressDialog.repoOperationView()
            self.progressDialog.show()
        self.progressDialog.enableCancel()

    def exceptionCaught(self, message):
        self.progressDialog.hide()
        if any(warning in message for warning in ('urlopen error','Socket Error', 'PYCURL ERROR')):
            errorTitle = i18n("Network Error")
            errorMessage = i18n("Please check your network connections and try again.")
        elif "Access denied" in message or "tr.org.pardus.comar.Comar.PolicyKit" in message:
            errorTitle = i18n("Authorization Error")
            errorMessage = i18n("You are not authorized for this operation.")
        elif "HTTP Error 404" in message:
            errorTitle = i18n("Pisi Error")
            errorMessage = i18n("Package not found. It may be upgraded in or removed from the repository. Please try upgrading repository informations.")
        else:
            errorTitle = i18n("Pisi Error")
            errorMessage = message

        self.messageBox = QMessageBox(errorTitle, errorMessage, QMessageBox.Critical, QMessageBox.Ok, 0, 0)
        self.messageBox.show()

        if self.state.state == self.state.UPGRADE:
            {self.state.INSTALL:self.parent.showInstallAction,
             self.state.REMOVE :self.parent.showRemoveAction}[self.lastState].setChecked(True)
            self.switchState(self.lastState)

    def actionFinished(self, operation):
        if operation == "System.Manager.installPackage":
            self.showSummary()
        if operation in ("System.Manager.installPackage", "System.Manager.removePackage", "System.Manager.updatePackage"):
            self.notifyFinished()
        if not self.state.silence:
            self.searchLine.clear()
            self.state.reset()
            self.progressDialog.hide()
            if operation in ("System.Manager.updateRepository", "System.Manager.updateAllRepositories"):
                self.emit(SIGNAL("repositoriesUpdated()"))
            self.initialize()
        else:
            qApp.exit()

    def actionCancelled(self):
        self.progressDialog.hide()
        if self.state.silence:
            qApp.exit()
        else:
            self.groupFilter()

    def notifyFinished(self):
        if not self.operation.totalPackages:
            return
        if self.state.silence:
            Pds.notify(i18n('Package Manager'), self.state.getSummaryInfo(self.operation.totalPackages))
        elif Pds.session == pds.Kde4:
            from PyKDE4.kdeui import KNotification
            from PyKDE4.kdecore import KComponentData
            KNotification.event("Summary",
                    self.state.getSummaryInfo(self.operation.totalPackages),
                    QPixmap(),
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
        self.lastState = self.state.state
        self.state.setState(state)
        self._selectedGroups = []
        self.setActionButton()
        if action:
            self.state.stateAction()

        self.initialize()

    def emitStatusBarInfo(self, packages, packagesSize, extraPackages, extraPackagesSize):
        self.emit(SIGNAL("selectionStatusChanged(QString)"), self.state.statusText(packages, packagesSize, extraPackages, extraPackagesSize))

    def setSelectAll(self, packages=None):
        if packages:
            self.packageList.reverseSelection(packages)

    def setReverseAll(self, packages=None):
        if packages:
            self.packageList.selectAll(packages)

    def toggleSelectAll(self, toggled):
        self._last_packages = self.packageList.model().getFilteredPackages()

        if toggled:
            if self.groupList.currentGroup() not in self._selectedGroups:
                self._selectedGroups.append(self.groupList.currentGroup())
            self.setReverseAll(self._last_packages)
        else:
            if self.groupList.currentGroup() in self._selectedGroups:
                self._selectedGroups.remove(self.groupList.currentGroup())
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

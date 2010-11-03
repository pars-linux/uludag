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

from PyQt4.QtGui import qApp
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QCompleter
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QToolButton
from PyQt4.QtGui import QFontMetrics

from PyQt4.QtCore import Qt
from PyQt4.QtCore import QSize
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QTimer
from PyQt4.QtCore import QMutex
from PyQt4.QtCore import QRegExp
from PyQt4.QtCore import QVariant

from PyKDE4.kdeui import KIcon
from PyKDE4.kdeui import KIconLoader
from PyKDE4.kdeui import KNotification

from PyKDE4.kdecore import i18n
from PyKDE4.kdecore import KComponentData

from ui_mainwidget_v3 import Ui_MainWidget

from config import PMConfig
from pmutils import waitCursor
from pmutils import restoreCursor

from pdswidgets import PMessageBox
from packageproxy import PackageProxy
from packagemodel import PackageModel
from packagemodel import GroupRole
from statemanager import StateManager
from basketdialog import BasketDialog
from statusupdater import StatusUpdater
from summarydialog import SummaryDialog
from progressdialog import ProgressDialog
from packagedelegate import PackageDelegate
from operationmanager import OperationManager

class MainWidget(QWidget, Ui_MainWidget):
    def __init__(self, parent = None, silence = False):
        QWidget.__init__(self, parent)

        self.setupUi(self)
        self.parent = parent

        self._selectedGroups = []

        self.state = StateManager(self)
        self.lastState = self.state.state
        self._back_to_all = False

        # state.silence is using for pm-install module
        self.state.silence = silence

        # in silence mode we dont need these
        self.statusUpdater = StatusUpdater()
        self.basket = BasketDialog(self.state, self.parent)
        self.searchButton.setIcon(KIcon("edit-find"))
        self.initializeUpdateTypeList()
        self.initialize()
        self.updateSettings()
        self.setActionButton()

        self.operation = OperationManager(self.state)
        self.progressDialog = ProgressDialog(self.state, self.parent)
        self.summaryDialog = SummaryDialog(silence = silence)

        self.connectOperationSignals()
        self.pdsMessageBox = PMessageBox(self.content)
        self.__ui_ready = True

    def connectMainSignals(self):
        self.connect(self.actionButton, SIGNAL("clicked()"), self.showBasket)
        self.connect(self.searchButton, SIGNAL("clicked()"), self.searchActivated)
        self.connect(self.searchLine, SIGNAL("textEdited(const QString&)"), self.searchLineChanged)
        self.connect(self.searchLine, SIGNAL("returnPressed()"), self.searchActivated)
        self.connect(self.searchLine, SIGNAL("clearButtonClicked()"), self.groupFilter)
        self.connect(self.typeCombo, SIGNAL("activated(int)"), self.typeFilter)
        self.connect(self.stateTab, SIGNAL("currentChanged(int)"), self.switchState)
        self.connect(self.groupList, SIGNAL("groupChanged()"), self.groupFilter)
        self.connect(self.groupList, SIGNAL("groupChanged()"), lambda:self.searchButton.setEnabled(False))
        self.connect(self.packageList.select_all, SIGNAL("clicked(bool)"), self.toggleSelectAll)
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
        self.initializePackageList()
        self.initializeGroupList()
        self.initializeStatusUpdater()
        self.statusChanged()
        self._selectedGroups = []
        self.packageList.select_all.setChecked(False)
        self.initializeBasket()
        restoreCursor()
        self.searchLine.setFocus(True)

    def initializeStatusUpdater(self):
        self.statusUpdater.calculate_deps = not self.state.state == self.state.ALL
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
        self.completer = QCompleter(self.state.packages(), self)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.searchLine.setCompleter(self.completer)
        self.connect(self.packageList.model(), SIGNAL("dataChanged(QModelIndex,QModelIndex)"), self.statusChanged)

    def updateSettings(self):
        self.packageList.showComponents = PMConfig().showComponents()
        self.packageList.setFocus()

    def searchLineChanged(self, text):
        self.searchButton.setEnabled(bool(text))
        if text == '':
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
        self.groupList.setIconSize(QSize(32, 32))
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
        waitCursor()
        self.packageList.resetMoreInfoRow()
        packages = self.state.groupPackages(self.groupList.currentGroup())
        self.packageList.model().setFilterRole(GroupRole)
        self.packageList.model().setFilterPackages(packages)
        self.packageList.scrollToTop()
        self.packageList.select_all.setChecked(self.groupList.currentGroup() in self._selectedGroups)
        restoreCursor()

    def searchActivated(self):
        searchText = str(self.searchLine.text()).split()
        if searchText:
            self.pdsMessageBox.showMessage(i18n("Searching..."), QPixmap(":/data/search.png"))
            sourceModel = self.packageList.model().sourceModel()
            self.state.cached_packages = sourceModel.search(searchText)
            self.groupList.lastSelected = None
            self.searchUsed = True
        else:
            self.state.cached_packages = None
            self.state.packages()
            self.searchUsed = False
        self.initializeGroupList()
        if self.state.cached_packages == []:
            self.pdsMessageBox.showMessage(i18n("No results found."), KIcon("dialog-information").pixmap(32,32))
        else:
            self.pdsMessageBox.hideMessage()

    def setActionButton(self):
        self.actionButton.setEnabled(False)
        if self.state.state == self.state.ALL:
            menu = QMenu(self.actionButton)
            self.__install_action = menu.addAction(self.state.getActionIcon(self.state.INSTALL),
                                                   self.state.getActionName(self.state.INSTALL),
                                                   self.showBasket)
            self.__remove_action = menu.addAction(self.state.getActionIcon(self.state.REMOVE),
                                                  self.state.getActionName(self.state.REMOVE),
                                                  self.showBasket)
            self.actionButton.setMenu(menu)
        else:
            self.actionButton.setMenu(None)
        self.actionButton.setIcon(self.state.getActionIcon())
        self.actionButton.setText(self.state.getActionName())

    def actionStarted(self, operation):
        if self.state.silence:
            totalPackages = len(self.state._selected_packages)
            if not any(package.endswith('.pisi') for package in self.state._selected_packages):
                totalPackages += len(self.state.iface.getExtras(self.state._selected_packages, self.state.state))

        self.progressDialog.reset()
        if not operation in ["System.Manager.updateRepository", "System.Manager.updateAllRepositories"]:
            if not self.state.silence:
                totalPackages = self.packageList.packageCount()
            self.operation.setTotalPackages(totalPackages)
            self.progressDialog.updateStatus(0, totalPackages, self.state.toBe())
        if self.isVisible():
            if operation in ["System.Manager.updateRepository", "System.Manager.updateAllRepositories"]:
                self.progressDialog.repoOperationView()
            self.progressDialog._show()
        self.progressDialog.enableCancel()

    def exceptionCaught(self, message):
        self.progressDialog._hide()
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
            self.switchState(self.lastState)

    def actionFinished(self, operation):
        has_summary = False
        if operation == "System.Manager.installPackage":
            has_summary = self.showSummary()

        if operation in ("System.Manager.installPackage",
                         "System.Manager.removePackage",
                         "System.Manager.updatePackage"):
            self.notifyFinished()

        if not has_summary and self.state.silence:
            qApp.exit()

        if not self.state.silence:
            if operation in ("System.Manager.updateRepository",
                             "System.Manager.updateAllRepositories"):
                self.emit(SIGNAL("repositoriesUpdated()"))

            self.searchLine.clear()
            self.state.reset()
            self.progressDialog._hide()

            if self._back_to_all:
                self.state.state = self.state.ALL

            self.initialize()

    def actionCancelled(self):
        self.progressDialog._hide()
        self.progressDialog.reset()
        if self.state.silence:
            qApp.exit()
        if self._back_to_all:
            self.state.state = self.state.ALL
        self.groupFilter()

    def notifyFinished(self):
        if not self.operation.totalPackages:
            return
        KNotification.event("Summary",
                self.state.getSummaryInfo(self.operation.totalPackages),
                QPixmap(),
                None,
                KNotification.CloseOnTimeout,
                KComponentData("package-manager", "package-manager", KComponentData.SkipMainComponentRegistration))

    def showSummary(self):
        self.summaryDialog.setDesktopFiles(self.operation.desktopFiles)
        if self.summaryDialog.hasApplication():
            self.summaryDialog.show()
            return True

    def setActionEnabled(self):
        enabled = self.packageList.isSelected()
        self.actionButton.setEnabled(enabled)
        self.basket.setActionEnabled(enabled)

    def switchState(self, state, action=True):
        self.searchLine.clear()
        self.pdsMessageBox.hideMessage()
        self._back_to_all = False
        self._states[state][1].setChecked(True)
        self.lastState = self.state.state
        self.state.setState(state)
        self._selectedGroups = []
        if not state == self.state.HISTORY:
            self.setActionButton()
            if action:
                self.state.stateAction()
            self.state.cached_packages = None
            self.initialize()
            # self.contentHistory.hide()
            # self.content.show()
        # else:
            # self.contentHistory.show()
            # self.content.hide()

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

    def showBasket(self, action = None):
        if self.basket.isVisible():
            return

        waitCursor()
        self.statusUpdater.wait()

        if not action:
            action = {self.__remove_action:self.state.REMOVE,
                      self.__install_action:self.state.INSTALL}.get(self.sender(), None)
            if action:
                self._back_to_all = True
                self.state.state = action
            else:
                self._back_to_all = False

        self.basket._show()
        restoreCursor()

    def initializeUpdateTypeList(self):
        self.typeCombo.clear()
        UPDATE_TYPES = [['normal', i18n('All Updates'), 'system-software-update'],
                        ['security', i18n('Security Updates'), 'security-medium'],
                        ['critical', i18n('Critical Updates'), 'security-low']]

        for type in UPDATE_TYPES:
            self.typeCombo.addItem(KIcon(type[2]), type[1], QVariant(type[0]))


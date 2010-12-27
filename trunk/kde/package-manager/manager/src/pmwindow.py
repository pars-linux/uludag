#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import sys

from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import *

from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

from statemanager import StateManager
from operationmanager import OperationManager

from pmutils import PM
from pmutils import askForActions

from ui_pminstall import Ui_PmWindow
from summarydialog import SummaryDialog
from progressdialog import ProgressDialog

from packageproxy import PackageProxy
from packagemodel import PackageModel
from packagedelegate import PackageDelegate

from PyKDE4.kdeui import KNotification
from PyKDE4.kdecore import KComponentData

class PmWindow(QDialog, PM, Ui_PmWindow):

    def __init__(self, app = None, packages = [], hide_summary = False):
        QDialog.__init__(self, None)
        self.setupUi(self)

        self.hide_summary = hide_summary
        self.state = StateManager(self)
        self.iface = self.state.iface
        self.state._selected_packages = packages

        if not any(package.endswith('.pisi') for package in self.state._selected_packages):
            available_packages = self.state.packages()
            for package in self.state._selected_packages:
                if package not in available_packages:
                    self.exceptionCaught('HTTP Error 404', package)
                    sys.exit(1)

        self.model = PackageModel(self)
        self.model.setCheckable(False)

        proxy = PackageProxy(self)
        proxy.setSourceModel(self.model)

        self.packageList.setModel(proxy)
        self.packageList.setPackages(packages)
        self.packageList.selectAll(packages)
        self.packageList.setItemDelegate(PackageDelegate(self, self, False))
        self.packageList.setColumnWidth(0, 32)
        self.packageList.hideSelectAll()

        self.operation = OperationManager(self.state)
        self.progressDialog = ProgressDialog(self.state, self)
        self.summaryDialog = SummaryDialog()

        self.connectOperationSignals()
        self.state.state = StateManager.INSTALL

        self.button_install.clicked.connect(self.installPackages)
        self.button_install.setIcon(KIcon("list-add"))

        self.button_cancel.clicked.connect(self.actionCancelled)
        self.button_cancel.setIcon(KIcon("dialog-cancel"))

        self.rejected.connect(self.actionCancelled)

    def reject(self):
        if self.iface.operationInProgress():
            return
        QDialog.reject(self)

    def installPackages(self):

        reinstall = False
        answer = True
        actions = self.state.checkInstallActions(self.model.selectedPackages())
        if actions:
            answer = askForActions(actions,
                   i18n("Selected packages are already installed.<br>"
                        "If you continue, the packages will be reinstalled"),
                   i18n("Already Installed Packages"),
                   i18n("Installed Packages"))

        if not answer:
            return

        if actions:
            reinstall = True

        operation = self.state.operationAction(self.model.selectedPackages(),
                                               reinstall = reinstall,
                                               silence = True)

        if operation == False:
            sys.exit(1)

    def actionStarted(self, operation):
        totalPackages = len(self.state._selected_packages)
        if not any(package.endswith('.pisi') for package in self.state._selected_packages):
            totalPackages += len(self.state.iface.getExtras(self.state._selected_packages, self.state.state))

        self.progressDialog.reset()
        if not operation in ["System.Manager.updateRepository", "System.Manager.updateAllRepositories"]:
            self.operation.setTotalPackages(totalPackages)
            self.progressDialog.updateStatus(0, totalPackages, self.state.toBe())

        self.progressDialog._show()
        self.progressDialog.enableCancel()

    def actionFinished(self, operation):
        if operation in ("System.Manager.installPackage",
                         "System.Manager.removePackage",
                         "System.Manager.updatePackage"):
            self.notifyFinished()

        if operation == "System.Manager.installPackage" and not self.hide_summary:
            self.summaryDialog.setDesktopFiles(self.operation.desktopFiles)
            self.summaryDialog.showSummary()
            self.hide()

        if not self.summaryDialog.hasApplication():
            # Package install succesfull return value is 0
            QTimer.singleShot(10, lambda: sys.exit(0))

    def actionCancelled(self):
        # Package install failed with user cancel, return value is 3
        sys.exit(3)

    def exceptionCaught(self, message, package = ''):
        PM.exceptionCaught(self, message, package)
        # Package install failed with some kind of error, return value is 1
        sys.exit(1)


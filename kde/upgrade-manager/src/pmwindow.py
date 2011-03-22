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

import os
import sys
import pisi

from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtCore import *

from statemanager import StateManager
from operationmanager import OperationManager

from pds.qpagewidget import QPageWidget
from pmutils import *

from ui_pminstall import Ui_UmWindow
from progressdialog import ProgressDialog

from packagemodel import PackageModel

class UmWindow(QDialog, PM, Ui_UmWindow):

    def __init__(self, app = None):
        QDialog.__init__(self, None)
        self.setupUi(self)

        self.state = StateManager(self)
        self.iface = self.state.iface
        self._started = False

        self._postexceptions = [lambda: sys.exit(1)]

        # Check if another pisi instance already running
        if isPisiRunning():
            self.exceptionCaught("ALREADY RUNNING", block = True)

        self.state.state = StateManager.INSTALL

        self.model = PackageModel(self)
        self.operation = OperationManager(self.state)
        self.progressDialog = ProgressDialog(self.state, self)

        self.connectOperationSignals()

        self._layout = QHBoxLayout(self.widget)
        self.pages = QPageWidget(self.widget)
        self.pages.setDuration(1000)
        self._layout.addWidget(self.pages)

        self.pages.createPage(QLabel("Welcome to upgrade manager bla bla bla... ", self.widget))
        self.pages.createPage(QLabel("Second Page we can define anything in here... ", self.widget))

        button = QPushButton("Install Curl package for test", self.widget)
        button.clicked.connect(self.install_test)
        self.pages.createPage(button,
                              inMethod  = lambda: self.nextButton.setEnabled(False),
                              outMethod = lambda: self.nextButton.setEnabled(True))

        self.pages.createPage(QLabel("Package Install Finished ! time to reboot...", self.widget),
                              inMethod  = lambda: self.nextButton.setText("Reboot"),
                              outMethod = lambda: self.nextButton.setText("Next"))

        self.nextButton.clicked.connect(self.pages.next)
        self.prevButton.clicked.connect(self.pages.prev)

        self.rejected.connect(self.actionCancelled)

    def install_test(self):

        packages = ['curl']
        self.state._selected_packages = packages
        self.model.setPackages(packages)
        self.model.selectPackages(packages)

        self.installPackages()

    def reject(self):
        if self.iface.operationInProgress() and self._started:
            return
        QDialog.reject(self)

    def installPackages(self):
        reinstall = True
        connection_required = True
        operation = self.state.operationAction(self.model.selectedPackages(),
                                               reinstall = reinstall,
                                               silence = True,
                                               connection_required = connection_required)
        self._started = True
        if operation == False:
            sys.exit(1)

    def actionStarted(self, operation):
        totalPackages = len(self.state._selected_packages)

        self.progressDialog.reset()
        if not operation in ["System.Manager.updateRepository", "System.Manager.updateAllRepositories"]:
            self.operation.setTotalPackages(totalPackages)
            self.progressDialog.updateStatus(0, totalPackages, self.state.toBe())

        self.progressDialog._show()

        if not self._started:
            self.progressDialog.disableCancel()
        else:
            self.progressDialog.enableCancel()

    def actionFinished(self, operation):
        if operation in ("System.Manager.installPackage",
                         "System.Manager.removePackage",
                         "System.Manager.updatePackage"):
            self.notifyFinished()

        self.progressDialog._hide()
        self.pages.next()

    def actionCancelled(self):
        # Package install failed with user cancel, return value is 3
        sys.exit(3)


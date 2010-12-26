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
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import *

from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

from ui_pminstall import Ui_PmDialog
from statemanager import StateManager
from packageproxy import PackageProxy
from packagemodel import PackageModel
from packagedelegate import PackageDelegate

class PmDialog(QDialog, Ui_PmDialog):

    def __init__(self, app = None, packages = []):
        QDialog.__init__(self, None)
        self.setupUi(self)

        self.state = StateManager(self)
        self.iface = self.state.iface
        self.state._selected_packages = packages

        if not any(package.endswith('.pisi') for package in self.state._selected_packages):
            available_packages = self.state.packages()
            for package in self.state._selected_packages:
                if package not in available_packages:
                    errorMessage = i18n("Package <b>%s</b> not found in repositories.<br>"\
                                        "It may be upgraded or removed from the repository.<br>"\
                                        "Please try upgrading repository informations." % package)
                    self.showFailMessage(errorMessage)
                    sys.exit()

        model = PackageModel(self)

        proxy = PackageProxy(self)
        proxy.setSourceModel(model)

        self.packageList.setModel(proxy)
        self.packageList.setPackages(packages)
        self.packageList.selectAll(packages)
        self.packageList.setItemDelegate(PackageDelegate(self, self, False))
        self.packageList.setColumnWidth(0, 32)
        self.packageList.hideSelectAll()

        self.state.state = StateManager.INSTALL
        self.button_install.clicked.connect(self.installPackages)

        self.progress.hide()

    def showFailMessage(self, message):
        errorTitle = i18n("Pisi Error")
        self.messageBox = QMessageBox(errorTitle, message, QMessageBox.Critical, QMessageBox.Ok, 0, 0)
        self.messageBox.exec_()

    def installPackages(self):
        operation = self.state.operationAction(self.state._selected_packages, silence = True)
        print "op:::", operation
        if operation == False:
            sys.exit()



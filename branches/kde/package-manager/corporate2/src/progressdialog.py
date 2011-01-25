#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file

from PyQt4 import QtGui
from PyQt4.QtCore import QSize
from PyQt4.QtCore import SIGNAL

from context import *

from ui_progressdialog import Ui_ProgressDialog
from pds.qprogressindicator import QProgressIndicator
import backend

class ProgressDialog(QtGui.QDialog, Ui_ProgressDialog):
    def __init__(self, state, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.iface = backend.pm.Iface()
        self.state = state
        self.setupUi(self)
        self.setModal(True)

        self.busy = QProgressIndicator(self)
        self.busy.setFixedSize(QSize(22, 22))
        self.titleLayout.addWidget(self.busy)

        self.connect(self.cancelButton, SIGNAL("clicked()"), self.cancel)

    def closeEvent(self, event):
        if self.cancelButton.isEnabled():
            self.cancel()
        event.ignore()

    def show(self):
        self.busy.busy()
        QtGui.QDialog.show(self)

    def hide(self):
        self.busy.hide()
        QtGui.QDialog.hide(self)

    def updateProgress(self, progress):
        self.progressBar.setValue(progress)
        self.setWindowTitle(i18n("Operation - %1%", progress))

    def updateOperation(self, operation, arg):
        if operation in [i18n("configuring"),  i18n("extracting")]:
            self.disableCancel()

        if operation == "updatingrepo":
            operationInfo = i18n("Downloading package list of %1", arg)
        else:
            operationInfo = i18n('%1 %2', operation, arg)

        self.operationInfo.setText(operationInfo)

    def updateStatus(self, packageNo, totalPackages, operation):
        if packageNo > 0:
            self.statusInfo.setText(i18n("%1 / %2 package %3", packageNo, totalPackages, operation))
        else:
            self.statusInfo.setText('')

    def updateRemainingTime(self, time):
        self.timeRemaining.setText(time)

    def updateCompletedInfo(self, completed, total, rate):
        self.completedInfo.setText(i18n("<p align='center'>%1 / %2, %3</p>", completed, total, rate))

    def updateActionLabel(self, action):
        self.actionLabel.setText("<b>%s</b>" % self.state.getActionCurrent(action))

    def enableCancel(self):
        self.cancelButton.setEnabled(True)

    def disableCancel(self):
        self.cancelButton.setEnabled(False)

    def reset(self):
        self.actionLabel.setText(i18n("<h3>Preparing PiSi...</h3>"))
        self.progressBar.setValue(0)
        self.operationInfo.setText("")
        self.completedInfo.setText("")
        self.statusInfo.setText(i18n("--  / --"))
        self.timeLabel.setText(i18n("Time remaining:"))
        self.timeRemaining.setText(i18n("--:--:--"))
        self.timeRemaining.show()

    def cancel(self):
        self.actionLabel.setText(i18n("<b>Cancelling operation...</b>"))
        self.disableCancel()
        self.iface.cancel()

    def repoOperationView(self):
        for widget in [self.statusInfo, self.timeLabel, self.timeRemaining]:
            widget.setText("")
        self.timeRemaining.hide()

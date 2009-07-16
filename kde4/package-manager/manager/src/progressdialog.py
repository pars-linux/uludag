#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file

from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL

from PyKDE4.kdecore import i18n

from ui_progressdialog import Ui_ProgressDialog
import backend

class ProgressDialog(QtGui.QDialog, Ui_ProgressDialog):
    def __init__(self, state, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.iface = backend.pm.Iface()
        self.state = state
        self.setupUi(self)
        self.setModal(True)
        self.startAnimation()
        self.connect(self.cancelButton, SIGNAL("clicked()"), self.cancel)

    def startAnimation(self):
        self.movie = QtGui.QMovie(self)
        self.animeLabel.setMovie(self.movie)
        self.movie.setFileName(":/data/pisianime.gif")
        self.movie.start()

    def updateProgress(self, progress):
        self.progressBar.setValue(progress)

    def updateOperation(self, operation, arg):
        if operation in [i18n("configuring"),  i18n("extracting")]:
            self.disableCancel()

        if operation == "updatingrepo":
            operationInfo = i18n("Downloading package list of %1", arg)
        else:
            operationInfo = i18n('%1 %2', operation, arg)

        self.operationInfo.setText(operationInfo)

    def updateStatus(self, packageNo, totalPackages, operation):
        self.statusInfo.setText(i18n("%1 / %2 package %3", packageNo, totalPackages, operation))

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
        self.statusLabel.setText(i18n("Status:"))
        self.statusInfo.setText(i18n("--  / --"))
        self.timeLabel.setText(i18n("Time remaining:"))
        self.timeRemaining.setText(i18n("--:--:--"))

    def cancel(self):
        self.actionLabel.setText(i18n("<b>Cancelling operation...</b>"))
        self.disableCancel()
        self.iface.cancel()

    def repoOperationView(self):
        for widget in [self.statusLabel, self.statusInfo, self.timeLabel, self.timeRemaining]:
            widget.setText("")

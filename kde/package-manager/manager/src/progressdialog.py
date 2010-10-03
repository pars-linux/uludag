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
from PyQt4.QtCore import SIGNAL

from PyKDE4.kdecore import i18n

from pds.gui import *
from ui_progressdialog_v4 import Ui_ProgressDialog
import backend

class ProgressDialog(PAbstractBox, Ui_ProgressDialog):

    def __init__(self, state, parent=None):
        PAbstractBox.__init__(self, parent)
        self.iface = backend.pm.Iface()
        self.state = state
        self.setupUi(self)
        self._animation = 2
        self._duration = 500
        self.last_msg = None
        self.enableOverlay()

        self.connect(self.cancelButton, SIGNAL("clicked()"), self.cancel)

    def _show(self):
        self.animate(start = MIDCENTER, stop = MIDCENTER, dont_animate = True)

    def _hide(self):
        self.animate(direction = OUT, dont_animate = True)

    def updateProgress(self, progress):
        self.progressBar.setValue(progress)
        self.percentage.setText(i18n("<p align='right'>%1 %</p>", progress))
        self.setWindowTitle(i18n("Operation - %1%", progress))

    def updateOperation(self, operation, arg):
        if operation in [i18n("configuring"),  i18n("extracting")]:
            self.disableCancel()

        if operation == "updatingrepo":
            operationInfo = i18n("Downloading package list of %1", arg)
        else:
            operationInfo = i18n('%1 %2', operation, arg)

        if not operationInfo == self.operationInfo.text():
            self.operationInfo.setText(operationInfo)

    def updateStatus(self, packageNo, totalPackages, operation):
        text = i18n("[%1 / %2]", packageNo, totalPackages)
        self.statusInfo.setText(text)

    def updateRemainingTime(self, time):
        self.timeRemaining.setText("<p align='right'>%s</p>" % time)

    def updateCompletedInfo(self, completed, total, rate):
        text = i18n("%1 / %2, %3", completed, total, rate)
        self.completedInfo.setText(text)

    def updateActionLabel(self, action):
        self.actionLabel.setText("<i>%s</i>" % self.state.getActionCurrent(action))

    def enableCancel(self):
        self.cancelButton.setEnabled(True)

    def disableCancel(self):
        self.cancelButton.setEnabled(False)

    def reset(self):
        self.actionLabel.setText(i18n("Preparing PiSi..."))
        self.progressBar.setValue(0)
        self.operationInfo.setText("")
        self.completedInfo.setText("")
        self.statusInfo.setText(i18n("-- / --"))
        self.timeRemaining.setText("<p align='right'>--:--:--</p>")
        self.timeRemaining.show()

    def cancel(self):
        self.actionLabel.setText(i18n("<b>Cancelling operation...</b>"))
        self.disableCancel()
        self.iface.cancel()

    def repoOperationView(self):
        for widget in [self.statusInfo, self.timeRemaining]:
            widget.setText("")
        self.timeRemaining.hide()

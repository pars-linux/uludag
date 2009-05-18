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

from PyKDE4.kdecore import i18n

from ui_progressdialog import Ui_ProgressDialog

class ProgressDialog(QtGui.QDialog, Ui_ProgressDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setModal(True)
        self.startAnimation()

    def startAnimation(self):
        self.movie = QtGui.QMovie(self)
        self.animeLabel.setMovie(self.movie)
        self.movie.setFileName("data/pisianime.gif")
        self.movie.start()

    def updateAction(self, action):
        self.actionInfo.setText(action)

    def updateProgress(self, progress):
        self.progressBar.setValue(progress)

    def updateOperation(self, operation, package):
        operationInfo = i18n('%1 %2', package, operation)
        self.operationInfo.setText(operationInfo)

    def updateStatus(self, status):
        self.statusInfo.setText(status)

    def updateRemainingTime(self, time):
        self.timeRemaining.setText(time)

    def updateCompletedInfo(self, completed):
        self.completedInfo.setText(completed)

    def enableCancel(self):
        self.cancelButton.setEnabled(True)

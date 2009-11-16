#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, 2006 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file

import time

from qt import *
from kdecore import *
from ProgressDialog import *

import Basket
import PisiIface
import Globals

class Progress(ProgressDialog):
    def __init__(self, parent=None):
        ProgressDialog.__init__(self)
        self.parent = parent
        animatedPisi = QMovie(locate("data","package-manager/pisianime.gif"))
        self.animeLabel.setMovie(animatedPisi)
        self.forcedClose = False
        self.connect(self.cancelButton,SIGNAL("clicked()"),self.cancelThread)
        self.cancelButton.setEnabled(False)
        self.hideOperationDescription()

        self.packageNo = 0
        self.totalPackages = 0
        self.rate = "-- KB/s"
        self.packageName = ""
        self.timeLeft = "--:--:--"

        self.totalSize = 0
        self.totalDownloaded = 0
        self.curPkgDownloaded = 0
        self.reset()

    def disableCancel(self):
        self.cancelButton.setEnabled(False)

    def enableCancel(self):
        self.cancelButton.setEnabled(True)

    def setCurrentOperation(self, text):
        self.currentOperationLabel.setText(text)

    def setOperationDescription(self, text):
        self.operationDescription.setText(text)

    def calculateTimeLeft(self, total, downloaded, rate, symbol):
        factor = {"B/s":1, "KB/s":1024, "MB/s":1048576, "GB/s":1073741824}
        if symbol == "--/-":
            return "--:--:--"
        rates = float(rate) * factor[symbol]
        left = total - downloaded
        self.timeLeft = '%02d:%02d:%02d' % tuple([i for i in time.gmtime(left/rates)[3:6]])

    def updateCompletedInfo(self):
        completed, total = self.getCurrentDownloadedSize()
        self.completedInfo.setText(i18n("<p align='center'>%1 / %2, %3</p>").arg(completed).arg(total).arg(self.rate))
        self.timeRemaining.setText(self.timeLeft)
        self.updateStatusInfo()

    def closeEvent(self, closeEvent):
        closeEvent.accept()
        if self.parent.command.inProgress():
            closeEvent.ignore()

    def showStatus(self):
        self.statusInfo.show()
        self.completedInfo.show()

    def showOperationDescription(self):
        self.operationDescription.show()

    def hideStatus(self, hidepackage=False):
        if hidepackage:
            self.statusLabel.hide()
            self.statusInfo.hide()
        else:
            self.statusLabel.show()
            self.statusInfo.show()

        self.completedInfo.hide()

    def hideOperationDescription(self):
        self.setOperationDescription("")

    def updateProgressBar(self, progress):
        self.progressBar.setProgress(float(progress))

    def reset(self):
        self.setCurrentOperation(i18n("<b>Preparing PiSi...</b>"))
        self.timeRemaining.setText("--:--")
        self.completedInfo.setText(i18n("<p align='center'>-- / --, -- KB/s</p>"))
        self.statusInfo.setText(i18n("-- / --"))
        self.timeLeft = "--:--:--"

        self.hideOperationDescription()
        self.hideStatus()

        # package statistics
        self.packageNo = 0
        self.totalPackages = 0

        # size informations
        self.totalDownloaded = 0
        self.curPkgDownloaded = 0
        self.totalSize = 0

        self.progressBar.setProgress(0)
        self.cancelButton.setEnabled(False)

    def cancelThread(self):
        self.setCurrentOperation(i18n("<b>Cancelling operation...</b>"))
        self.cancelButton.setEnabled(False)
        self.parent.command.cancel()

    def closeForced(self):
        self.forcedClose = True
        self.close()

    def close(self, alsoDelete=False):
        if self.forcedClose:
            ProgressDialog.close(self,alsoDelete)
            self.forcedClose = False
            return True

        self.forcedClose = False
        return False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            return
        else:
            ProgressDialog.keyPressEvent(self,event)

    def updateOperationDescription(self, operation, package=None):
        if not package:
            package = self.packageName

        self.setOperationDescription(i18n('%1 %2').arg(package).arg(operation))

    def updateDownloadingInfo(self, operation, file):
        self.packageName = PisiIface.parsePackageName(file)[0]
        self.setOperationDescription(i18n('%1 %2').arg(self.packageName).arg(operation))
        self.updateCompletedInfo()
        self.showOperationDescription()

    def updateUpgradingInfo(self):
        self.updateCompletedInfo()
        self.showOperationDescription()

    def updateStatusInfo(self):
        if self.parent.state == Basket.install_state:
            operation = i18n("installed")
        elif self.parent.state == Basket.remove_state:
            operation = i18n("removed")
        elif self.parent.state == Basket.upgrade_state:
            operation = i18n("upgraded")

        self.statusInfo.setText(i18n("%1 / %2 package %3").arg(self.packageNo).arg(self.totalPackages).arg(operation))

    # pisi does not provide total downloaded size, just package based.
    def updateTotalDownloaded(self, pkgDownSize, pkgTotalSize, rate, symbol):
        if rate == 0:
            self.rate = "-- KB/s"
        else:
            self.rate = "%s %s" % (rate, symbol)

        if pkgDownSize == pkgTotalSize:
            self.totalDownloaded += int(pkgTotalSize)
            self.curPkgDownloaded = 0
        else:
            self.curPkgDownloaded = int(pkgDownSize)

        self.calculateTimeLeft(self.totalSize, self.totalDownloaded + self.curPkgDownloaded, rate, symbol)

    # pisi does not provide total operation percent, just package based.
    def updateTotalOperationPercent(self):
        totalDownloaded = self.totalDownloaded + self.curPkgDownloaded
        try:
            percent = (totalDownloaded * 100) / self.totalSize
        except ZeroDivisionError:
            percent = 100

        self.updateProgressBar(percent)

    def getCurrentDownloadedSize(self):
        totaldownloaded = Globals.humanReadableSize(self.totalDownloaded + self.curPkgDownloaded, ".2")
        totalsize = Globals.humanReadableSize(self.totalSize, ".2")
        return (totaldownloaded, totalsize)

    def updatePackageProgress(self):
        try:
            percent = (self.packageNo * 100) / self.totalPackages
        except ZeroDivisionError:
            percent = 0

        self.updateProgressBar(percent)

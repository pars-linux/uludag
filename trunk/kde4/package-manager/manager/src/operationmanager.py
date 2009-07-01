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

import time

from PyQt4.QtCore import QObject, SIGNAL
from PyKDE4.kdecore import i18n

from pmutils import *
from pmlogging import logger

class OperationManager(QObject):
    def __init__(self, state):
        QObject.__init__(self)
        self.nop = ["System.Manager.clearCache", "System.Manager.setCache", "System.Manager.setConfig",
                    "System.Manager.setRepoActivities", "System.Manager.setRepositories"]
        self.state = state
        self.state.setExceptionHandler(self.exceptionHandler)
        self.state.setActionHandler(self.handler)
        self.initialize()

    def initialize(self):
        self.packageNo = 0
        self.totalPackages = 0
        self.totalSize = 0
        self.totalDownloaded = 0
        self.curPkgDownloaded = 0
        self.desktopFiles = []

    def setTotalPackages(self, totalPackages):
        self.totalPackages = totalPackages

    def calculateTimeLeft(self, rate, symbol):
        factor = {"B/s":1, "KB/s":1024, "MB/s":1048576, "GB/s":1073741824}
        if symbol == "--/-":
            return "--:--:--"
        rates = float(rate) * factor[symbol]
        total = self.totalSize
        downloaded = self.totalDownloaded + self.curPkgDownloaded
        left = total - downloaded

        timeLeft = '%02d:%02d:%02d' % tuple([i for i in time.gmtime(left/rates)[3:6]])
        self.emit(SIGNAL("elapsedTime(QString)"), timeLeft)

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

        completed = humanReadableSize(self.totalDownloaded + self.curPkgDownloaded, ".2")
        total = humanReadableSize(self.totalSize, ".2")

        self.emit(SIGNAL("downloadInfoChanged(QString, QString, QString)"), completed, total, self.rate)

    def updateTotalOperationPercent(self):
        totalDownloaded = self.totalDownloaded + self.curPkgDownloaded
        try:
            percent = (totalDownloaded * 100) / self.totalSize
        except ZeroDivisionError:
            percent = 100

        self.emit(SIGNAL("progress(int)"), percent)

    def updatePackageProgress(self):
        try:
            percent = (self.packageNo * 100) / self.totalPackages
        except ZeroDivisionError:
            percent = 0

        self.emit(SIGNAL("progress(int)"), percent)

    def addDesktopFile(self, desktopFile):
        if not self.state.inInstall():
            return
        if desktopFile.startswith("usr/share/applications/") or desktopFile.startswith("usr/kde/4/share/applications/kde4/"):
            self.desktopFiles.append(desktopFile)

    def exceptionHandler(self, exception):
        self.emit(SIGNAL("exception(QString)"), unicode(exception).lstrip("tr.org.pardus.comar.Exception: "))

    def handler(self, package, signal, args):

        if signal in ["started", "finished"]:
            logger.debug("Signal: %s" % str(signal))
            logger.debug("Args: %s" % str(args))

        # FIXME: manager.py should just send either a status or signal
        if signal in  ["status", "progress"]:
            signal = args[0]
            args = args[1:]
        ####

        if signal == "finished":
            self.state.chainAction(args[0])
            if args[0] in self.nop: # no operation
                return
            self.emit(SIGNAL("finished(QString)"), args[0])

        elif signal == "fetching":
            if not args[0].startswith("pisi-index.xml"):
                self.emit(SIGNAL("operationChanged(QString, QString)"), i18n("downloading"), args[0])
            self.updateTotalDownloaded(args[4], args[5], args[2], args[3])
            self.calculateTimeLeft(args[2], args[3])
            self.updateTotalOperationPercent()

        elif signal == "updatingrepo":
            self.emit(SIGNAL("operationChanged(QString, QString)"), signal, args[0])

        elif signal == "started":
            if args[0] in self.nop: # no operation
                return
            self.initialize()
            self.emit(SIGNAL("started(QString)"), args[0])

        elif signal in ["installing", "removing", "extracting", "configuring"]:
            self.emit(SIGNAL("operationChanged(QString, QString)"), i18n(signal), args[0])

        if signal == "cancelled":
            self.emit(SIGNAL("operationCancelled()"))

        elif signal == "desktopfile":
            self.addDesktopFile(str(args[0]))

        elif signal == "cached":
            self.totalSize = int(args[0]) - int(args[1])

        elif signal in ["removed", "installed", "upgraded"]:
            # Bug 4030
            if not self.state.inRemove() and signal == "removed":
                return
            self.packageNo += 1
            self.updatePackageProgress()
            self.emit(SIGNAL("packageChanged(int, int, QString)"), self.packageNo, self.totalPackages, i18n(signal))

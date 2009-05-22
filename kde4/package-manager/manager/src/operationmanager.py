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

from PyQt4.QtCore import QObject, SIGNAL
from PyKDE4.kdecore import i18n

from statemanager import StateManager

class OperationManager(QObject):
    def __init__(self, state):
        QObject.__init__(self)
        self.state = state
        self.state.setActionHandler(self.handler)
        self.initialize()

    def initialize(self):
        self.packageNo = 0
        self.totalPackages = 0
        self.totalSize = 0
        self.totalDownloaded = 0
        self.curPkgDownloaded = 0

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

    def updateTotalOperationPercent(self):
        totalDownloaded = self.totalDownloaded + self.curPkgDownloaded
        try:
            percent = (totalDownloaded * 100) / self.totalSize
        except ZeroDivisionError:
            percent = 100

        self.emit(SIGNAL("progress(int)"), percent)

    def handler(self, package, signal, args):
        print "Signal:", signal
        print "Args:", args

        # FIXME: manager.py should just send either a status or signal
        if signal in  ["status", "progress"]:
            signal = args[0]
            args = args[1:]
        ####

        if signal == "finished":
            self.emit(SIGNAL("finished(QString)"), args[0])

        elif signal == "fetching":
            self.emit(SIGNAL("operationChanged(QString, QString)"), i18n("downloading"), args[0])
            self.updateTotalDownloaded(args[4], args[5], args[2], args[3])
            self.calculateTimeLeft(args[2], args[3])
            self.updateTotalOperationPercent()

        elif signal == "started":
            self.initialize()
            self.emit(SIGNAL("started()"))

        elif signal in ["installing", "removing", "extracting", "configuring"]:
            self.emit(SIGNAL("operationChanged(QString, QString)"), i18n(signal), args[0])

        elif signal == "cached":
            self.totalSize = int(args[0]) - int(args[1])

        elif signal in ["removed", "installed", "upgraded"]:
            # Bug 4030
            if self.state.getState() != StateManager.REMOVE and signal == "removed":
                return
            self.packageNo += 1
            self.emit(SIGNAL("packageChanged(int, int, QString)"), self.packageNo, self.totalPackages, i18n(signal))

#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009-2010, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

from PyQt4.QtCore import QObject, SIGNAL
from PyKDE4.kdecore import i18n

from offlineparser import OfflineParser
from sessionmanager import SessionManager

import backend

class OfflineManager(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.setExceptionHandler(self.exceptionHandler)
        self.setActionHandler(self.handler)
        
        self.offlineparser = OfflineParser()

    def setActionHandler(self, handler):
        backend.pm.Iface().setHandler(handler)

    def setExceptionHandler(self, handler):
        backend.pm.Iface().setExceptionHandler(handler)

    def updateExportingProgress(self):
        try:
            percent = (self.packageNo * 100) / self.totalPackages
        except ZeroDivisionError:
            percent = 0

        self.emit(SIGNAL("exportingProgress(int)"), percent)

    def updateTotalOperationPercent(self):
        try:
            percent = (self.operationNo * 100) / self.totalOperations
        except ZeroDivisionError:
            percent = 0

        self.emit(SIGNAL("totalProgress(int)"), percent)

    def updateOperationPercent(self):
        try:
            percent = (self.packageNo * 100) / self.totalPackages
        except ZeroDivisionError:
            percent = 0

        self.emit(SIGNAL("currentProgress(int)"), percent)

    def importIndex(self, filename):        
        backend.pm.Iface().setIndex(filename)

    def exportIndex(self, filename):
        iface = backend.pm.Iface()

        source = iface.source  # store current source
        iface.setSource(None)  # set source None

        list_installed = iface.getPackageList()  # get installed package list
        packages = []

        self.totalPackages = len(list_installed)
        self.packageNo = 0

        for name in list_installed:
            packages.append(iface.getPackage(name))
            self.packageNo += 1
            self.updateExportingProgress()

        session = SessionManager()
        session.setSession(session.OFFLINE)

        try:
            backend.pm.Iface().writeIndex(packages, filename)
            print "Index file is written successfully."
        except:
            print "Index file could not written!"

        # set source and session to their previous states
        session.setSession(session.NORMAL)
        iface.setSource(source)

    def saveSession(self, filename):
        self.offlineparser.saveArchive(filename)

    def openSession(self, filename):
        self.offlineparser.extractArchive(filename)
        
        self.initOperations()
        self.getOperation()

    def initOperations(self):
        self.operations = self.offlineparser.parseOperations()
        self.totalOperations = len(self.operations)
        self.operationNo = 0
        self.signalCounter = 0

    def getOperation(self):
        self.updateTotalOperationPercent()
        self.operationNo += 1

        try:
            operation = self.operations[0][0]
            packages = self.operations[0][1]

            self.operations.pop(0)
            self.startOperation(operation, packages)
        except IndexError:
            self.emit(SIGNAL("finished()"))

    def startOperation(self, operation, packages):
        self.totalPackages = len(packages)
        self.packageNo = 0

        if operation == "install":
            backend.pm.Iface().installPackages(packages)

        elif operation == "remove":
            backend.pm.Iface().removePackages(packages)

        else:
            raise Exception("Unknown operation")

    def exceptionHandler(self, exception):
        self.emit(SIGNAL("exception(QString)"), str(exception))

    def handler(self, package, signal, args):
        if signal == "status":
            signal = str(args[0])
            args = args[1:]

            packageName = args[0]

            if signal == "installing":
                self.emit(SIGNAL("operationChanged(QString)"), i18n("Installing %s" % packageName))

            elif signal == "removing":
                self.emit(SIGNAL("operationChanged(QString)"), i18n("Removing %s" % packageName))

            elif signal in ["installed", "removed"]:
                self.packageNo += 1
                self.updateOperationPercent()

        elif signal == "finished":
            # it must wait for second finish signal to start next operation
            if self.signalCounter == 1:
                self.getOperation()
                self.signalCounter = 0
            else:
                self.signalCounter += 1

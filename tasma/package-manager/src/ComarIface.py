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

from qt import QMutex, SIGNAL
from kdeui import KMessageBox
from kdecore import i18n

# DBus
import dbus
import dbus.mainloop.qt3

from handler import CallHandler

class ComarIface:
    def __init__(self, handler=None, errHandler=None):
        self.errHandler = errHandler
        self.handler = handler
        # tray and package-manager synchronization
        self.com_lock = QMutex()
        # setup dbus stuff
        self.setupBusses()
        self.setupSignals()

    def setupBusses(self):
        try:
            self.sysBus = dbus.SystemBus()
            self.sesBus = dbus.SessionBus()
        except dbus.DBusException:
            KMessageBox.error(None, i18n("Unable to connect to DBus."), i18n("DBus Error"))
            return False
        return True

    def setupSignals(self):
        self.sysBus.add_signal_receiver(self.handleSignals, dbus_interface="tr.org.pardus.comar.System.Manager", member_keyword="signal", path_keyword="path")

    def handleSignals(self, *args, **kwargs):
        signal = kwargs["signal"]
        # use args here
        if self.handler:
            self.handler(signal, args)

    def busError(self, exception):
        KMessageBox.error(None, str(exception), i18n("D-Bus Error"))
        self.setupBusses()
        self.errHandler()

    def comarAuthError(self, exception):
        KMessageBox.error(None, str(exception), i18n("COMAR Auth Error"))
        self.errHandler()

    def comarError(self, exception):
        KMessageBox.error(None, str(exception), i18n("COMAR Error"))
        self.errHandler()

    def callMethod(self, method, action, handler, handleErrors, *args):
        print "Method: %s      Action: %s" % (method, action)
        ch = CallHandler("pisi", "System.Manager", method,
                         action,
                         self.sysBus, self.sesBus)

        if handleErrors:
            ch.registerError(self.comarError)
            ch.registerAuthError(self.comarAuthError)
            ch.registerDBusError(self.busError)

        if handler:
            ch.registerDone(handler)

        ch.call(*args)

    def installPackage(self, package):
        self.com_lock.lock()
        self.callMethod("installPackage", "tr.org.pardus.comar.system.manager.installpackage", None, True, package)

    def removePackage(self, package):
        self.com_lock.lock()
        self.callMethod("removePackage", "tr.org.pardus.comar.system.manager.removepackage", None, True, package)

    def updatePackage(self, package):
        self.com_lock.lock()
        self.callMethod("updatePackage", "tr.org.pardus.comar.system.manager.updatepackage", None, True, package)

    def updateRepo(self, repo):
        self.com_lock.lock()
        self.callMethod("updateRepository", "tr.org.pardus.comar.system.manager.updaterepository", None, True, repo)

    # handleErrors is for Tray's Interval Check. If there is no network, handleErrors param is used for not showing any error to the user.
    def updateAllRepos(self, handleErrors=True):
        self.com_lock.lock()
        self.callMethod("updateAllRepositories", "tr.org.pardus.comar.system.manager.updateallrepositories", None, handleErrors)

    def addRepo(self, name, uri):
        self.com_lock.lock()
        self.callMethod("addRepository", "tr.org.pardus.comar.system.manager.addrepository", None, True, name, uri)

    def removeRepo(self, repo):
        self.com_lock.lock()
        self.callMethod("removeRepo", "tr.org.pardus.comar.system.manager.removerepo", None, True, repo)

    def setRepositories(self, repos):
        self.com_lock.lock()
        self.callMethod("setRepositories", "tr.org.pardus.comar.system.manager.setrepositories", None, True, repos)

    def clearCache(self, cacheDir, limit):
        self.callMethod("clearCache", "tr.org.pardus.comar.system.manager.clearcache", None, True, cacheDir, limit)

    def setCache(self, enabled, limit):
        self.callMethod("setCache", "tr.org.pardus.comar.system.manager.setcache", None, True, enabled, limit)

    def cancel(self):
        obj = self.sysBus.get_object("tr.org.pardus.comar", "/")
        obj.cancel(dbus_interface="tr.org.pardus.comar")

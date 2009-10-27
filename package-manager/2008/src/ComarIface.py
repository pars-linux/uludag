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

from qt import QString, QMutex, SIGNAL
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
        if "urlopen error" in exception.message or "Socket Error" in exception.message:
            KMessageBox.error(None, i18n("Network error. Please check your network connections and try again."), i18n("COMAR Error"))
        elif "Access denied" in exception.message:
            message = i18n("You are not authorized for this operation.")
            KMessageBox.sorry(None, message, i18n("Error"))
        else:
            KMessageBox.error(None, QString.fromUtf8(str(exception)), i18n("COMAR Error"))

        self.errHandler()

    def cancelError(self):
        message = i18n("You are not authorized for this operation.")
        self.errHandler()
        KMessageBox.sorry(None, message, i18n("Error"))

    def callSyncMethod(self, method, *args):
        ch = CallHandler("pisi", "System.Manager", method,
                         None,
                         self.sysBus, self.sesBus)

    def callMethod(self, method, action, handler, handleErrors, async = True, *args):
        print "Method: %s      Action: %s" % (method, action)
        ch = CallHandler("pisi", "System.Manager", method,
                         action, async,
                         self.sysBus, self.sesBus)

        if handleErrors:
            ch.registerError(self.comarError)
            ch.registerAuthError(self.comarAuthError)
            ch.registerDBusError(self.busError)
            ch.registerCancel(self.cancelError)

        if handler:
            ch.registerDone(handler)

        ch.call(*args)

    def installPackage(self, package):
        self.com_lock.lock()
        self.callMethod("installPackage", "tr.org.pardus.comar.system.manager.installpackage", None, True, True, package)

    def removePackage(self, package):
        self.com_lock.lock()
        self.callMethod("removePackage", "tr.org.pardus.comar.system.manager.removepackage", None, True, True, package)

    def updatePackage(self, package):
        self.com_lock.lock()
        self.callMethod("updatePackage", "tr.org.pardus.comar.system.manager.updatepackage", None, True, True, package)

    def updateRepo(self, repo):
        self.com_lock.lock()
        self.callMethod("updateRepository", "tr.org.pardus.comar.system.manager.updaterepository", None, True, True, str(repo))

    # handleErrors is for Tray's Interval Check. If there is no network, handleErrors param is used for not showing any error to the user.
    def updateAllRepos(self, handleErrors=True):
        self.com_lock.lock()
        self.callMethod("updateAllRepositories", "tr.org.pardus.comar.system.manager.updateallrepositories", None, handleErrors, True)

    def addRepo(self, name, uri):
        self.com_lock.lock()
        self.callMethod("addRepository", "tr.org.pardus.comar.system.manager.addrepository", None, True, True, name, uri)

    def removeRepo(self, repo):
        self.com_lock.lock()
        self.callMethod("removeRepo", "tr.org.pardus.comar.system.manager.removerepo", None, True, True, repo)

    def setRepositories(self, repos):
        self.com_lock.lock()
        self.callMethod("setRepositories", "tr.org.pardus.comar.system.manager.setrepositories", None, True, True, repos)

    def clearCache(self, cacheDir, limit):
        self.callMethod("clearCache", "tr.org.pardus.comar.system.manager.clearcache", None, True, True, cacheDir, limit)

    def setCache(self, enabled, limit):
        self.callMethod("setCache", "tr.org.pardus.comar.system.manager.setcache", None, True, True, enabled, limit)

    def setConfig(self, category, name, value):
        self.callMethod("setConfig", "tr.org.pardus.comar.system.manager.setconfig", None, True, False, category, name, value)

    def cancel(self):
        obj = self.sysBus.get_object("tr.org.pardus.comar", "/", introspect=False)
        obj.cancel(dbus_interface="tr.org.pardus.comar")

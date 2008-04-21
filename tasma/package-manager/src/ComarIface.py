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

# DBus
import dbus
import dbus.mainloop.qt3

from handler import CallHandler

class ComarIface:
    def __init__(self,parent):
        self.parent = parent
        self.setupBusses()

        # tray and package-manager synchronization
        self.com_lock = QMutex()

        # Notification
        self.listenSignals()

    def setupBusses(self):
        try:
            self.busSys = dbus.SystemBus()
            self.busSes = dbus.SessionBus()
        except dbus.DBusException:
            KMessageBox.error(self, i18n("Unable to connect to DBus."), i18n("DBus Error"))
            return False
        return True

    def listenSignals(self):
        self.busSys.add_signal_receiver(self.handleSignals, dbus_interface="tr.org.pardus.comar.System.Manager", member_keyword="signal", path_keyword="path")

    def handleSignals(self, *args, **kwargs):
        path = kwargs["path"]
        signal = kwargs["signal"]
        if not path.startswith("/package/"):
            return
        script = path[9:]

    def busError(self, exception):
        KMessageBox.error(self, str(exception), i18n("D-Bus Error"))
        self.setupBusses()

    def comarError(self, exception):
        KMessageBox.error(self, str(exception), i18n("COMAR Error"))

    def callMethod(self, method, action, handler, *args):
        ch = CallHandler("pisi", "System.Manager", method,
                         action,
                         self.parent.winId(),
                         self.busSys, self.busSes)
        ch.registerError(self.comarError)
        ch.registerAuthError(self.comarError)
        ch.registerDBusError(self.busError)
        if handler:
            ch.registerDone(handler)
        ch.call(*args)

    def installPackage(self, package):
        self.com_lock.lock()
        self.callMethod("installPackage", "tr.org.pardus.comar.system.manager.installpackage", None, package)

    def removePackage(self, package):
        self.com_lock.lock()
        self.callMethod("removePackage", "tr.org.pardus.comar.system.manager.removepackage", None, package)

    def updatePackage(self, package):
        self.com_lock.lock()
        self.callMethod("updatePackage", "tr.org.pardus.comar.system.manager.updatepackage", None, package)

    def updateRepo(self, repo):
        self.com_lock.lock()
        self.callMethod("updateRepository", "tr.org.pardus.comar.system.manager.updaterepository", None, repo)

    def updateAllRepos(self):
        self.com_lock.lock()
        self.callMethod("updateAllRepositories", "tr.org.pardus.comar.system.manager.updateallrepositories", None)

    def addRepo(self, name, uri):
        self.com_lock.lock()
        self.callMethod("addRepository", "tr.org.pardus.comar.system.manager.addrepository", None, name, uri)

    def removeRepo(self, repo):
        self.com_lock.lock()
        self.callMethod("removeRepo", "tr.org.pardus.comar.system.manager.removerepo", None, repo)

    def setRepositories(self, repos):
        self.com_lock.lock()
        self.callMethod("setRepositories", "tr.org.pardus.comar.system.manager.setrepositories", None, repos)

    def clearCache(self, cacheDir, limit):
        self.callMethod("clearCache", "tr.org.pardus.comar.system.manager.clearcache", None, cacheDir, limit)

    def setCache(self, enabled=None, limit=None):
        self.callMethod("setCache", "tr.org.pardus.comar.system.manager.setcache", None, enabled, limit)

    def cancel(self):
        #FIXME
        pass

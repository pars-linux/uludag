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

from qt import QSocketNotifier, QMutex, SIGNAL
import comar

class ComarIface:
    def __init__(self,parent):
        self.parent = parent
        self.com = comar.Link()

        # tray and package-manager synchronization
        self.com_lock = QMutex()

        # Notification
        self.com.ask_notify("System.Manager.progress")
        self.com.ask_notify("System.Manager.error")
        self.com.ask_notify("System.Manager.warning")
        self.com.ask_notify("System.Manager.info")
        self.com.ask_notify("System.Manager.notify")
        self.com.ask_notify("System.Manager.finished")
        self.com.ask_notify("System.Manager.updatingRepo")

        self.notifier = QSocketNotifier(self.com.sock.fileno(), QSocketNotifier.Read)

        self.parent.connect(self.notifier, SIGNAL("activated(int)"), self.parent.slotComar)

    def installPackage(self, package):
        self.com_lock.lock()
        self.com.call("System.Manager.installPackage", ["package",package])

    def removePackage(self, package):
        self.com_lock.lock()
        self.com.call("System.Manager.removePackage", ["package",package])

    def updatePackage(self, package):
        self.com_lock.lock()
        self.com.call("System.Manager.updatePackage", ["package",package])

    def updateRepo(self, repo):
        self.com_lock.lock()
        self.com.call("System.Manager.updateRepository", ["repository",repo])

    def updateAllRepos(self, id=0):
        self.com_lock.lock()
        self.com.call("System.Manager.updateAllRepositories", id=id)

    def addRepo(self, name, uri):
        self.com_lock.lock()
        self.com.call("System.Manager.addRepository", ["name",name,"uri",uri])

    def removeRepo(self, repo):
        self.com_lock.lock()
        self.com.call("System.Manager.removeRepo", ["repository",repo])

    def setRepositories(self, repos):
        self.com_lock.lock()
        self.com.call("System.Manager.setRepositories", ["repos",repos])

    def clearCache(self, cacheDir, limit):
        self.com.call("System.Manager.clearCache", ["cacheDir",cacheDir,"limit",limit])

    def setCache(self, enabled=None, limit=None):
        self.com.call("System.Manager.setCache", ["enabled",enabled,"limit",limit])

    def cancel(self):
        self.com.cancel()

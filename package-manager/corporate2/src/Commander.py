# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

import string
import PisiIface

from kdeui import KMessageBox
from kdecore import i18n
from qt import QObject, QTimer
import Settings

class Commander(QObject):
    def __init__(self, parent):
        QObject.__init__(self)
        self.parent = parent
        self.iface = PisiIface.Iface()
        self.iface.setHandler(self.handler)
        self.iface.setExceptionHandler(self.exceptionHandler)

    def errHandler(self):
        self.iface.com_lock.unlock()
        self.parent.finished("System.Manager.cancelled")
        self.parent.resetState()
        self.parent.refreshState()

    def exceptionHandler(self, exception):
        if "urlopen error" in exception.message or "Socket Error" in exception.message:
            KMessageBox.error(None, i18n("Network error. Please check your network connections and try again."), i18n("COMAR Error"))
        elif "Access denied" in exception.message:
            message = i18n("You are not authorized for this operation.")
            KMessageBox.sorry(None, message, i18n("Error"))
        else:
            KMessageBox.error(None, QString.fromUtf8(str(exception)), i18n("COMAR Error"))

        self.errHandler()


    def handler(self, package, signal, data):
        if len(data) > 1:
            args = data[1:]
        else:
            args = None

        if signal == "finished":
            command = data[0]
            self.iface.com_lock.unlock()
            self.parent.finished(command)
        elif signal == "progress":
            self.parent.displayProgress(data)
        elif signal == "error":
            self.iface.com_lock.unlock()
            print "Error: ", str(data)
#            self.parent.showErrorMessage(str(args))
            self.parent.resetState()
            self.parent.refreshState()
        elif signal == "started":
            operation = signal
            self.parent.pisiNotify(operation, args)
        elif signal == "status":
            operation = data[0]
            self.parent.pisiNotify(operation, args)
        elif signal == "warning":
            self.iface.com_lock.unlock()
#            self.parent.showWarningMessage(str(args))
            print "Warning: ", str(data)
            self.parent.resetState()
            self.parent.refreshState()
        elif signal == "PolicyKit" and "policy.no" in data:
            message = i18n("You are not authorized for this operation.")
            KMessageBox.sorry(None, message, i18n("Error"))
        else:
            print "Got notification : %s with data : %s" % (signal, data)

    def startUpdate(self, repo = None, handleErrors=True):
        if repo is None:
            self.updateAllRepos(handleErrors)
        else:
            self.updateRepo(repo)

    def install(self,apps):
        self.iface.installPackage(apps)

    def updatePackage(self,apps):
        self.iface.upgradePackages(apps)

    def remove(self,apps):
        self.iface.removePackages(apps)

    def updateRepo(self, repo):
        self.iface.updateRepository(repo)

    def updateAllRepos(self):
        self.iface.updateRepositories()

    def addRepo(self,repoName,repoAddress):
        raise Exception("Not implemented")
#        self.iface.addRepo(repoName,repoAddress)

    def removeRepo(self, repoName):
        raise Exception("Not implemented")
#       self.iface.removeRepo(repoName)

    def setRepositories(self, repos):
        self.iface.setRepositories(repos)

    def listUpgradable(self):
        return self.iface.getUpdates()

    def listPackages(self):
        return self.iface.getPackageList()

    def listNewPackages(self):
        return self.iface.getPackageList()

    def getRepoList(self):
        return map(lambda x:x[0], self.iface.getRepositories())

    def getRepoUri(self,repoName):
        return self.iface.getRepositoryUrl(repoName)

    def cancel(self):
        self.iface.cancel()

    def checkConflicts(self, packages):
        return self.iface.getConflicts(packages)

    def inProgress(self):
        return self.iface.com_lock.locked()

    def clearCache(self, limit):
        self.iface.clearCache(limit)

    def setCache(self, enabled, limit):
        self.iface.setCacheLimit(enabled, limit)

    def setConfig(self, category, name, value):
        self.iface.setConfig(category, name, value)



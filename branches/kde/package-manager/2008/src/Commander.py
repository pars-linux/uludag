# -*- coding: utf-8 -*-
#
# Copyright (C) 2005,2006 TUBITAK/UEKAE
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
import ComarIface
import Settings

class Commander(QObject):
    def __init__(self, parent):
        QObject.__init__(self)
        self.parent = parent
        try:
            self.comar = ComarIface.ComarIface(self.handler, self.errHandler)
        except:
            parent.showErrorMessage("Cannot connect to Comar daemon")

    def errHandler(self):
        self.comar.com_lock.unlock()
        self.parent.finished("System.Manager.cancelled")
        self.parent.resetState()
        self.parent.refreshState()

    def handler(self, signal, data):
        if len(data) > 1:
            args = data[1:]
        else:
            args = None

        if signal == "finished":
            command = data[0]
            self.comar.com_lock.unlock()
            self.parent.finished(command)
        elif signal == "progress":
            self.parent.displayProgress(data)
        elif signal == "error":
            self.comar.com_lock.unlock()
            print "Error: ", str(data)
#            self.parent.showErrorMessage(str(args))
            self.parent.resetState()
            self.parent.refreshState()
        elif signal == "status":
            operation = data[0]
            self.parent.pisiNotify(operation, args)
        elif signal == "warning":
            self.comar.com_lock.unlock()
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
        apps = string.join(apps,",")
        self.comar.installPackage(apps)

    def updatePackage(self,apps):
        apps = string.join(apps,",")
        self.comar.updatePackage(apps)

    def remove(self,apps):
        apps = string.join(apps,",")
        self.comar.removePackage(apps)

    def updateRepo(self, repo):
        self.comar.updateRepo(repo)

    def updateAllRepos(self, handleErrors=True):
        self.comar.updateAllRepos(handleErrors)

    def addRepo(self,repoName,repoAddress):
        self.comar.addRepo(repoName,repoAddress)

    def removeRepo(self, repoName):
        self.comar.removeRepo(repoName)

    def setRepositories(self, repos):
        self.comar.setRepositories(repos)

    def listUpgradable(self):
        return PisiIface.get_upgradable_packages()

    def listPackages(self):
        return PisiIface.get_installed_packages()

    def listNewPackages(self):
        return PisiIface.get_not_installed_packages()

    def getRepoList(self):
        return PisiIface.get_repositories()

    def getRepoUri(self,repoName):
        return PisiIface.get_repository_url(repoName)

    def cancel(self):
        self.comar.cancel()

    def checkConflicts(self, packages):
        return PisiIface.get_conflicts(packages)

    def inProgress(self):
        return self.comar.com_lock.locked()

    def clearCache(self, limit):
        # FIXME: We can not get cache package directory from pisi if 
        # it is _removed_ (PiSi tries to create new one), so hardcoded.
        return self.comar.clearCache("/var/cache/pisi/packages", limit)

    def setCache(self, enabled, limit):
        self.comar.setCache(enabled, limit)

    def setConfig(self, category, name, value):
        self.comar.setConfig(category, name, value)



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

from kdecore import i18n
from qt import QObject, QTimer
import ComarIface
import Settings

from Tray import ID_TRAY_INTERVAL_CHECK

class Commander(QObject):
    def __init__(self, parent):
        QObject.__init__(self)
        self.parent = parent
        try:
            self.comar = ComarIface.ComarIface(self.handler, self.errHandler)
        except:
            parent.showErrorMessage("Cannot connect to Comar daemon")

    def errHandler():
        self.comar.com_lock.unlock()
        self.parent.finished("System.Manager.cancelled")
        self.parent.resetState()
        self.parent.refreshState()

    def handler(self, signal, data):
        print "Signal: ", signal
        print "Data: ", data
        args = data[1:] if len(data) > 1 else None

        if signal == "finished":
            command = data[0]
            self.comar.com_lock.unlock()
            self.parent.finished(command)
        elif signal == "progress":
            self.parent.displayProgress(data)
        elif signal == "error":
            self.comar.com_lock.unlock()
            self.parent.showErrorMessage(args)
            self.parent.resetState()
            self.parent.refreshState()
        elif signal == "status":
            operation = data[0]
            self.parent.pisiNotify(operation, args)
        elif signal == "warning":
            self.comar.com_lock.unlock()
            self.parent.showWarningMessage(args)
            self.parent.resetState()
            self.parent.refreshState()
        else:
            print "Got notification : %s with data : %s" % (signal, data)

#         # This is paranoia. We dont know what happened but we cancel what ever is being done, gracefully. If
#         # some misbehaviour is seen, comar.log is always there to look.
#         elif signal == "error":
#             self.comar.com_lock.unlock()
#             self.parent.finished("System.Manager.cancelled")
#             return
#         elif signal == "denied":
#             self.comar.com_lock.unlock()
#             self.parent.finished("System.Manager.cancelled")
#             self.parent.showErrorMessage(i18n("You do not have permission to do this operation."))
#         elif signal == "fail":
#             if data == "System.Manager.cancelled":
#                 self.comar.com_lock.unlock()
#                 self.parent.finished(data)
#                 return

#             self.comar.com_lock.unlock()
#             self.parent.finished()
#             self.parent.resetState()
#             self.parent.refreshState()

#             #FIXME: What replaces this in new Comar api
#             # do not show any error if it is the interval check
#             # if not reply.id == ID_TRAY_INTERVAL_CHECK:
#             #     self.parent.showErrorMessage(unicode(reply.data))

#             # if an error occured communicating with comar and components are not ready we should warn
#             if not PisiIface.get_components():
#                 self.parent.repoNotReady()
#         else:
#             # paranoia
#             self.comar.com_lock.unlock()
#             pass

    def startUpdate(self, repo = None):
        if repo is None:
            #FIXME: track id... anything needs to be added here?
            self.updateAllRepos()
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

    def updateAllRepos(self):
        self.comar.updateAllRepos()

    def addRepo(self,repoName,repoAddress):
        self.comar.addRepo(repoName,repoAddress)

    def removeRepo(self, repoName):
        self.comar.removeRepo(repoName)

    def setRepositories(self, list):
        self.comar.setRepositories(",".join(list))

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

    def checkCacheLimits(self):
        print "checkCacheLimits called"
        config = PisiIface.read_config("/etc/pisi/pisi.conf")

        cache = config.get("general", "package_cache")
        if cache == "True":
            limit = config.get("general", "package_cache_limit")

            # If PackageCache is used and limit is 0. It means limitless.
            if limit and int(limit) != 0:
                self.clearCache(int(limit) * 1024 * 1024)
        elif cache == "False":
            self.clearCache(0)

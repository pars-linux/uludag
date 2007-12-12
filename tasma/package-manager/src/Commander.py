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
import pisi

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
            self.comar = ComarIface.ComarIface(self)
        except:
            parent.showErrorMessage("Cannot connect to Comar daemon")

    def wait_comar(self):
        self.comar.notifier.setEnabled(False)
        import socket, time
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        timeout = 5
        while timeout > 0:
            self.parent.processEvents()
            try:
                if pisi.api.ctx.comar_sockname:
                    sock.connect(pisi.api.ctx.comar_sockname)
                    return True
                else:
                    self.comar.notifier.setEnabled(True)
                    sock.connect("/var/run/comar.socket")
                    return True
            except socket.error:
                timeout -= 0.2
            time.sleep(0.2)
        return False

    def slotComar(self, sock):
        try:
            reply = self.comar.com.read_cmd()
        except:
            if not self.wait_comar():
                self.comar.com_lock.unlock()
                self.parent.showErrorMessage(i18n("Can't connect to Comar daemon"))
                self.parent.resetState()
                self.parent.refreshState()
            else:
                self.comar = ComarIface.ComarIface(self)
            return

        if reply.command == "notify":
            print "Comar notify received"
            (notification, script, data) = (reply.notify, reply.script, reply.data)
            data = unicode(data)
            if notification == "System.Manager.error":
                self.comar.com_lock.unlock()
                self.parent.showErrorMessage(data)
                self.parent.resetState()
                self.parent.refreshState()
            elif notification == "System.Manager.notify":
                self.parent.pisiNotify(data)
            elif notification == "System.Manager.progress":
                self.parent.displayProgress(data)
            elif notification == "System.Manager.finished":
                self.comar.com_lock.unlock()
                self.parent.finished(data)
            elif notification == "System.Manager.updatingRepo":
                pass
            else:
                print "Got notification : %s , for script : %s , with data : %s" % (notification, script, data)
        # This is paranoia. We dont know what happened but we cancel what ever is being done, gracefully. If
        # some misbehaviour is seen, comar.log is always there to look.
        elif reply.command == "error":
            print "Comar error received"
            self.comar.com_lock.unlock()
            self.parent.finished("System.Manager.cancelled")
            return
        elif reply.command == "denied":
            print "Comar denied received"
            self.comar.com_lock.unlock()
            self.parent.finished("System.Manager.cancelled")
            self.parent.showErrorMessage(i18n("You do not have permission to do this operation."))
        elif reply.command == "fail":
            print "Comar fail received"
            if reply.data == "System.Manager.cancelled":
                self.comar.com_lock.unlock()
                self.parent.finished(reply.data)
                return

            self.comar.com_lock.unlock()
            self.parent.finished()
            self.parent.resetState()
            self.parent.refreshState()

            # do not show any error if it is the interval check
            if not reply.id == ID_TRAY_INTERVAL_CHECK:
                self.parent.showErrorMessage(unicode(reply.data))

            # if an error occured communicating with comar and components are not ready we should warn
            if not pisi.db.componentdb.ComponentDB().list_components():
                self.parent.repoNotReady()
        else:
            # paranoia
            self.comar.com_lock.unlock()
            pass

    def startUpdate(self, repo = None, id=0):
        if repo is None:
            self.updateAllRepos(id)
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

    def updateAllRepos(self, id=0):
        self.comar.updateAllRepos(id)

    def addRepo(self,repoName,repoAddress):
        self.comar.addRepo(repoName,repoAddress)

    def removeRepo(self, repoName):
        self.comar.removeRepo(repoName)

    def setRepositories(self, list):
        self.comar.setRepositories(",".join(list))

    def listUpgradable(self):
        return pisi.api.list_upgradable()

    def listPackages(self):
        return list(pisi.api.list_installed())

    def listNewPackages(self):
        return list((set(pisi.api.list_available()) - set(pisi.api.list_installed())) - set(pisi.api.list_replaces().values()))
    
    def packageGraph(self,list,ignoreInstalled=True):
        return pisi.api.package_graph(list, ignoreInstalled)

    def getRepoList(self):
        return pisi.db.repodb.RepoDB().list_repos()

    def getRepoUri(self,repoName):
        return pisi.db.repodb.RepoDB().get_repo(repoName).indexuri.get_uri()

    def cancel(self):
        self.comar.cancel()

    def checkConflicts(self, packages):
        return pisi.api.get_conflicts(packages)

    def inProgress(self):
        return self.comar.com_lock.locked()

    def clearCache(self, limit):
        # FIXME: We can not get cache package directory from pisi if 
        # it is _removed_ (PiSi tries to create new one), so hardcoded.
        return self.comar.clearCache("/var/cache/pisi/packages", limit)

    def setCache(self, enabled, limit):
        self.comar.setCache(enabled, limit)

    def checkCacheLimits(self):
        config = pisi.configfile.ConfigurationFile("/etc/pisi/pisi.conf")

        cache = config.get("general", "package_cache")
        if cache == "True":
            limit = config.get("general", "package_cache_limit")
            
            # If PackageCache is used and limit is 0. It means limitless.
            if limit and int(limit) != 0:
                self.clearCache(int(limit) * 1024 * 1024)
        elif cache == "False":
            self.clearCache(0)

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
import pisi.api

from kdecore import i18n
from qt import QObject, QTimer
import ComarIface

class Commander(QObject):
    def __init__(self, parent):
        QObject.__init__(self)

        try:
            self.comar = ComarIface.ComarIface(self)
        except:
            parent.showErrorMessage("Cannot connect to Comar daemon")

        self.parent = parent

        # Init the database
        pisi.api.init(database=True, write=False)

    def wait_comar(self):
        self.comar.notifier.setEnabled(False)
        import socket, time
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        timeout = 5
        while timeout > 0:
            self.parent.processEvents()
            try:
                if ctx.comar_sockname:
                    sock.connect(ctx.comar_sockname)
                else:
                    self.comar.notifier.setEnabled(True)
                    sock.connect("/var/run/comar.socket")
                    return True
            except:
                timeout -= 0.2
            time.sleep(0.2)
        return False

    def slotComar(self, sock):
        try:
            reply = self.comar.com.read_cmd()
        except:
            if not self.wait_comar():
                self.parent.showErrorMessage(i18n("Can't connect to Comar daemon"))
            else:
                self.comar = ComarIface.ComarIface(self)
            return

        if reply.command == "notify":
            (notification, script, data) = (reply.notify, reply.script, reply.data)
            data = unicode(data)
            if notification == "System.Manager.error":
                self.parent.showErrorMessage(data)
            elif notification == "System.Manager.notify":
                self.parent.pisiNotify(data)
            elif notification == "System.Manager.progress":
                self.parent.displayProgress(data)
            elif notification == "System.Manager.finished":
                self.parent.finished(data)
            elif notification == "System.Manager.updatingRepo":
                pass
            else:
                print "Got notification : %s , for script : %s , with data : %s" % (notification, script, data)
        # This is paranoia. We dont know what happened but we cancel what ever is being done, gracefully. If
        # some misbehaviour is seen, comar.log is always there to look.
        elif reply.command == "error":
            self.parent.finished("System.Manager.cancelled")
            return
        elif reply.command == "fail":
            if reply.data == "System.Manager.cancelled":
                self.parent.finished(reply.data)
                return

            self.parent.finished()
            self.parent.showErrorMessage(unicode(reply.data))

            # if an error occured communicating with comar and components are not ready we quit
            if not pisi.context.componentdb.list_components():
                self.parent.repoNotReady()
        else:
            pass
            #print 'Unhandled: ',reply

    def startUpdate(self):
        self.updateAllRepos()

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
        return pisi.api.list_upgradable()

    def listPackages(self):
        return list(pisi.api.list_installed())

    def listNewPackages(self):
        return list(pisi.api.list_available() - pisi.api.list_installed())

    def packageGraph(self,list,ignoreInstalled=True):
        return pisi.api.package_graph(list, ignoreInstalled)

    def getRepoList(self):
        return pisi.context.repodb.list()

    def getRepoUri(self,repoName):
        return pisi.api.ctx.repodb.get_repo(repoName).indexuri.get_uri()

    def cancel(self):
        self.comar.cancel()

    def checkConflicts(self, packages):
        return pisi.api.generate_conflicts(packages)

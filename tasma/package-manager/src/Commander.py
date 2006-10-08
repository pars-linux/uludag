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
#
# Authors: İsmail Dönmez <ismail@pardus.org.tr>

import string
import pisi
import pisi.api

from kdecore import i18n
from qt import QObject, QTimer
import ComarIface

(install, remove, upgrade, addrepo, removerepo, updaterepo, setrepo) = range(1, 8)

class Commander(QObject):
    def __init__(self, parent):
        QObject.__init__(self)

        try:
            self.comar = ComarIface.ComarIface(self)
        except:
            parent.showErrorMessage("Cannot connect to Comar daemon")

        self.parent = parent
        self.command = None

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

        if reply[0] == self.comar.com.NOTIFY:
            notification, script, data = reply[2].split("\n", 2)
            data = unicode(data)

            if notification == "System.Manager.error":
                self.parent.showErrorMessage(data)
            elif notification == "System.Manager.notify":
                self.parent.pisiNotify(data)
            elif notification == "System.Manager.progress":
                data = data.split(",")
                rate = round(int(data[2]),1)
                self.parent.updateProgressBar(data[0], int(data[1]), rate, data[3], int(data[4]), int(data[5]))
            elif notification == "System.Manager.finished":
                self.parent.finished(self.command)
            elif notification == "System.Manager.updatingRepo":
                self.parent.packagesOrder.append(data)
            else:
                print "Got notification : %s , for script : %s , with data : %s" % (notification, script, data)
        elif reply[0] == self.comar.com.FAIL:
            self.parent.finished()
            self.parent.showErrorMessage(unicode(reply[2]))

            if self.parent.initialRepoCheck:
                self.parent.initialRepoCheck = False
                self.parent.repoMetadataCheck()
        else:
            pass
            #print 'Unhandled: ',reply

    def startUpdate(self):
        self.command = updaterepo
        self.updateAllRepos()

    def install(self,apps):
        self.command = install
        apps = string.join(apps,",")
        self.comar.installPackage(apps)

    def updatePackage(self,apps):
        self.command = upgrade
        apps = string.join(apps,",")
        self.comar.updatePackage(apps)

    def remove(self,apps):
        self.command = remove
        apps = string.join(apps,",")
        self.comar.removePackage(apps)

    def updateRepo(self, repo):
        self.command = updaterepo
        self.comar.updateRepo(repo)

    def updateAllRepos(self):
        self.command = updaterepo
        self.comar.updateAllRepos()

    def addRepo(self,repoName,repoAddress):
        self.command = addrepo
        self.comar.addRepo(repoName,repoAddress)

    def removeRepo(self, repoName):
        self.command = removeRepo
        self.comar.removeRepo(repoName)

    def setRepositories(self, list):
        self.command = setrepos
        self.comar.setRepositories(",".join(list))

    def listUpgradable(self):
        return pisi.api.list_upgradable()

    def listPackages(self):
        return list(pisi.api.list_installed())

    def listNewPackages(self):
        return list(pisi.api.list_available() - pisi.api.list_installed())

    def searchPackage(self,query,language='tr'):
        return pisi.api.search_package(query,language)

    def packageGraph(self,list,ignoreInstalled=True):
        return pisi.api.package_graph(list, ignoreInstalled)

    def getRepoList(self):
        return pisi.context.repodb.list()

    def getRepoUri(self,repoName):
        return pisi.api.ctx.repodb.get_repo(repoName).indexuri.get_uri()

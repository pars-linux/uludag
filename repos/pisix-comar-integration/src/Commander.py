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
#
# Authors: İsmail Dönmez <ismail@pardus.org.tr>

import pisi
import pisi.api

from qt import QObject
import ComarIface

class Commander(QObject):
    def __init__(self, parent):
        QObject.__init__(self)
        self.comar = ComarIface.ComarIface(self)
        self.parent = parent

        # Caching mechanism
        self.databaseDirty = False
        self.allPackages = []
        self.newPackages = []
        self.upgrades = []

        # Init the database
        pisi.api.init(database=True, write=False)

    def slotComar(self, sock):
        reply = self.comar.com.read_cmd()
        if reply[0] == self.comar.com.NOTIFY:
            notification, script, data = reply[2].split("\n", 2)
            data = unicode(data)

            if notification in ("System.Manager.warning","System.Manager.info"):
                self.parent.showInfoMessage(data)
            elif notification == "System.Manager.error":
                self.parent.showErrorMessage(data)
            elif notification == "System.Manager.progress":
                pass
            elif notification == "System.Manager.notify":
                pass
            else:
                print "Got notification : %s , for script : %s , with data : %s" % (notification, script, data)
        else:
            print 'Unhandled: ',reply[2]
        
    def install(self,apps):
        self.databaseDirty = True
        self.comar.installPackage(apps)
        
    def upgrade(self,apps):
        self.databaseDirty = True
        self.comar.upgradePackage(apps)
            
    def remove(self,apps):
        self.databaseDirty = True
        self.comar.removePackage(apps)
        
    def updateRepo(self, repo):
        self.databaseDirty = True
        self.comar.updateRepo(repo)
            
    def updateAllRepos(self):
        self.databaseDirty = True
        self.comar.updateAllRepos()
        
    def addRepo(self,repoName,repoAddress):
        self.databaseDirty = True
        self.comar.addRepo(repoName,repoAddress)
        
    def removeRepo(self, repoName):
        self.databaseDirty = True
        self.comar.removeRepo(repoName)
       
    def swapRepos(self, repo1, repo2):
        self.comar.swapRepos(repo1, repo2)
    
    def listUpgradable(self):
        if not len(self.upgrades) or self.databaseDirty:
            self.upgrades = pisi.api.list_upgradable()

        self.databaseDirty = False
        return self.upgrades
        
    def listPackages(self):
        if not len(self.allPackages) or self.databaseDirty:
            self.allPackages = pisi.context.installdb.list_installed()

        self.databaseDirty = False
        return self.allPackages

    def listNewPackages(self):
        if not len(self.newPackages) or self.databaseDirty:
            self.newPackages = list(pisi.api.list_available()-set(self.listPackages()))

        self.databaseDirty = False
        return self.newPackages

    def searchPackage(self,query,language='tr'):
        return pisi.api.search_package(query,language)

    def packageGraph(self,list,ignoreInstalled=True):
        return pisi.api.package_graph(list, ignoreInstalled)

    def getRepoList(self):
        return pisi.context.repodb.list()
    
    def getRepoUri(self,repoName):
        return pisi.api.ctx.repodb.get_repo(repoName).indexuri.get_uri()

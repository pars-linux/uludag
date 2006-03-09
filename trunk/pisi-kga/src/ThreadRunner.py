# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
#
# Authors: İsmail Dönmez <ismail@uludag.org.tr>

from qt import *

import pisi
import pisi.api

from Enums import *
import PisiUi

class PisiThread(QThread):
    def __init__(self, parent):
        QThread.__init__(self)
        self.ui = PisiUi.PisiUi(parent)
        self.parent = parent
        self.installing = False
        self.upgrading = False
        self.removing = False
        self.updatingRepo = False
        self.updatingAllRepos = False

    def initDatabase(self):
        try:
            pisi.api.init(database=True, options=None, ui=self.ui, comar=True)
        except:
            event = QCustomEvent(CustomEvent.InitError)
            self.postEvent(self.parent,event)
    
    def install(self,apps):
        self.installing = True
        self.appList = apps
        self.start()

    def upgrade(self,apps):
        self.upgrading = True
        self.appList = apps
        self.start()
    
    def remove(self,apps):
        self.removing = True
        self.appList = apps
        self.start()

    def updateRepo(self, repo):
        self.updatingRepo = True
        self.repo = repo
        self.start()
    
    def updateAllRepos(self):
        self.updatingAllRepos = True
        self.repoList = pisi.context.repodb.list()
        self.start()

    def addRepo(self,repoName,repoAddress):
        pisi.api.add_repo(repoName,repoAddress)
        
    def removeRepo(self, repoName):
        pisi.api.remove_repo(repoName)
       
    def swapRepos(self, repo1, repo2):
        pisi.api.ctx.repodb.swap(repo1, repo2)
    
    def listUpgradable(self):
        return pisi.api.list_upgradable()

    def listPackages(self):
        return pisi.packagedb.inst_packagedb.list_packages()

    def listAvailable(self):
        return pisi.api.list_available()

    def searchPackage(self,query,language='tr'):
        return pisi.api.search_package(query,language)

    def packageGraph(self,list,ignoreInstalled=True):
        return pisi.api.package_graph(list, ignoreInstalled)

    def getRepoList(self):
        return pisi.context.repodb.list()
    
    def getRepoUri(self,repoName):
        return pisi.api.ctx.repodb.get_repo(repoName).indexuri.get_uri()
        
    def run(self):
        try:
            if self.installing:
                pisi.api.install(self.appList)
                self.installing = False
                
            elif self.upgrading:
                pisi.api.upgrade(self.appList)
                self.upgrading = False
                
            elif self.removing:
                pisi.api.remove(self.appList)
                self.removing = False
                
            elif self.updatingRepo:
                event = QCustomEvent(CustomEvent.RepositoryUpdate)
                event.setData(self.repo)
                self.postEvent(self.parent,event)
                pisi.api.update_repo(self.repo)
                self.updatingRepo = False

            elif self.updatingAllRepos:
                for repo in self.repoList:
                    event = QCustomEvent(CustomEvent.RepositoryUpdate)
                    event.setData(repo)
                    self.postEvent(self.parent,event)
                    pisi.api.update_repo(repo)
                self.updatingAllRepos = False

        except pisi.Error,e:
            pisi.api.finalize()
            self.initDatabase()
            event = QCustomEvent(CustomEvent.PisiError)
            event.setData(unicode(e))
            self.postEvent(self.parent,event)

        # Send a finish event
        event = QCustomEvent(CustomEvent.Finished)
        self.postEvent(self.parent,event)

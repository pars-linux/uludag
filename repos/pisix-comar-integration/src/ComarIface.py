# -*- coding: utf-8 -*-
# Comar Interface

import comar

class ComarIface:
    def __init__(self):
        self.com = comar.Link()

    def installPackage(self, package):
        self.com.call("System.Manager.installPackage", ["package",package])

    def removePackage(self, package):
        self.com.call("System.Manager.removePackage", ["package",package])

    def upgradePackage(self, package):
        self.com.call("System.Manager.upgradePackage", ["package",package])

    def updateRepo(self, repo):
        self.com.call("System.Manager.upgradeRepository", ["repository",repo])

    def updateAllRepos(self):
        self.com.call("System.Manager.updateAllRepositories")

    def addRepo(self, repo):
        self.com.call("System.Manager.addRepository", ["repository",repo])

    def removeRepo(self, repo):
        self.com.call("System.Manager.removeRepo", ["repository",repo])

    def swapRepos(self, repo1, repo2):
        self.com.call("System.Manager.swapRepositories", ["repository1",repo1, "repository2",repo2])

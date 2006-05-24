# -*- coding: utf-8 -*-
# Comar Interface

from qt import QSocketNotifier, SIGNAL
import comar

class ComarIface:
    def __init__(self,parent):
        self.parent = parent
        self.com = comar.Link()

        # Notification
        self.com.ask_notify("System.Manager.progress")
        self.notifier = QSocketNotifier(self.com.sock.fileno(), QSocketNotifier.Read)
        
        self.parent.connect(self.notifier, SIGNAL("activated(int)"), self.parent.slotComar)

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

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
        self.com.ask_notify("System.Manager.error")
        self.com.ask_notify("System.Manager.warning")
        self.com.ask_notify("System.Manager.info")
        self.com.ask_notify("System.Manager.notify")
        self.com.ask_notify("System.Manager.finished")
        self.com.ask_notify("System.Manager.updatingRepo")

        self.notifier = QSocketNotifier(self.com.sock.fileno(), QSocketNotifier.Read)

        self.parent.connect(self.notifier, SIGNAL("activated(int)"), self.parent.slotComar)

    def installPackage(self, package):
        self.com.call("System.Manager.installPackage", ["package",package])

    def removePackage(self, package):
        self.com.call("System.Manager.removePackage", ["package",package])

    def updatePackage(self, package):
        self.com.call("System.Manager.updatePackage", ["package",package])

    def updateRepo(self, repo):
        self.com.call("System.Manager.upgradeRepository", ["repository",repo])

    def updateAllRepos(self):
        self.com.call("System.Manager.updateAllRepositories")

    def addRepo(self, name, uri):
        self.com.call("System.Manager.addRepository", ["name",name,"uri",uri])

    def removeRepo(self, repo):
        self.com.call("System.Manager.removeRepo", ["repository",repo])

    def setRepositories(self, repos):
        self.com.call("System.Manager.setRepositories", ["repos",repos])

    def cancel(self):
        self.com.cancel()

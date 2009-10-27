#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from qt import *
from kdeui import *
from kdecore import *

import pisi.api
import comar
from BalloonMessage import *


class ComarIface:
    def __init__(self):
        self.com = comar.Link()

    def updateAllRepos(self):
        self.com.call("System.Manager.updateAllRepositories")

class TrayApp(KSystemTray):
    def __init__(self,parent=None):
        KSystemTray.__init__(self,parent)

        icon = KGlobal.iconLoader().loadIcon("packagemanager",KIcon.Small)
        self.setPixmap(icon)

        self.timer = QTimer(self)
        self.connect(self.timer, SIGNAL("timeout()"), self.initPiSi)
        self.timer.start(1000, True)

        self.interval = None


    def initPiSi(self):
        pisi.api.init(database=True, write=False, options=None, comar=False)

        # check for upgrades for the first time
        self.checkUpgradable()

        self.config = KSimpleConfig("packagemanager_trayrc")
        self.config.setGroup("General")

        # check interval, default is 60 min
        self.interval = self.config.readNumEntry("Interval", 60) * (60 * 1000)

        self.disconnect(self.timer, SIGNAL("timeout()"), self.initPiSi)
        self.connect(self.timer, SIGNAL("timeout()"), self.checkUpgradable)
        self.timer.start(self.interval, False)


    def checkUpgradable(self):

        try:
            if self.popup.isShown():
                return
        except:
            pass

        # FIXME: No notification... etc...
        ComarIface().updateAllRepos()

        self.upgradeList = pisi.api.list_upgradable()

        if len(self.upgradeList):
            self.show()
            QTimer.singleShot(1000,self.showPopup)

    def showPopup(self):
        self.show()
        self.popup = KopeteBalloon(self,i18n("There are %1 updates available!").arg(len(self.upgradeList)),
                                   KGlobal.iconLoader().loadIcon("packagemanager",KIcon.Small))
        pos = self.mapToGlobal(self.pos())

        self.popup.setAnchor(pos)
        self.popup.show()

def main():
    name = "Package Manager Tray"
    desc = "Update Manager"
    aboutData = KAboutData(name, name, "0.1", desc, KAboutData.License_GPL,
                            "(C) 2006 UEKAE/TÜBİTAK", None, None, "bilgi@pardus.org.tr")
    aboutData.addAuthor('İsmail Dönmez', 'Maintainer', 'ismail@pardus.org.tr')

    KCmdLineArgs.init(sys.argv,aboutData)

    if not KUniqueApplication.start():
        return

    kapp = KUniqueApplication(True,True,True)

    tray = TrayApp()

    kapp.setMainWidget(tray)
    kapp.exec_loop()

if __name__ == "__main__":
    main()

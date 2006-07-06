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



class PiSiXTrayApp(KSystemTray):
    def __init__(self,parent=None):
        KSystemTray.__init__(self,parent)

        icon = KGlobal.iconLoader().loadIcon("pisix",KIcon.Small)
        self.setPixmap(icon)

        self.config = KSimpleConfig("pisix-tray")

        self.menu = self.contextMenu()
        self.menu.insertItem(QIconSet(icon), "Run PiSi-X")
        # FIXME: use proper icons
        self.menu.insertItem(QIconSet(icon), "Check upgrades now!")
        self.menu.insertItem(QIconSet(icon), "Configure")
        self.connect(self.menu, SIGNAL("activated(int)"), self.menuActivated)


        self.timer = QTimer(self)
        self.connect(self.timer, SIGNAL("timeout()"), self.initPiSi)
        self.timer.start(1000, True)

        self.interval = None


    def initPiSi(self):
        pisi.api.init(database=True, write=False, options=None, comar=False)

        # check for upgrades for the first time
        self.checkUpgradable()

        self.config.setGroup("General")
        # check interval, default is 60 min
        self.interval = self.config.readNumEntry("Interval", 60) * (60 * 1000)

        self.disconnect(self.timer, SIGNAL("timeout()"), self.initPiSi)
        self.connect(self.timer, SIGNAL("timeout()"), self.checkUpgradable)
        self.timer.start(self.interval, False)


    def checkUpgradable(self):

        # FIXME: No notification... etc...
        ComarIface().updateAllRepos()
                             
        upgradeList = pisi.api.list_upgradable()

        if upgradeList:
            self.popup = KopeteBalloon(i18n("There are new updates available!"),
                                       KGlobal.iconLoader().loadIcon("pisix",KIcon.Small))
            pos = self.mapToGlobal(self.pos())
            self.popup.setAnchor(pos)
            self.popup.show()

    def menuActivated(self):
        pass


            
if __name__ == "__main__":

    name = "pisix-tray"
    desc = "pisix tray application"
    aboutData = KAboutData(name, name, "0.0.1", desc, KAboutData.License_GPL,
                            "(C) 2006 UEKAE/TÜBİTAK", None, None, "bilgi@pardus.org.tr")
    aboutData.addAuthor('İsmail Dönmez', 'Maintainer', 'ismail@pardus.org.tr')

    KCmdLineArgs.init(sys.argv,aboutData)
    kapp = KApplication()
    
    tray = PiSiXTrayApp()
    tray.show()
    
    kapp.setMainWidget(tray)
    kapp.exec_loop()

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

def setconfig(config,key,value):
    config.writeEntry(key,value)

class TrayApp(KSystemTray):
    def __init__(self,parent=None):
        KSystemTray.__init__(self,parent)
        self.parent= parent

        icon = KGlobal.iconLoader().loadIcon("pisi-kga",KIcon.Desktop,24)
        self.setPixmap(icon)

        self.timer = QTimer()
        self.timer.connect(self.timer, SIGNAL("timeout()"), self.initPiSi)
        self.timer.start(1000, True)

        self.interval = None

    def initPiSi(self):
        pisi.api.init(database=True, write=False, options=None, comar=False)
        self.show()

        # check for upgrades for the first time
        self.checkUpgradable()

        self.config = KSimpleConfig("package-managerrc")
        self.config.setGroup("Tray")

        # get timer value or use default
        self.interval = self.config.readNumEntry("Timer",10)*60000

        self.disconnect(self.timer, SIGNAL("timeout()"), self.initPiSi)
        self.connect(self.timer, SIGNAL("timeout()"), self.checkUpgradable)
        self.timer.start(self.interval, False)

    def checkUpgradable(self):
        try:
            if self.popup.isShown():
                return
        except:
            pass

        self.upgradeList = pisi.api.list_upgradable()

        if len(self.upgradeList):
            QTimer.singleShot(10,self.showPopup)
        else:
            ComarIface().updateAllRepos()
            # lock for package-manager comar listener
            # FIXME, if package-manager window is running then dont do anything..
            self.parent.mainwidget.lock=1

    def showPopup(self):
        self.show()
        timeout=self.config.readNumEntry("Timeout",10)
        self.popup = KopeteBalloon(self,i18n("There are <b>%1</b> updates available!").arg(len(self.upgradeList)),
                                   KGlobal.iconLoader().loadIcon("pisi-kga",KIcon.Desktop,48),timeout)
        pos = self.mapToGlobal(self.pos())

        self.popup.setAnchor(pos)
        self.popup.show()


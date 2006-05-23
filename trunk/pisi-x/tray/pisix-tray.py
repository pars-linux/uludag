#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from qt import *
from kdeui import *
from kdecore import *

import pisi.api
from BalloonMessage import *


class PiSiXTrayApp(KSystemTray):
    def __init__(self,parent=None):
        KSystemTray.__init__(self,parent)

        icon = KGlobal.iconLoader().loadIcon("pisix",KIcon.Small)
        self.setPixmap(icon)

        self.menu = self.contextMenu()
        self.menu.insertItem(QIconSet(icon), "Run PiSi-X")
        self.connect(menu, SIGNAL("activated(int)"), self.menuActivated)


        self.timer = QTimer(self)
        self.connect(self.timer, SIGNAL("timeout()"), self.initPiSi)
        self.timer.start(1000, True)


    def initPiSi(self):
        pisi.api.init(database=True, write=False, options=None, comar=False)
        print pisi.api.list_upgradable()


    def menuActivated(self):
        pass


    def mousePressEvent(self,event):
        if event.button() == Qt.LeftButton:
            self.popup = KopeteBalloon(i18n("There are new updates available!"),
                                       KGlobal.iconLoader().loadIcon("pisix",KIcon.Small))
            pos = self.mapToGlobal(self.pos())
            self.popup.setAnchor(pos)
            self.popup.show()
        else:   
            KSystemTray.mousePressEvent(self,event)
            
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

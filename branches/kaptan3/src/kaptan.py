#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Copyright (C) 2008, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

# QT & KDE Modules
from qt import *
from kdecore import *
from kdeui import *
import kdedesigner

import sys

from screens.kaptanMain import kaptanUi

# Screens
import screens.ScrWelcome as ScrWelcome
import screens.ScrWallpaper as ScrWallpaper
import screens.ScrPackage as ScrPackage
import screens.ScrMouse as ScrMouse
import screens.ScrNetwork as ScrNetwork
import screens.ScrPanel as ScrPanel
import screens.ScrSummary as ScrSummary
import screens.ScrGoodbye as ScrGoodbye
import screens.ScrMultiple as ScrMultiple

#set avaiable screens
avail_screens = [ScrWelcome,
                 ScrMouse,
                 ScrPanel,
                 ScrMultiple,
                 ScrWallpaper,
                 ScrNetwork,
                 ScrPackage,
                 ScrSummary,
                 ScrGoodbye]



# set left panel
stepContents = {ScrWelcome: "Welcome",
                ScrMouse : "Mouse",
                ScrPanel : "Panel",
                ScrMultiple : "Multiple",
                ScrWallpaper : "Wallpaper",
                ScrNetwork : "Network",
                ScrPackage : "Package",
                ScrSummary : "Summary",
                ScrGoodbye : "Goodbye"
                }

mod_app = "Kaptan"
mod_name = "Kaptan"
mod_version = "3.0"

class Kaptan(kaptanUi):

    def __init__(self, *args):
        apply(kaptanUi.__init__, (self,) + args)

        #set images
        self.pixSteps.setPaletteBackgroundPixmap(QPixmap(locate("data", "kaptan/pics/leftWithCorner.png")))
        self.pageStack.setPaletteBackgroundPixmap(QPixmap(locate("data", "kaptan/pics/middleWithCorner.png")))
        self.pageIcon.setPixmap(QPixmap(locate("data", "kaptan/pics/default_icon.png")))

        # set texts
        self.pageTitle.setText(i18n("Welcome"))
        self.pageDesc.setText(i18n("Welcome to Kaptan Wizard :)"))
        self.buttonCancel.setText(i18n("&Cancel"))
        self.buttonBack.setText(i18n("« &Back"))
        self.buttonNext.setText(i18n("&Next »"))

        # set signals
        self.connect(self.buttonNext, SIGNAL("clicked()"),self.slotNext)
        self.connect(self.buttonBack, SIGNAL("clicked()"),self.slotBack)
        self.connect(self.buttonCancel, SIGNAL("clicked()"),self.slotExit)
        self.initialize()

    def initialize(self):
        for screen in avail_screens:
            _w = screen.Widget()
            self.pageStack.addWidget(_w)
        self.pageStack.raiseWidget(1)

    def getCurrent(self):
        return self.pageStack.id(self.pageStack.visibleWidget())

    def stackMove(self,where):
        if where<=0:
            where = 1
        if where>=len(avail_screens):
            where = len(avail_screens)

        self.pageStack.raiseWidget(where)
        _w = self.pageStack.visibleWidget()
        self.pageTitle.setText(_w.title)
        self.pageDesc.setText(_w.desc)
        _w.shown()


    def slotNext(self):
        _w = self.pageStack.visibleWidget()
        _w.execute()
        self.stackMove(self.getCurrent() + 1)

    def slotBack(self):
        self.stackMove(self.getCurrent() - 1)

    def slotExit(self):
        sys.exit(1)

def AboutData():
    return KAboutData(
        mod_app,
        mod_name,
        mod_version,
        None,
        KAboutData.License_GPL,
        '(C) 2008 UEKAE/TÜBİTAK',
        None,
        None,
        'bugs@pardus.org.tr'
    )

if __name__ == "__main__":
    global kapp

    about = AboutData()
    KCmdLineArgs.init(sys.argv, about)
    KUniqueApplication.addCmdLineOptions()

    if not KUniqueApplication.start():
        print i18n('Kaptan is already running!')
        sys.exit(1)

    kapp = KUniqueApplication(True, True, True)
    kaptan = Kaptan()
    kaptan.setCaption(i18n('Kaptan Welcome Wizard'))
    kaptan.setIcon(QPixmap(locate("data", "kaptan/pics/default_icon.png")))
    kaptan.show()
    kapp.setMainWidget(kaptan)
    sys.exit(kapp.exec_loop())


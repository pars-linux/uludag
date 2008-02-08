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

avail_screens = [ScrWelcome,
                 ScrWallpaper]

mod_name = 'Hede Manager'
mod_app = 'hede-manager'
mod_version = '0.1'

class Kaptan(kaptanUi):

    def __init__(self, *args):
        apply(kaptanUi.__init__, (self,) + args)
        self.connect(self.buttonNext, SIGNAL("clicked()"),self.slotNext)
        self.connect(self.buttonBack, SIGNAL("clicked()"),self.slotBack)
        self.initialize()

    def initialize(self):
        for screen in avail_screens:
            _w = screen.Widget()
            self.pageStack.addWidget(_w)
        self.pageStack.raiseWidget(1)

    def getCurrent(self):
        return self.pageStack.id(self.pageStack.visibleWidget())

    def stackMove(self,where):
        if where<=0:where = 1
        if where>=len(avail_screens):where = len(avail_screens)
        self.pageStack.raiseWidget(where)
        _w = self.pageStack.visibleWidget()
        self.pageTitle.setText(_w.title)
        self.pageDesc.setText(_w.desc)
        _w.shown()


    def slotNext(self):
        self.stackMove(self.getCurrent() + 1)

    def slotBack(self):
        self.stackMove(self.getCurrent() - 1)

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
        print 'Kaptan is already running!'

    kapp = KUniqueApplication(True, True, True)
    kaptan = Kaptan()
    kaptan.show()
    kapp.setMainWidget(kaptan)
    sys.exit(kapp.exec_loop())


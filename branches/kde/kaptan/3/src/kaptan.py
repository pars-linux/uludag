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
import logging
import os
import ConfigParser
import screens

from screens.kaptanMain import kaptanUi

# Screens
import screens.ScrWelcome as ScrWelcome
import screens.ScrWallpaper as ScrWallpaper
import screens.ScrPackage as ScrPackage
import screens.ScrMouse as ScrMouse
#import screens.ScrNetwork as ScrNetwork
import screens.ScrPanel as ScrPanel
import screens.ScrKeyboard as ScrKeyboard
import screens.ScrGoodbye as ScrGoodbye
import screens.ScrMultiple as ScrMultiple

def getKernelOpt(cmdopt=None):
    if cmdopt:
        for cmd in "".join(loadFile("/proc/cmdline")).split():
            if cmd.startswith("%s=" % cmdopt):
                return cmd[len(cmdopt)+1:].split(",")
    else:
        return "".join(loadFile("/proc/cmdline")).split()

    return ""

def loadFile(_file):
    try:
        f = file(_file)
        d = [a.strip() for a in f]
        d = (x for x in d if x and x[0] != "#")
        f.close()
        return d
    except:
        return []

def isLiveCD():
    opts = getKernelOpt("mudur")

    if opts and "livecd" in opts:
        return True

    return False

if isLiveCD():
    #set avaiable screens
    avail_screens = [ScrWelcome,
                 ScrMouse,
                 ScrKeyboard,
                 ScrPanel,
                 ScrMultiple,
                 ScrWallpaper,
                 #ScrNetwork,
                 ScrGoodbye]
else:
    #set avaiable screens
    avail_screens = [ScrWelcome,
                     ScrMouse,
                     ScrPanel,
                     ScrMultiple,
                     ScrWallpaper,
                     #ScrNetwork,
                     ScrPackage,
                     ScrGoodbye]


screenId = {}

mod_app = "kaptan"
mod_name = "Kaptan"
mod_version = screens.version

class Kaptan(kaptanUi):

    def __init__(self, *args):
        apply(kaptanUi.__init__, (self,) + args)

        self.logPath = os.path.join(os.path.expanduser("~"), ".kde/share/apps/kaptan/")

        if not os.path.exists(self.logPath):
            os.mkdir(self.logPath)

        self.logDir = os.path.join(self.logPath)

        # start logging:
        logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s %(levelname)-8s %(message)s',
            datefmt='%H:%M:%S',
            filename= self.logDir + 'kaptan.log',
            filemode='w')
        logging.info("Kaptan Started")

        # set images
        self.setPaletteBackgroundPixmap(QPixmap(locate("data", "kaptan/pics/bg.png")))
        self.pixSteps.setPaletteBackgroundPixmap(QPixmap(locate("data", "kaptan/pics/leftWithCorner.png")))
        self.pageStack.setPaletteBackgroundPixmap(QPixmap(locate("data", "kaptan/pics/middleWithCorner.png")))
        self.pageDesc.setPaletteBackgroundPixmap(QPixmap(locate("data", "kaptan/pics/text_bg.png")))

        # set button icons
        loader = KGlobal.iconLoader()
        self.buttonNext.setIconSet(QIconSet(loader.loadIcon("forward", KIcon.Small)))
        self.buttonBack.setIconSet(QIconSet(loader.loadIcon("back", KIcon.Small)))
        self.buttonCancel.setIconSet(QIconSet(loader.loadIcon("cancel", KIcon.Small)))
        self.buttonFinish.setIconSet(QIconSet(loader.loadIcon("ok", KIcon.Small)))

        # set texts
        self.pageDesc.setText(i18n("Welcome to Kaptan"))
        self.buttonCancel.setText(i18n("&Cancel"))
        self.buttonBack.setText(i18n("&Back"))
        self.buttonNext.setText(i18n("&Next"))
        self.buttonFinish.setText(i18n("Finish"))

        # hide back and finish buttons
        self.buttonFinish.hide()
        self.buttonBack.hide()

        # set signals
        self.connect(self.buttonNext, SIGNAL("clicked()"),self.slotNext)
        self.connect(self.buttonBack, SIGNAL("clicked()"),self.slotBack)
        self.connect(self.buttonCancel, SIGNAL("clicked()"), qApp, SLOT("quit()"))
        self.connect(self.buttonFinish, SIGNAL("clicked()"), qApp, SLOT("quit()"))

        self.initialize()

    def initialize(self):
        leftPanel = ""
        for screen in avail_screens:
            _w = screen.Widget()
            self.pageStack.addWidget(_w)
            sId = self.pageStack.id(_w)
            sCaption = _w.caption()
            screenId[sId] = sCaption

            if sId == 1:
                leftPanel += self.putBold(sCaption)
            else:
                leftPanel += self.putBr(sCaption)

        self.pixSteps.setText(leftPanel)
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
        self.pageDesc.setText(i18n(_w.desc))
        #self.pageIcon.setPixmap(QPixmap(locate("data", _w.icon)))

        _w.shown()

        if self.getCurrent() == 1:
            self.buttonBack

        # hide next and show finish buttons on last screen
        if self.getCurrent() == len(screenId):
            self.buttonNext.hide()
            self.buttonFinish.show()
        else:
            self.buttonNext.show()
            self.buttonFinish.hide()

        # hide back button on first screen
        if self.getCurrent() == 1:
            self.buttonBack.hide()
        else:
            self.buttonBack.show()

    def slotNext(self):
        _w = self.pageStack.visibleWidget()
        _w.execute()
        stepBatch = ""
        stepBatch += self.putBr(screenId[1])

        for sId in screenId:
            if  sId < len(screenId):
                if sId == self.getCurrent():
                    stepBatch+= self.putBold(screenId[sId+1])
                else:
                    stepBatch+= self.putBr(screenId[sId +1])

        self.pixSteps.setText(stepBatch)
        self.stackMove(self.getCurrent() + 1)

    def putBr(self, item):
        return item + "<br>"

    def putBold(self, item):
        return "<b>" + item + "</b><br>"

    def slotBack(self):
        stepBatch = ""
        for sId in screenId:
            if  sId <= len(screenId) and not sId == 1:
                if sId == self.getCurrent():
                    stepBatch+= self.putBold(screenId[sId - 1])
                else:
                    stepBatch+= self.putBr(screenId[sId - 1])
        stepBatch+= self.putBr(screenId[len(screenId)])
        self.pixSteps.setText(stepBatch)

        self.stackMove(self.getCurrent() - 1)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            qApp.quit()

    def __del__(self):
        self.tmpThumbDir = os.path.join(os.path.expanduser("~"), ".kde/share/apps/kaptan/kaptan-thumbs")

        if os.path.exists(self.tmpThumbDir):
            for root, dirs, files in os.walk(self.tmpThumbDir):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(self.tmpThumbDir)
        config = KConfig("kaptanrc")
        config.setGroup("General")
        config.writeEntry("RunOnStart", "False")
        config.sync()

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
        print i18n('Kaptan is already running.')
        sys.exit(1)

    kapp = KUniqueApplication(True, True, True)
    kaptan = Kaptan()

    # other themes don't look good
    style = QStyleFactory.create("QtCurve")
    kapp.setStyle(style)

    kaptan.setCaption(i18n('Welcome to Kaptan'))
    kaptan.setIcon(QPixmap(locate("data", "kaptan/pics/default_icon.png")))
    kaptan.show()
    kapp.setMainWidget(kaptan)
    sys.exit(kapp.exec_loop())


#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import sys

from qt import *
from kdecore import *
from kdeui import *

import mainwin
from icons import icons
import comar

def I18N_NOOP(x):
    return x

mod_version = "1.1"
mod_app = "network-manager"


def AboutData():
    return KAboutData(
        mod_app,
        "Network Manager",
        mod_version,
        I18N_NOOP("Network Manager"),
        KAboutData.License_GPL,
        "(C) 2005-2006 UEKAE/TÜBİTAK",
        None,
        None,
        "bugs@pardus.org.tr"
    )

def attachMainWidget(self):
    KGlobal.iconLoader().addAppDir(mod_app)
    icons.load_icons()
    self.mainwidget = mainwin.Widget(self)
    toplayout = QVBoxLayout(self, 0, KDialog.spacingHint())
    toplayout.addWidget(self.mainwidget)
    self.aboutus = KAboutApplication(self)


class Module(KCModule):
    def __init__(self, parent, name):
        KCModule.__init__(self, parent, name)
        KGlobal.locale().insertCatalogue(mod_app)
        self.config = KConfig(mod_app)
        self.setButtons(self.Help)
        self.aboutdata = AboutData()
        attachMainWidget(self)
    
    def aboutData(self):
        return self.aboutdata


# KCModule factory
def create_network_manager(parent, name):
    global kapp
    
    kapp = KApplication.kApplication()
    return Module(parent, name)


# Standalone
def main():
    global kapp
    
    about = AboutData()
    KCmdLineArgs.init(sys.argv, about)
    KUniqueApplication.addCmdLineOptions()
    
    if not KUniqueApplication.start():
        print i18n("Network manager module is already started!")
        return
    
    kapp = KUniqueApplication(True, True, True)
    win = QDialog()
    win.setCaption(i18n("Network Manager"))
    win.setMinimumSize(520, 440)
    win.resize(520, 440)
    attachMainWidget(win)
    kapp.setMainWidget(win)
    sys.exit(win.exec_loop())


if __name__ == "__main__":
    main()

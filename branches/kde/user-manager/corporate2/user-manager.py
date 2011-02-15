#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

import sys

from qt import *
from kdecore import *
from kdeui import *

import dbus
import dbus.mainloop.qt3

import um_mainview
from um_utility import *

mod_version = "2.2"
mod_app = "user-manager"


def AboutData():
    return KAboutData(
        mod_app,
        "User Manager",
        mod_version,
        I18N_NOOP("User Management"),
        KAboutData.License_GPL,
        "(C) 2005-2008 UEKAE/TÜBİTAK",
        None,
        None,
        "bugs@pardus.org.tr"
    )

def attachMainWidget(self):
    KGlobal.iconLoader().addAppDir(mod_app)
    self.mainwidget = um_mainview.UserManager(self)
    toplayout = QVBoxLayout(self, 0, KDialog.spacingHint())
    toplayout.addWidget(self.mainwidget)
    self.aboutus = KAboutApplication(self)


class Module(KCModule):
    def __init__(self, parent, name):
        KCModule.__init__(self, parent, name)
        KGlobal.locale().insertCatalogue(mod_app)
        self.config = KConfig(mod_app)
        self.setButtons(0)
        self.aboutdata = AboutData()
        attachMainWidget(self)

    def aboutData(self):
        return self.aboutdata


# KCModule factory
def create_user_manager(parent, name):
    global kapp

    kapp = KApplication.kApplication()
    if not dbus.get_default_main_loop():
        dbus.mainloop.qt3.DBusQtMainLoop(set_as_default=True)
    return Module(parent, name)


# Standalone
def main():
    global kapp

    dbus.mainloop.qt3.DBusQtMainLoop(set_as_default=True)

    about = AboutData()
    KCmdLineArgs.init(sys.argv, about)
    KUniqueApplication.addCmdLineOptions()

    if not KUniqueApplication.start():
        print i18n("User manager module is already started!")
        return

    kapp = KUniqueApplication(True, True, True)
    win = QDialog()
    win.setCaption(i18n("User Manager"))
    win.setMinimumSize(620, 460)
    win.resize(620, 460)
    attachMainWidget(win)
    win.setIcon(getIconSet("kuser").pixmap(QIconSet.Small, QIconSet.Normal))
    kapp.setMainWidget(win)
    sys.exit(win.exec_loop())

if __name__ == "__main__":
    main()

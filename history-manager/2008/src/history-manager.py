#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2008, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.

import sys

from utility import *
from historygui import formMain
from history_gui import *

import dbus

def attachMainWidget(self):
    KGlobal.iconLoader().addAppDir(mod_app)
    self.mainwidget = widgetMain(self)
    toplayout = QVBoxLayout(self, 0, KDialog.spacingHint())
    toplayout.addWidget(self.mainwidget)
    self.aboutus = KAboutApplication(self)

class Module(KCModule):
    def __init__(self, parent, name):
        KCModule.__init__(self, parent, name)
        KGlobal.locale().insertCatalogue(mod_app)
        self.config = KConfig(mod_app)
        self.aboutData = AboutData()
        attachMainWidget(self)

    def aboutData(self):
        return self.aboutData

def create_history_manager(parent, name):
    global kapp

    kapp = KApplication.kApplication()
    return Module(parent, name)

def main():
    global kapp

    about = AboutData()
    KCmdLineArgs.init(sys.argv, about)
    KUniqueApplication.addCmdLineOptions()

    if not KUniqueApplication.start():
        print i18n('History Manager is already running!')
        return

    kapp = KUniqueApplication(True, True, True)

    dbus.mainloop.qt3.DBusQtMainLoop(set_as_default=True)

    win = QDialog()
    win.setCaption(i18n('History Manager'))
    win.setIcon(loadIconSet("date").pixmap(QIconSet.Small, QIconSet.Normal))
    attachMainWidget(win)
    kapp.setMainWidget(win)

    sys.exit(win.exec_loop())

if __name__ == '__main__':
    main()

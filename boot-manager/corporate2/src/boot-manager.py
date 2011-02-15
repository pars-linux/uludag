#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009, TUBITAK/UEKAE
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

import bm_mainview
from bm_utility import *

import dbus.mainloop.qt3
import dbus

mod_name = 'Boot Manager'
mod_app = 'boot-manager'
mod_version = '1.1.1'

def AboutData():
    about_data = KAboutData(
        mod_app,
        mod_name,
        mod_version,
        I18N_NOOP('Boot Manager'),
        KAboutData.License_GPL,
        '(C) 2006-2010 UEKAE/TÜBİTAK',
        None,
        None,
        'bugs@pardus.org.tr'
    )
    about_data.addAuthor("Bahadır Kandemir", I18N_NOOP("Developer"), "bahadir@pardus.org.tr")
    about_data.addAuthor("Mehmet Özdemir", I18N_NOOP("Developer"), "mehmet@pardus.org.tr")
    about_data.addAuthor("Gökmen Göksel", I18N_NOOP("Developer"), "gokmen@pardus.org.tr")
    about_data.addAuthor("Fred Gansevles", I18N_NOOP("Contributions to Boot.Loader model."), "fred@gansevles.net")
    return about_data

def attachMainWidget(self):
    KGlobal.iconLoader().addAppDir(mod_app)
    self.mainwidget = bm_mainview.widgetMain(self)
    toplayout = QVBoxLayout(self, 0, KDialog.spacingHint())
    toplayout.addWidget(self.mainwidget)
    self.aboutus = KAboutApplication(self)


class Module(KCModule):
    def __init__(self, parent, name):
        KCModule.__init__(self, parent, name)
        KGlobal.locale().insertCatalogue(mod_app)
        self.config = KConfig(mod_app)
        self.setButtons(KCModule.Apply)
        self.aboutdata = AboutData()
        attachMainWidget(self)

    def aboutData(self):
        return self.aboutdata


# KCModule factory
def create_boot_manager(parent, name):
    global kapp

    kapp = KApplication.kApplication()
    if not dbus.get_default_main_loop():
        dbus.mainloop.qt3.DBusQtMainLoop(set_as_default=True)
    return Module(parent, name)


# Standalone
def main():
    global kapp

    about = AboutData()
    KCmdLineArgs.init(sys.argv, about)
    KUniqueApplication.addCmdLineOptions()

    if not KUniqueApplication.start():
        print i18n('Boot Manager is already started!')
        return

    kapp = KUniqueApplication(True, True, True)

    dbus.mainloop.qt3.DBusQtMainLoop(set_as_default=True)

    win = QDialog()
    win.setCaption(i18n('Boot Manager'))
    win.resize(QSize(500, 400).expandedTo(win.minimumSizeHint()))
    attachMainWidget(win)
    win.setIcon(getIconSet("boot_manager").pixmap(QIconSet.Small, QIconSet.Normal))
    kapp.setMainWidget(win)
    sys.exit(win.exec_loop())


if __name__ == '__main__':
    main()

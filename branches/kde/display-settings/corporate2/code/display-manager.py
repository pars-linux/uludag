#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) TUBITAK/UEKAE
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
import kdedesigner

import dbus
from dbus.mainloop.qt3 import DBusQtMainLoop

from displaysettings.mainwidget import MainWidget
from displaysettings.utility import *


mod_name = 'Display Settings'
mod_app = 'display-settings'
mod_version = '0.5.80'

def AboutData():
    return KAboutData(
        mod_app,
        mod_name,
        mod_version,
        I18N_NOOP('Display Settings'),
        KAboutData.License_GPL,
        '(C) UEKAE/TÜBİTAK',
        None,
        None,
        'bugs@pardus.org.tr'
    )

def attachMainWidget(self):
    KGlobal.iconLoader().addAppDir(mod_app)
    self.mainwidget = MainWidget(self)
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

        self.mainwidget.layout().setMargin(0)
        self.mainwidget.frameDialogButtons.hide()

        self.connect(self.mainwidget, PYSIGNAL("configChanged"), self.changed)

        self.load()

    def load(self):
        self.mainwidget.load()

    def save(self):
        self.mainwidget.save()

    def aboutData(self):
        return self.aboutdata


# KCModule factory
def create_display_manager(parent, name):
    global kapp

    kapp = KApplication.kApplication()
    if not dbus.get_default_main_loop():
        DBusQtMainLoop(set_as_default=True)
    return Module(parent, name)


# Standalone
def main():
    global kapp

    about = AboutData()
    KCmdLineArgs.init(sys.argv, about)
    KUniqueApplication.addCmdLineOptions()

    if not KUniqueApplication.start():
        print i18n('Display Settings module is already started!')
        return

    kapp = KUniqueApplication(True, True, True)
    win = QDialog()

    DBusQtMainLoop(set_as_default=True)

    win.setCaption(i18n('Display Settings'))
    win.setMinimumSize(400, 300)
    #win.resize(500, 300)
    attachMainWidget(win)
    win.setIcon(getIconSet("randr").pixmap(QIconSet.Small, QIconSet.Normal))
    kapp.setMainWidget(win)

    QTimer.singleShot(0, win.mainwidget.load)

    sys.exit(win.exec_loop())


if __name__ == '__main__':
    main()

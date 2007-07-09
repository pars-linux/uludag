#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, TUBITAK/UEKAE
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

import mainview
from utility import *

mod_name = 'Display Manager'
mod_app = 'display-manager'
mod_version = '0.1'

def AboutData():
    return KAboutData(
        mod_app,
        mod_name,
        mod_version,
        I18N_NOOP('Display Manager'),
        KAboutData.License_GPL,
        '(C) 2007 UEKAE/TÜBİTAK',
        None,
        None,
        'bugs@pardus.org.tr'
    )

def attachMainWidget(self):
    KGlobal.iconLoader().addAppDir(mod_app)
    self.mainwidget = mainview.widgetMain(self)
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
def create_display_manager(parent, name):
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
        print i18n('Display Manager is already started!')
        return

    kapp = KUniqueApplication(True, True, True)
    win = QDialog()
    win.setCaption(i18n('Display Manager'))
    win.setMinimumSize(400, 300)
    win.resize(400, 300)
    attachMainWidget(win)
    kapp.setMainWidget(win)
    sys.exit(win.exec_loop())


if __name__ == '__main__':
    main()

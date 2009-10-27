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

import sm_mainview
from sm_utility import *

mod_name = 'Service Manager'
mod_app = 'service-manager'
mod_version = '1.2.2'

def AboutData():
    return KAboutData(
        mod_app,
        mod_name,
        mod_version,
        I18N_NOOP('Service Manager'),
        KAboutData.License_GPL,
        '(C) 2005-2006 UEKAE/TÜBİTAK',
        None,
        None,
        'bugs@pardus.org.tr'
    )

def attachMainWidget(self):
    KGlobal.iconLoader().addAppDir(mod_app)
    self.mainwidget = sm_mainview.widgetMain(self)
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
def create_service_manager(parent, name):
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
        print i18n('Service Manager is already started!')
        return

    kapp = KUniqueApplication(True, True, True)
    win = QDialog()
    win.config = KConfig(mod_app)
    win.setCaption(i18n('Service Manager'))
    win.setMinimumSize(620, 420)
    win.resize(620, 420)
    attachMainWidget(win)
    kapp.setMainWidget(win)
    sys.exit(win.exec_loop())


if __name__ == '__main__':
    main()

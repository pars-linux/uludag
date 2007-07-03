#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.

# Python Modules
import os
import sys
import time

# KDE/QT Modules
from qt import *
from kdecore import *
from kdeui import *
from kfile import *
from khtml import *

# Widget
import kdedesigner
from browser import browser
from profileHandler import profileHandler

#Utilities
from utility import *

version = '1.0'
mod_app = 'proxy-manager'

def AboutData():
    about_data = KAboutData(mod_app,
                            'Proxy Manager',
                            version,
                            'Proxy Manager Interface',
                            KAboutData.License_GPL,
                            '(C) 2007 UEKAE/TÜBİTAK',
                            None, None,
                            'rmznbrtn@gmail.com')
    about_data.addAuthor('R. Bertan Gündoğdu', None, 'rmznbrtn@gmail.com')

    return about_data


def create_proxy_manager(parent, name):
    global kapp
    kapp = KApplication.kApplication()
    return Module(parent, name)


class Module(KCModule):
    def __init__(self, parent, name):
        KCModule.__init__(self, parent, name)
        KGlobal.locale().insertCatalogue(mod_app)
        KGlobal.iconLoader().addAppDir(mod_app)
        self.config = KConfig(mod_app)
        self.aboutdata = AboutData()
        widget = browser(self)
        toplayout = QVBoxLayout(self, 0, KDialog.spacingHint())
        toplayout.addWidget(widget)
    def aboutData(self):
        return self.aboutdata

def main():
    about_data = AboutData()
    KCmdLineArgs.init(sys.argv, about_data)
    if not KUniqueApplication.start():
        print i18n('Proxy Manager is already running!')
        return
    app = KUniqueApplication(True, True, True)

    win = QDialog()
    win.setCaption(i18n('Proxy Manager'))
    win.setIcon(loadIconSet("proxy").pixmap(QIconSet.Small, QIconSet.Normal))
    widget = browser(win)
    win.aboutus = KAboutApplication(win)
    toplayout = QVBoxLayout(win, 0, KDialog.spacingHint())
    toplayout.addWidget(widget)
    win.setMinimumSize(620, 420)
    win.resize(620, 420)

    app.setMainWidget(win)
    sys.exit(win.exec_loop())

# FIXME: fix here
if __name__ == '__main__':
    main()

#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import sys

from PyQt4 import QtGui
from PyQt4.QtCore import *

from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

import dbus

from about import aboutData
from localedata import setSystemLocale
from ui_pminstaller import Ui_PMInstaller

class PMInstaller(QtGui.QDialog, Ui_PMInstaller):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.Window)

    def closeEvent(self, event):
        event.ignore()
    
if __name__ == '__main__':

    KCmdLineArgs.init(sys.argv, aboutData)

    options = KCmdLineOptions()
    options.add("+files", ki18n("Packages to install"))
    KCmdLineArgs.addCmdLineOptions(options)

    if not KUniqueApplication.start():
        print i18n('Package Installer is already started!')
        sys.exit()

    app = KUniqueApplication(True, True)
    app.connect(app, SIGNAL('lastWindowClosed()'), app.quit)

    args = KCmdLineArgs.parsedArgs()

    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default = True)

    setSystemLocale()

    installer = PMInstaller()
    installer.exec_()

    app.exec_()

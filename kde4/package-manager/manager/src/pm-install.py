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

import backend
from about import aboutData
from localedata import setSystemLocale
from ui_pminstaller import Ui_PMInstaller

class Operation(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.iface = backend.pm.Iface()
        self.iface.setHandler(self.handler)
        self.iface.setExceptionHandler(self.exceptionHandler)

    def handler(self, package, signal, args):
        if signal == "status":
            signal = args[0]
            args = args[1:]

        if signal == "finished":
            print "finished"
        elif signal == "status" and args[0] in ["installing", "removing", "extracting", "configuring"]:
            operation = args[0]
            package = args[1]
            print "%s - %s" % (operation, package)

    def install(self, packages):
        self.iface.installPackages(packages)
    
    def exceptionHandler(self, exception):
        self.messageBox = QtGui.QMessageBox(i18n("Pisi Error"), unicode(exception), QtGui.QMessageBox.Critical, QtGui.QMessageBox.Ok, 0, 0)
        self.messageBox.show()

class PMInstaller(QtGui.QDialog, Ui_PMInstaller):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.operation = Operation()

if __name__ == '__main__':

    KCmdLineArgs.init(sys.argv, aboutData)

    options = KCmdLineOptions()
    options.add("+files", ki18n("Packages to install"))
    KCmdLineArgs.addCmdLineOptions(options)

    if not KUniqueApplication.start():
        print i18n('Package Installer is already started!')
        sys.exit()

    app = KUniqueApplication(True, True)
    args = KCmdLineArgs.parsedArgs()

    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default = True)

    setSystemLocale()

    installer = PMInstaller()
    installer.exec_()

    app.exec_()

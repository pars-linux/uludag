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

import os
import sys

from PyQt4 import QtGui
from PyQt4.QtCore import *

from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

import dbus

import backend
from localedata import setSystemLocale
from ui_pminstaller import Ui_PMInstaller

class Operation(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.statusChanges = 0
        self.packages = []
        self.iface = backend.pm.Iface()
        self.iface.setHandler(self.handler)
        self.iface.setExceptionHandler(self.exceptionHandler)

    def handler(self, package, signal, args):
        if signal == "status":
            signal = str(args[0])
            args = args[1:]

        if signal == "finished":
            self.emit(SIGNAL("operationChanged(QString)"), "Succesfully finished installing %s" % os.path.basename(self.packages[0]))

        elif signal in ["installing", "extracting", "configuring"]:
            self.statusChanges += 1
            self.updateProgress()
            # operation = signal
            # package = args[0]
            # self.emit(SIGNAL("operationChanged(QString)"), "Installing %s" % package)

    def updateProgress(self):
        try:
            percent = (self.statusChanges * 100) / (len(self.packages) * 3)
        except ZeroDivisionError:
            percent = 0

        self.emit(SIGNAL("progress(int)"), percent)

    def install(self, packages):
        self.packages = packages
        self.iface.installPackages(self.packages)
    
    def exceptionHandler(self, exception):
        self.messageBox = QtGui.QMessageBox(i18n("Pisi Error"), unicode(exception), QtGui.QMessageBox.Critical, QtGui.QMessageBox.Ok, 0, 0)
        self.messageBox.show()

class PMInstaller(QtGui.QDialog, Ui_PMInstaller):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.operationText.setText("")
        self.operation = Operation()
        self.connect(self.operation, SIGNAL("progress(int)"), self.progressBar.setValue)
        self.connect(self.operation, SIGNAL("operationChanged(QString)"), self.operationText.setText)

    def install(self, packages):
        self.operationText.setText("Installing %s" % os.path.basename(packages[0]))
        self.operation.install(packages)

if __name__ == '__main__':

    appName     = "pm-install"
    catalog     = ""
    programName = ki18n("pm-install")
    version     = "0.1"
    aboutData   = KAboutData(appName, catalog, programName, version)
    aboutData.setProgramIconName(":/data/package-manager.png")
    KCmdLineArgs.init(sys.argv, aboutData)

    options = KCmdLineOptions()
    options.add("+files", ki18n("Packages to install"))
    KCmdLineArgs.addCmdLineOptions(options)

    if not KUniqueApplication.start():
        print i18n('Package Installer is already started!')
        sys.exit()

    app = KUniqueApplication(True, True)
    args = KCmdLineArgs.parsedArgs()

    packages = []
    for i in range(args.count()):
        package = str(args.url(i).toLocalFile())
        print package
        if package.endswith(".pisi"):
            packages.append(package)

    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default = True)

    setSystemLocale()

    installer = PMInstaller()
    installer.show()
    installer.install(packages)

    app.exec_()

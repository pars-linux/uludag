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
            self.emit(SIGNAL("operationChanged(QString)"), i18n("Succesfully finished installing %1", os.path.basename(self.packages[0])))
            self.emit(SIGNAL("finished()"))

        if signal == "cancelled":
            KApplication.kApplication().quit()

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

    def cancel(self):
        self.iface.cancel()

    def install(self, packages):
        self.packages = packages
        self.iface.installPackages(self.packages)

    def exceptionHandler(self, message):
        message = str(message)

        if "urlopen error" in message or "Socket Error" in message:
            errorTitle = i18n("Network Error")
            errorMessage = i18n("Please check your network connections and try again.")
        elif "Access denied" in message or "tr.org.pardus.comar.Comar.PolicyKit" in message:
            errorTitle = i18n("Authorization Error")
            errorMessage = i18n("You are not authorized for this operation.")
        else:
            errorTitle = i18n("Pisi Error")
            errorMessage = message

        self.messageBox = QtGui.QMessageBox(errorTitle, errorMessage, QtGui.QMessageBox.Critical, QtGui.QMessageBox.Ok, 0, 0)
        self.messageBox.exec_()
        KApplication.kApplication().quit()

class MainWindow(KMainWindow):
    def __init__(self, parent=None):
        KMainWindow.__init__(self, parent)
        self.setWindowTitle(i18n("Package Installer"))
        widget = PMInstaller(self)
        self.resize(widget.size())
        self.setCentralWidget(widget)
        self.center()

    def center(self):
        desktop = QtGui.QApplication.desktop()
        x = (desktop.width() - self.size().width()) / 2
        y = (desktop.height() - self.size().height()) / 2 - 50
        self.move(x, y)

    def install(self, packages):
        self.centralWidget().install(packages)

class PMInstaller(QtGui.QWidget, Ui_PMInstaller):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.operationText.setText("")
        self.operation = Operation()
        self.connect(self.operation, SIGNAL("progress(int)"), self.progressBar.setValue)
        self.connect(self.operation, SIGNAL("operationChanged(QString)"), self.operationText.setText)
        self.connect(self.operation, SIGNAL("finished()"), self.finished)
        self.connect(self.actionButton, SIGNAL("clicked()"), self.operation.cancel)

    def finished(self):
        self.actionButton.setText(i18n("Ok"))
        self.connect(self.actionButton, SIGNAL("clicked()"), self.parent.close)

    def install(self, packages):
        self.operationText.setText(i18n("Installing %1", os.path.basename(packages[0])))
        self.operation.install(packages)

if __name__ == '__main__':

    appName     = "pm-install"
    catalog     = "package-manager"
    programName = ki18n("pm-install")
    version     = "0.1"
    aboutData   = KAboutData(appName, catalog, programName, version)
    aboutData.setProgramIconName("package-manager")
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

    app.connect(app, SIGNAL('lastWindowClosed()'), app.quit)

    installer = MainWindow()
    installer.show()
    installer.install(packages)

    app.exec_()

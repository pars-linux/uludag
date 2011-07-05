#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009-2010, TUBITAK/UEKAE
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
from ui_pmoffline import Ui_PMOffline

from offline import OfflineManager

class Operation(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.offlinemanager = OfflineManager()
        self.offlinemanager.setActionHandler(self.handler)
        self.offlinemanager.setExceptionHandler(self.exceptionHandler)
        self.connect(self.offlinemanager, SIGNAL("operationChanged(QString)"), SIGNAL("operationChanged(QString)"))
        self.connect(self.offlinemanager, SIGNAL("totalProgress(int)"), SIGNAL("totalProgress(int)"))
        self.connect(self.offlinemanager, SIGNAL("currentProgress(int)"), SIGNAL("currentProgress(int)"))
        self.connect(self.offlinemanager, SIGNAL("finished()"), SIGNAL("finished()"))

    def handler(self, package, signal, args):
        if signal == "cancelled":
            KApplication.kApplication().quit()

    def startProcesses(self, archive):
        self.offlinemanager.startProcesses(archive)

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
        self.setWindowTitle(i18n("Offline Package Manager"))
        widget = PMOffline(self)
        self.resize(widget.size())
        self.setCentralWidget(widget)
        self.center()

    def center(self):
        desktop = QtGui.QApplication.desktop()
        x = (desktop.width() - self.size().width()) / 2
        y = (desktop.height() - self.size().height()) / 2 - 50
        self.move(x, y)

    def startProcesses(self, archive):
        self.centralWidget().startProcesses(archive)

class PMOffline(QtGui.QWidget, Ui_PMOffline):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.operationText.setText("")
        self.operation = Operation()
        self.connect(self.operation, SIGNAL("totalProgress(int)"), self.generalProgressBar.setValue)
        self.connect(self.operation, SIGNAL("currentProgress(int)"), self.currentProgressBar.setValue)
        self.connect(self.operation, SIGNAL("operationChanged(QString)"), self.operationText.setText)
        self.connect(self.operation, SIGNAL("finished()"), self.finished)

    def finished(self):
        self.operationText.setText("All processes completed successfully.")
        self.actionButton.setEnabled(True)
        self.connect(self.actionButton, SIGNAL("clicked()"), self.parent.close)

    def startProcesses(self, archive):
        self.operation.startProcesses(archive)

if __name__ == '__main__':

    appName     = "pm-offline"
    catalog     = "package-manager"
    programName = ki18n("pm-offline")
    version     = "0.1"
    aboutData   = KAboutData(appName, catalog, programName, version)
    aboutData.setProgramIconName("package-manager")
    KCmdLineArgs.init(sys.argv, aboutData)

    options = KCmdLineOptions()
    options.add("+files", ki18n("Offline Archive Files to install or remove packages"))
    KCmdLineArgs.addCmdLineOptions(options)

    if not KUniqueApplication.start():
        print i18n('Offline Package Manager is already started!')
        sys.exit()

    app = KUniqueApplication(True, True)
    args = KCmdLineArgs.parsedArgs()

    archives = []
    for i in range(args.count()):
        archive = str(args.url(i).toLocalFile())
        print archive
        if archive.endswith(".offline"):
            archives.append(archive)

    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default = True)

    setSystemLocale()

    app.connect(app, SIGNAL('lastWindowClosed()'), app.quit)

    offline = MainWindow()
    offline.show()
    for archive in archives:
        offline.startProcesses(archive)

    app.exec_()

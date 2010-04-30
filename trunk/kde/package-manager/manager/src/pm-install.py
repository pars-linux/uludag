#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009-2010 TUBITAK/UEKAE
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
import dbus

from PyQt4 import QtGui
from PyQt4.QtCore import *

import backend
from localedata import setSystemLocale
from ui_pminstaller import Ui_PMInstaller

from pds.quniqueapp import QUniqueApplication
from context import i18n
from context import Pds
import pds

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

        if signal == "finished" and "installPackage" in args[0]:
            if len(self.packages) == 1:
                self.emit(SIGNAL("operationChanged(QString)"), 
                        i18n("Succesfully finished installing %1", 
                            self.packages[0]))
            else:
                self.emit(SIGNAL("operationChanged(QString)"), 
                        i18n("Succesfully finished installing packages"))

            self.emit(SIGNAL("finished()"))

        if signal == "cancelled":
            QUniqueApplication.quit()

        elif signal in ["installing", "extracting", "configuring", "fetching"]:
            self.statusChanges += 1
            self.updateProgress()
            package = args[0]
            if signal == "installing":
                self.emit(SIGNAL("operationChanged(QString)"), 
                        "Installing %s %s" % (package, i18n("%p%")))
            elif signal == "fetching":
                self.emit(SIGNAL("operationChanged(QString)"), 
                        "Fetching %s %s" % (package, i18n("%p%")))
            elif signal == "configuring":
                self.emit(SIGNAL("operationChanged(QString)"), 
                        "Configuring %s %s" % (package, i18n("%p%")))
            elif signal == "extracting":
                self.emit(SIGNAL("operationChanged(QString)"), 
                        "Extracting %s %s" % (package, i18n("%p%")))

    def updateProgress(self):
        try:
            percent = (self.statusChanges * 100) / (len(self.packages) * 3)
        except ZeroDivisionError:
            percent = 0

        self.emit(SIGNAL("progress(int)"), percent)

    def install(self, packages):
        self.packages = packages
        self.iface.installPackages(self.packages)

    def exceptionHandler(self, message):
        message = str(message)

        if "urlopen error" in message or "Socket Error" in message:
            errorTitle = i18n("Network Error")
            errorMessage = \
                    i18n("Please check your network connections and try again.")
        elif "Access denied" in message or \
                "tr.org.pardus.comar.Comar.PolicyKit" in message:
            errorTitle = i18n("Authorization Error")
            errorMessage = i18n("You are not authorized for this operation.")
        else:
            errorTitle = i18n("Pisi Error")
            errorMessage = message

        self.messageBox = QtGui.QMessageBox(errorTitle, errorMessage, 
                QtGui.QMessageBox.Critical, QtGui.QMessageBox.Ok, 0, 0)
        self.messageBox.exec_()
        QUniqueApplication.quit()

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
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
        self.operation = Operation()
        self.connect(self.operation, SIGNAL("progress(int)"), 
                self.progressBar.setValue)
        self.connect(self.operation, SIGNAL("operationChanged(QString)"), 
                self.progressBar.setFormat)
        self.connect(self.operation, SIGNAL("finished()"), self.finished)

    def finished(self):
        QTimer.singleShot(2000, self.parent.close)
        if Pds.session == pds.Kde4:
            from PyKDE4.kdeui import KNotification
            from PyKDE4.kdecore import KComponentData
            KNotification.event("Summary",
                    self.progressBar.format(),
                    QtGui.QPixmap(),
                    None,
                    KNotification.CloseOnTimeout,
                    KComponentData("package-manager", "package-manager", 
                        KComponentData.SkipMainComponentRegistration)
                    )
        else:
            Pds.notify(unicode(i18n('Summary')), 
                    unicode(self.progressBar.format()), 'package-manager')

    def install(self, packages):
        self.operation.install(packages)

if __name__ == '__main__':

    import os
    import sys
    from optparse import OptionParser

    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-p", "--from-repository", dest="fromrepo",
                      action="store_true", default=False,
                      help="packages to install from repository")

    (options, args) = parser.parse_args()

    if not options or not args:
        parser.print_help()
        sys.exit(0)
    packages = args

    app = QUniqueApplication(sys.argv, catalog='pm-install')
    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default = True)

    setSystemLocale()

    installer = MainWindow()
    app.setMainWindow(installer)
    installer.show()
    installer.install(packages)

    app.exec_()

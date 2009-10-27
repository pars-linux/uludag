#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# System
import sys
import os
import shutil
import subprocess
import dbus

# Qt Stuff
from PyQt4 import QtGui
from PyQt4 import QtCore

# PyKDE4 Stuff
from PyKDE4.kdeui import KApplication, KAboutApplicationDialog, KSystemTrayIcon, KMessageBox
from PyKDE4.kdecore import KAboutData, KCmdLineArgs

from ui_puma import Ui_MainWindow
from about import *

from backend import Interface
from pumaconf import *


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)

        self.setWindowTitle('Puma')
        self.setWindowIcon(QtGui.QIcon(":/icons/icons/manager.png"))

        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

        self.ifc = Interface()

    @QtCore.pyqtSignature("bool")
    def on_actionQt_About_triggered(self):
        QtGui.QMessageBox.aboutQt(self)

    @QtCore.pyqtSignature("bool")
    def on_pushButton_clicked(self):
        print self.ifc.adslstart()

    @QtCore.pyqtSignature("bool")
    def on_pushButton_2_clicked(self):
        self.close()

    @QtCore.pyqtSignature("bool")
    def on_actionExit_triggered(self):
        app.exit()

    @QtCore.pyqtSignature("bool")
    def on_actionAbout_triggered(self):
        KAboutApplicationDialog(aboutData, self).show()

    @QtCore.pyqtSignature("bool")
    def on_actionSave_triggered(self):
        self.ifc.saveconf()


    QtCore.pyqtSignature("bool")
    def on_actionHelp_triggered(self):
        QtGui.QMessageBox.question(self,
                QtGui.QApplication.translate("MainWindow", "Help Puma"),
                QtGui.QApplication.translate("MainWindow", "Authors :\n Cihan Okyay <okyaycihan@gmail.com>\n\n Project page :\n https://sourceforge.net/projects/pumaproject/\n\n Source code : https://pumaproject.svn.sourceforge.net/svnroot/pumaproject/\n\n  Usage :\n http://pumaproject.sourceforge.net/"),
                )

    @QtCore.pyqtSignature("bool")
    def on_actionDisconnect_triggered(self):
        self.ifc.adslstop()

if not dbus.get_default_main_loop():
    from dbus.mainloop.qt import DBusQtMainLoop
    DBusQtMainLoop(set_as_default=True)

aboutData = KAboutData(appName, catalog, programName, version, description, license, copyright, text, homePage, bugEmail)

KCmdLineArgs.init(sys.argv, aboutData)

app = KApplication()
app.setQuitOnLastWindowClosed(False)
mw = MainWindow()
mw.show()


aboutData.setProgramIconName(":/icons/icons/manager.png")
aboutData.addAuthor(ki18n("Cihan Okyay"), ki18n("Current Maintainer"), "okyaycihan@gmail.com")

def showw(event):
    if event == QtGui.QSystemTrayIcon.Trigger:
        if not mw.isVisible():
            mw.show()
        else:
            mw.hide()


menu = QtGui.QMenu()

exitAction = QtGui.QAction(QtGui.QIcon(":/icons/icons/exit.png"), (u"Exit"), None)
connectAction = QtGui.QAction(QtGui.QIcon(":/icons/icons/ok.png"), (u"Connect"), None)
disconnectAction = QtGui.QAction(QtGui.QIcon(":/icons/icons/disconnet.png"), (u"Disconnect"), None)

QtCore.QObject.connect(exitAction, QtCore.SIGNAL("triggered(bool)"), app.exit)
QtCore.QObject.connect(connectAction, QtCore.SIGNAL("triggered(bool)"), mw.connect)
QtCore.QObject.connect(disconnectAction, QtCore.SIGNAL("triggered(bool)"), mw.disconnect)

menu.addAction(connectAction)
menu.addAction(disconnectAction)
menu.addSeparator()
menu.addAction(exitAction)


tray = KSystemTrayIcon(QtGui.QIcon(":/icons/icons/manager.png"))

QtCore.QObject.connect(tray, QtCore.SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), showw)
tray.setContextMenu(menu)

tray.show()
import pumaicons_rc

app.exec_()


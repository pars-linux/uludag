#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import re
import time

from PyQt4 import QtGui
from PyQt4 import QtCore

import sys
import dbus


from PyKDE4.kdeui import KMainWindow, KApplication, KCModule, KIcon
from PyKDE4.kdecore import KCmdLineArgs, KGlobal
from PyKDE4.kdecore import KAboutData, ki18n, ki18nc

from peditlabel import PEditLabel

PACKAGE = "Sample"
appName     = "sample"
modName     = "sample"
programName = ki18n(PACKAGE)
version     = "1.0.0"
description = ki18n(PACKAGE)
license     = KAboutData.License_GPL
copyright   = ki18n("(c) 2006-2011 TUBITAK/UEKAE")
text        = ki18n(None)
homePage    = "http://developer.pardus.org.tr/projects/sample"
bugEmail    = "bugs@pardus.org.tr"
catalog     = appName
aboutData   = KAboutData(appName, catalog, programName, version, description, license, copyright, text, homePage, bugEmail)
aboutData.setProgramIconName("computer")


class MainWindow(KMainWindow):
    def __init__(self, parent=None):
        KMainWindow.__init__(self, parent)
        #self.resize(QtCore.QSize(800,800))
        #self.setMaximumSize(QtCore.QSize(800,800))
        #self.setMinimumSize(QtCore.QSize(800,800))

        centralWidget = QtGui.QWidget(self)
        centralWidget.setStyleSheet( "background-color: rgb( 8,8,228 )" )

        #centralWidget.setMinimumSize(QtCore.QSize(400,400))
        #centralWidget.setMaximumSize(QtCore.QSize(400,400))

        layout = QtGui.QHBoxLayout(centralWidget)

        widget = PEditLabel(centralWidget, "deneme mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")
        #widget.setStyleSheet( "background-color: rgb( 0,0,0 )" )
        #www = QtGui.QWidget(centralWidget)
        #QtGui.QLabel("wwww", www)
        layout.addWidget(widget)

        w2 = QtGui.QWidget(centralWidget)
        #w2.setMinimumWidth(400)
        w2.setStyleSheet( "background-color: rgb( 255,0,0 )" )
        QtGui.QLabel("eee", w2)
        layout.addWidget(w2)

        self.setCentralWidget(centralWidget)


if __name__ == "__main__":

    KCmdLineArgs.init(sys.argv, aboutData)
    app = KApplication()

    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default=True)

    window = MainWindow()
    window.show()

    app.exec_()


class Module(KCModule):
    def __init__(self, component_data, parent):
        KCModule.__init__(self, component_data, parent)

        KGlobal.locale().insertCatalog(catalog)

        if not dbus.get_default_main_loop():
            from dbus.mainloop.qt import DBusQtMainLoop
            DBusQtMainLoop(set_as_default=True)

        MainWidget(self, embed=True)


def CreatePlugin(widget_parent, parent, component_data):
    return Module(component_data, parent)



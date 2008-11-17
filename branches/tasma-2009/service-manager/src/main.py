#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2008, TUBITAK/UEKAE
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
import comar

# Qt Stuff
from PyQt4 import QtGui
from PyQt4.QtCore import *

# PyKDE4 Stuff
from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

# Application Stuff
from about import aboutData
from ui import Ui_mainManager

# DBUS-QT
from dbus.mainloop.qt import DBusQtMainLoop

class MainManager(QtGui.QWidget):
    def __init__(self, parent, standAlone=True):
        QtGui.QWidget.__init__(self, parent)

        # Create the ui
        self.ui = Ui_mainManager()
        if standAlone:
            self.ui.setupUi(self)
        else:
            self.ui.setupUi(parent)

        # Call Comar
        self.link = comar.Link()

        # Fill service list
        self.getServices()

    def handleServices(self, package, exception, results):
        # Handle request and fill the listServices in the ui
        if not exception:
            ServiceItem(self.ui.listServices, results, package)

    def getServices(self):
        # Get service list from comar link
        self.link.System.Service.info(async=self.handleServices)

class ServiceItem(QtGui.QListWidgetItem):

    def __init__(self, parent, data, package):
        serviceType, serviceDesc, serviceState = data
        text = '%s\n%s' % (package, serviceDesc)
        QtGui.QListWidgetItem.__init__(self, text, parent)

        if serviceState in ('on', 'started', 'conditional_started'):
            icon = 'running'
        else:
            icon = 'notrunning'
        if not serviceType == "server":
            self.setHidden(True)
        self.setIcon(QtGui.QIcon(':data/icons/%s.png' % icon))
        self.package = package

class Manager(KMainWindow):
    def __init__ (self, *args):
        KMainWindow.__init__(self)
        self.resize (640, 480)
        self.setCentralWidget(MainManager(self))

class ServiceManager(KCModule):
    def __init__(self, component_data, parent):
        KCModule.__init__(self, component_data, parent)

        # DBUS MainLoop
        DBusQtMainLoop(set_as_default = True)
        self = MainManager(self, standAlone=False)

def CreatePlugin(widget_parent, parent, component_data):
    return ServiceManager(component_data, parent)

if __name__ == '__main__':

    # Set Command-line arguments
    KCmdLineArgs.init(sys.argv, aboutData)

    # Create a Kapplitcation instance
    app = KApplication()

    # DBUS MainLoop
    DBusQtMainLoop(set_as_default = True)

    # Create Main Widget
    mainWindow = Manager(None, 'service-manager')
    mainWindow.show()

    # Create connection for lastWindowClosed signal to quit app
    app.connect(app, SIGNAL('lastWindowClosed()'), app.quit)

    # Run the application
    app.exec_()


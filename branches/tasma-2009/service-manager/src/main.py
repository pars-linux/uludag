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
from uimain import Ui_mainManager
from uiitem import Ui_ServiceItemWidget

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
        self.widgets = {}

        # Fill service list
        self.getServices()

    def handleServices(self, package, exception, results):
        # Handle request and fill the listServices in the ui
        if not exception:
            item = ServiceItem(self.ui.listServices, results, package)
            self.widgets[package] = ServiceItemWidget(results, package, self)
            self.ui.listServices.setItemWidget(item, self.widgets[package])
            item.setSizeHint(QSize(38,38))

    def getServices(self):
        self.link.listenSignals("System.Service", self.handler)
        # Get service list from comar link
        self.link.System.Service.info(async=self.handleServices)

    def handler(self, package, signal, args):
        print args, signal, package

class ServiceItem(QtGui.QListWidgetItem):

    def __init__(self, parent, data, package):
        serviceType, serviceDesc, serviceState = data
        QtGui.QListWidgetItem.__init__(self, parent)
        if not serviceType == "server":
            self.setHidden(True)
        self.package = package

class ServiceItemWidget(QtGui.QWidget):

    def __init__(self, data, package, parent):
        QtGui.QWidget.__init__(self, None)
        self.ui = Ui_ServiceItemWidget()
        self.ui.setupUi(self)
        self.ui.labelName.setText(package)
        serviceType, serviceDesc, serviceState = data
        if serviceState in ('on', 'started', 'conditional_started'):
            icon = 'running'
        else:
            icon = 'notrunning'
        self.ui.labelStatus.setPixmap(QtGui.QPixmap(':data/icons/%s.png' % icon))
        self.ui.labelDesc.setText(serviceDesc)
        self.toggleButtons()
        self.toggled = False
        self.rootWidget = parent
        self.package = package
        self.connect(self.ui.buttonStart, SIGNAL("clicked()"), self.setService)
        self.connect(self.ui.buttonStop, SIGNAL("clicked()"), self.setService)
        self.connect(self.ui.buttonReload, SIGNAL("clicked()"), self.setService)

    def setService(self):
        try:
            if self.sender() == self.ui.buttonStart:
                self.rootWidget.link.System.Service[self.package].start()
            elif self.sender() == self.ui.buttonStop:
                self.rootWidget.link.System.Service[self.package].stop()
            elif self.sender() == self.ui.buttonReload:
                self.rootWidget.link.System.Service[self.package].reload()
        except:
            pass

    def enterEvent(self, event):
        if not self.toggled:
            self.toggleButtons(True)
            self.toggled = True

    def leaveEvent(self, event):
        if self.toggled:
            self.toggleButtons()
            self.toggled = False

    def toggleButtons(self, toggle=False):
        self.ui.buttonStart.setVisible(toggle)
        self.ui.buttonReload.setVisible(toggle)
        self.ui.buttonStop.setVisible(toggle)

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


#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
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

# Qt Stuff
from PyQt4 import QtGui
from PyQt4.QtCore import *

# PyKDE4 Stuff
from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

# Application Stuff
from about import aboutData
from uimain import Ui_mainManager
from uiitem import Ui_ProfileItem

# Network Tools
import nettools

# DBus-Qt
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

        # Init network
        self.iface = nettools.Iface()

        # Backend info
        self.backends = {}

        # Profile info
        self.profiles = {}

        # Initialize
        self.initialize()

    def initialize(self):
        # Register listeners
        self.iface.listenBackendInfo(self.handleBackendInfo)
        self.iface.listenConnectionList(self.handleConnectionList)
        self.iface.listenConnectionInfo(self.handleConnectionInfo)
        self.iface.listenConnectionNew(self.handleConnectionNew)
        self.iface.listenConnectionEdit(self.handleConnectionEdit)
        self.iface.listenConnectionDel(self.handleConnectionDel)
        self.iface.listenConnectionState(self.handleConnectionState)
        # Get backend info
        self.iface.getBackendInfo()

    def handleBackendInfo(self, package, info):
        self.backends[package] = info
        self.iface.getConnectionList(package)

    def handleConnectionList(self, package, profiles):
        for profile in profiles:
            self.iface.getConnectionInfo(package, profile)

    def handleConnectionInfo(self, package, profile, info):
        if package not in self.profiles:
            self.profiles[package] = {}
        if profile in self.profiles[package]:
            # Updated profile
            item_widget, item = self.profiles[package][profile]
            item.initialize(info)
        else:
            # New profile
            item_widget = ProfileWidgetItem(self.ui.listProfiles, info, package)
            item = ProfileItem(info, package, self)
            self.profiles[package][profile] = (item_widget, item)
            self.ui.listProfiles.setItemWidget(item_widget, item)
            item_widget.setSizeHint(QSize(100, 48))

    def handleConnectionNew(self, package, profile):
        self.iface.getConnectionInfo(package, profile)

    def handleConnectionEdit(self, package, profile):
        self.iface.getConnectionInfo(package, profile)

    def handleConnectionDel(self, package, profile):
        item_widget, item = self.profiles[package][profile]
        # Lock list here
        row = self.ui.listProfiles.row(item_widget)
        self.ui.listProfiles.takeItem(row)
        del item
        # Unlock list here

    def handleConnectionState(self, package, profile, state, message):
        item_widget, item = self.profiles[package][profile]
        item.setState(state, message)


class ProfileWidgetItem(QtGui.QListWidgetItem):
    def __init__(self, parent, data, package):
        QtGui.QListWidgetItem.__init__(self, parent)


class ProfileItem(QtGui.QWidget):
    def __init__(self, data, package, parent):
        QtGui.QWidget.__init__(self, None)

        self.ui = Ui_ProfileItem()
        self.ui.setupUi(self)

        self.toggleButtons()
        self.toggled = False

        self.rootWidget = parent
        self.package = package
        self.initialize(data)

        self.connect(self.ui.buttonDelete, SIGNAL("clicked()"), self.slotDelete)
        self.connect(self.ui.checkState, SIGNAL("clicked()"), self.slotState)

    def initialize(self, data):
        self.data = data

        self.ui.labelName.setText(data["name"])
        self.ui.labelDesc.setText("")

        if self.rootWidget.backends[self.package]["type"] == "net":
            self.ui.labelStatus.setPixmap(QtGui.QPixmap("icons/network-wired.png"))
        elif self.rootWidget.backends[self.package]["type"] == "wifi":
            self.ui.labelStatus.setPixmap(QtGui.QPixmap("icons/network-wireless.png"))

    def setState(self, state, message=""):
        if state == "up":
            self.ui.checkState.setChecked(True)
        else:
            self.ui.checkState.setChecked(False)
        if message:
            self.ui.labelDesc.setText(message)

    def slotDelete(self):
        self.rootWidget.iface.deleteConnection(self.package, self.data["name"])

    def slotState(self):
        if self.ui.checkState.isChecked():
            self.rootWidget.iface.setState(self.package, self.data["name"], "up")
        else:
            self.rootWidget.iface.setState(self.package, self.data["name"], "down")

    def enterEvent(self, event):
        if not self.toggled:
            self.toggleButtons(True)
            self.toggled = True

    def leaveEvent(self, event):
        if self.toggled:
            self.toggleButtons()
            self.toggled = False

    def toggleButtons(self, toggle=False):
        self.ui.buttonEdit.setVisible(toggle)
        self.ui.buttonDelete.setVisible(toggle)

class Manager(KMainWindow):
    def __init__ (self, *args):
        KMainWindow.__init__(self)
        self.resize(640, 480)
        self.setCentralWidget(MainManager(self))

class NetworkManager(KCModule):
    def __init__(self, component_data, parent):
        KCModule.__init__(self, component_data, parent)

        # DBus MainLoop
        DBusQtMainLoop(set_as_default=True)
        MainManager(self, standAlone=False)

def CreatePlugin(widget_parent, parent, component_data):
    return NetworkManager(component_data, parent)

if __name__ == '__main__':

    # Set Command-line arguments
    KCmdLineArgs.init(sys.argv, aboutData)

    # Create a Kapplitcation instance
    app = KApplication()

    # DBus MainLoop
    DBusQtMainLoop(set_as_default=True)

    # Create Main Widget
    mainWindow = Manager(None, 'network-manager')
    mainWindow.show()

    # Create connection for lastWindowClosed signal to quit app
    app.connect(app, SIGNAL('lastWindowClosed()'), app.quit)

    # Run the application
    app.exec_()


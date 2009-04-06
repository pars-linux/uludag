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
from backend import NetworkIface
from about import aboutData
from ui import Ui_mainManager
from widgets import ConnectionItemWidget, ConnectionItem

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
        self.iface = NetworkIface()
        self.widgets = {}

        # Fill service list
        self.connections = self.iface.connections('net-tools')
        # self.services.sort()
        for connection in self.connections:
            item = ConnectionItem(connection, self.ui.profileList)
            self.widgets[connection] = ConnectionItemWidget(connection, self, item)
            self.ui.profileList.setItemWidget(item, self.widgets[connection])
            item.setSizeHint(QSize(38,48))

        self.ui.editBox.hide()
        # self.infoCount = 0
        # self.piece = 100/len(self.services)

        # Update service status and follow Comar for state changes
        self.getConnectionStates()

    def handleConnections(self, package, exception, results):
        print package, exception, results

    def getConnectionStates(self):
        # self.iface.connections('net-tools', self.handleConnections)
        self.iface.listen(self.handler)

    def handler(self, package, signal, args):
        print "Burasi,", args, signal, package
        # self.widgets[package].setState(args[1])

    def editConnection(self):
        print self.sender().parent().package

    def deleteConnection(self):
        print self.sender().parent().package

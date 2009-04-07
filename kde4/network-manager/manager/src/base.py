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
import time
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
            item.setSizeHint(QSize(48,48))

        self.ui.editBox.hide()
        self.ui.profileList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.maxSize = False
        self.minSize = False

        self.timer = QTimer(self)
        self.connect(self.timer, SIGNAL("timeout()"), self.animate)
        self.connect(self.ui.buttonCancel, SIGNAL("clicked()"), self.closeEdit)

        # Update service status and follow Comar for state changes
        self.getConnectionStates()

    def animate(self):
        if self.maxSize:
            if self.ui.editBox.minimumHeight() < self.maxSize - 30:
                self.ui.editBox.setMinimumHeight(self.ui.editBox.minimumHeight() + 30)
            else:
                self.ui.editBox.setMinimumHeight(self.maxSize)
                self.ui.editBox.setMaximumHeight(16777215)
                self.ui.profileList.setMaximumHeight(56)
                self.maxSize = False
                self.timer.stop()
        if self.minSize:
            if self.ui.editBox.maximumHeight() > 30:
                self.ui.editBox.setMinimumHeight(self.ui.editBox.minimumHeight() - 30)
                self.ui.editBox.setMaximumHeight(self.ui.editBox.minimumHeight() - 30)
            else:
                self.ui.editBox.hide()
                self.ui.editBox.setMinimumHeight(10)
                self.ui.editBox.setMaximumHeight(10)
                self.minSize = False
                self.timer.stop()
        self.update()

    def closeEdit(self):
        self.minSize = True
        self.ui.profileList.setMaximumHeight(16777215)
        self.timer.start(0.1)
        self.showAll()

    def resizeEvent(self, event):
        if not self.ui.editBox.isHidden():
            self.ui.editBox.setMaximumHeight(self.height() - 70)
            self.ui.editBox.setMinimumHeight(self.height() - 70)

    def handleConnections(self, package, exception, results):
        print package, exception, results

    def getConnectionStates(self):
        # self.iface.connections('net-tools', self.handleConnections)
        self.iface.listen(self.handler)

    def handler(self, package, signal, args):
        print "Burasi,", args, signal, package
        # self.widgets[package].setState(args[1])

    def editConnection(self):
        self.ui.editBox.setMaximumHeight(10)
        self.ui.editBox.show()
        self.ui.profileList.setMinimumHeight(52)
        self.maxSize = self.height() - 70
        self.timer.start(0.1)
        self.hideOthers(self.sender().parent())
        print self.sender().parent().package

    def hideOthers(self, current):
        print "called"
        for widget in self.widgets.values():
            if not widget == current:
                widget.item.setHidden(True)

    def showAll(self):
        for widget in self.widgets.values():
            widget.item.setHidden(False)

    def deleteConnection(self):
        print self.sender().parent().package

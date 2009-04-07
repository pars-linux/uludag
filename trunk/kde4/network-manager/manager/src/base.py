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
from widgets import ConnectionItemWidget

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
            item = QtGui.QListWidgetItem(self.ui.profileList)
            self.widgets[connection] = ConnectionItemWidget('net-tools', connection, self, item)
            self.ui.profileList.setItemWidget(item, self.widgets[connection])
            item.setSizeHint(QSize(48,48))

        self.ui.editBox.hide()
        self.ui.profileList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.animateWidget = self.ui.editBox
        self.animateTarget = None
        self.animateItemHeight = None
        self.animateInterval = 30

        self.animator = QTimer(self)
        self.connect(self.animator, SIGNAL("timeout()"), self.animate)
        self.connect(self.ui.buttonCancel, SIGNAL("clicked()"), self.hideEditBox)

        # Update service status and follow Comar for state changes
        self.getConnectionStates()

    # Anime Naruto depends on GUI
    def animate(self):
        if self.animateWidget:
            if self.animateWidget.maximumHeight() < self.animateTarget - self.animateInterval:
                self.animateWidget.setMaximumHeight(self.animateWidget.maximumHeight() + self.animateInterval)
                self.animateWidget.setMinimumHeight(self.animateWidget.maximumHeight() + self.animateInterval)
            else:
                self.animateWidget.setMaximumHeight(16777215)
                self.animateWidget.setMinimumHeight(self.animateTarget)
                self.ui.profileList.setMaximumHeight(self.animateItemHeight)
                self.animator.stop()
        else:
            self.animator.stop()

    def hideEditBox(self):
        self.ui.editBox.hide()

    def showEditBox(self, profile, package):
        self.ui.editBox.show()

        # Define minimumListHeight
        self.animateItemHeight = self.widgets.values()[0].height() + 10
        self.ui.profileList.setMinimumHeight(self.animateItemHeight)

        # Target height
        self.animateTarget = self.height() - self.animateItemHeight - 20 # -10 for spacing
        print self.animateTarget, self.animateWidget, self.height()

        # Do animation
        self.animator.start(0.1)

    def hideOthers(self, current):
        for widget in self.widgets.values():
            if not widget == current:
                widget.item.setHidden(True)

    def showAll(self):
        for widget in self.widgets.values():
            widget.item.setHidden(False)

    # Comar operations calls gui
    def editConnection(self):
        sender = self.sender().parent()
        profile, package = sender.profile, sender.package
        self.showEditBox(profile, package)

    def deleteConnection(self):
        print self.sender().parent().package

    # Comar mangling routines
    def handleConnections(self, package, exception, results):
        print package, exception, results

    def getConnectionStates(self):
        self.iface.listen(self.handler)

    def handler(self, package, signal, args):
        print "Comar call : ", args, signal, package


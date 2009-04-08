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

UP, DOWN = range(2)
M_HEIGHT = 0

class MainManager(QtGui.QWidget):
    def __init__(self, parent, standAlone=True):
        QtGui.QWidget.__init__(self, parent)

        # Create the ui
        self.ui = Ui_mainManager()

        if standAlone:
            self.ui.setupUi(self)
            self.baseWidget = self
        else:
            self.ui.setupUi(parent)
            self.baseWidget = parent

        # Call Comar
        self.iface = NetworkIface()
        self.widgets = {}

        # Fill profile list
        self.connections = self.iface.connections('net-tools')
        self.connections.sort()
        for connection in self.connections:
            item = QtGui.QListWidgetItem(self.ui.profileList)
            self.widgets[connection] = ConnectionItemWidget('net-tools', connection, self, item)
            self.ui.profileList.setItemWidget(item, self.widgets[connection])
            item.setSizeHint(QSize(48,48))
            del item

        # Preparing for animation
        self.ui.editBox.setMaximumHeight(M_HEIGHT)
        self.lastAnimation = UP

        # Naruto
        self.animator = QTimeLine(200, self)

        # Animator connections, Naruto loves Sakura-chan
        self.connect(self.animator, SIGNAL("frameChanged(int)"), self.animate)
        self.connect(self.animator, SIGNAL("finished()"), self.animateFinished)

        # Hide editBox
        self.connect(self.ui.buttonCancel, SIGNAL("clicked()"), self.hideEditBox)

        # Update service status and follow Comar for state changes
        self.getConnectionStates()

    # Anime Naruto depends on GUI
    def animate(self, height):
        self.ui.editBox.setMaximumHeight(height)
        self.ui.profileList.setMaximumHeight(self.baseWidget.height()-height)
        self.update()

    def animateFinished(self):
        if self.lastAnimation == UP:
            self.ui.editBox.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.ui.editBox.setMaximumHeight(167777)
            self.ui.profileList.setMaximumHeight(M_HEIGHT)
        elif self.lastAnimation == DOWN:
            self.ui.profileList.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.ui.profileList.setMaximumHeight(167777)
            self.ui.editBox.setMaximumHeight(M_HEIGHT)

    def hideEditBox(self):
        self.lastAnimation = DOWN
        self.hideScrollBars()
        self.animator.setFrameRange(self.ui.editBox.height(), M_HEIGHT)
        self.animator.start()

    def showEditBox(self, profile, package):
        self.lastAnimation = UP
        self.hideScrollBars()
        self.animator.setFrameRange(M_HEIGHT, self.baseWidget.height() - M_HEIGHT)
        self.animator.start()

    def hideScrollBars(self):
        self.ui.editBox.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.profileList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

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


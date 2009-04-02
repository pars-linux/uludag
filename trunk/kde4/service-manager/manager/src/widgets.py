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

# Qt Stuff
from PyQt4 import QtGui
from PyQt4.QtCore import *

# Application Stuff
from ui import Ui_mainManager
from uiitem import Ui_ServiceItemWidget

class ServiceItem(QtGui.QListWidgetItem):

    def __init__(self, parent, data, package):
        QtGui.QListWidgetItem.__init__(self, parent)

        serviceType, serviceDesc, serviceState = data

        if not serviceType == "server":
            self.setHidden(True)

        self.package = package

class ServiceItemWidget(QtGui.QWidget):

    def __init__(self, data, package, parent):
        QtGui.QWidget.__init__(self, None)

        self.ui = Ui_ServiceItemWidget()
        self.ui.setupUi(self)

        serviceType, serviceDesc, serviceState = data

        self.setState(serviceState)
        self.ui.labelDesc.setText(serviceDesc)
        self.ui.labelName.setText(package)

        self.toggleButtons()

        self.toggled = False
        self.iface = parent.iface
        self.package = package

        self.connect(self.ui.buttonStart, SIGNAL("clicked()"), self.setService)
        self.connect(self.ui.buttonStop, SIGNAL("clicked()"), self.setService)
        self.connect(self.ui.buttonReload, SIGNAL("clicked()"), self.setService)

    def setState(self, state):
        if state in ('on', 'started', 'conditional_started'):
            icon = 'running'
        else:
            icon = 'notrunning'
        self.ui.labelStatus.setPixmap(QtGui.QPixmap(':data/%s.png' % icon))

    def setService(self):
        try:
            if self.sender() == self.ui.buttonStart:
                self.iface.start(self.package)
            elif self.sender() == self.ui.buttonStop:
                self.iface.stop(self.package)
            elif self.sender() == self.ui.buttonReload:
                self.iface.restart(self.package)
        except Exception, e:
            print e

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
        #self.ui.runOnStart.setVisible(toggle)



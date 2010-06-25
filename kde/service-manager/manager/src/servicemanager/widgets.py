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

# KDE Stuff
from PyKDE4 import kdeui

# Application Stuff
from servicemanager.ui_item import Ui_ServiceItemWidget
import time

class ServiceItem(QtGui.QListWidgetItem):

    def __init__(self, package, parent):
        QtGui.QListWidgetItem.__init__(self, parent)

        self.package = package

class ServiceItemWidget(QtGui.QWidget):

    def __init__(self, package, parent, item):
        QtGui.QWidget.__init__(self, None)

        self.ui = Ui_ServiceItemWidget()
        self.ui.setupUi(self)

        self.ui.labelName.setText(package)

        self.toggleButtons()

        self.ui.buttonStart.setIcon(kdeui.KIcon("media-playback-start"))
        self.ui.buttonStop.setIcon(kdeui.KIcon("media-playback-stop"))
        self.ui.buttonReload.setIcon(kdeui.KIcon("view-refresh"))

        self.toggled = False
        self.iface = parent.iface
        self.item = item
        self.package = package
        self.type = None
        self.desc = None
        self.connect(self.ui.buttonStart, SIGNAL("clicked()"), self.setService)
        self.connect(self.ui.buttonStop, SIGNAL("clicked()"), self.setService)
        self.connect(self.ui.buttonReload, SIGNAL("clicked()"), self.setService)
        self.connect(self.ui.checkStart, SIGNAL("clicked()"), self.setService)

    def updateService(self, data, firstRun):
        self.type, self.desc, serviceState = data
        self.setState(serviceState, firstRun)
        self.ui.labelDesc.setText(self.desc)

    def setState(self, state, firstRun=False):
        if not firstRun:
            # There is a raise condition, FIXME in System.Service
            time.sleep(1)
            state = self.iface.info(self.package)[2]
        if state in ('on', 'started', 'conditional_started'):
            self.running = True
            icon = 'flag-green'
        else:
            self.running = False
            icon = 'flag-black'
        self.ui.labelStatus.setPixmap(kdeui.KIcon(icon).pixmap(32, 32))
        self.runningAtStart = False
        if state in ('on', 'stopped'):
            self.runningAtStart = True
        elif state in ('off', 'started', 'conditional_started'):
            self.runningAtStart = False
        self.ui.checkStart.setChecked(self.runningAtStart)
        # print self.package, state

    def setService(self):
        try:
            if self.sender() == self.ui.buttonStart:
                self.iface.start(self.package)
            elif self.sender() == self.ui.buttonStop:
                self.iface.stop(self.package)
            elif self.sender() == self.ui.buttonReload:
                self.iface.restart(self.package)
            elif self.sender() == self.ui.checkStart:
                self.iface.setEnable(self.package, self.ui.checkStart.isChecked())
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
        self.ui.checkStart.setVisible(toggle)


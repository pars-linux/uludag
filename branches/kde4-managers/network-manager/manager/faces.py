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

# Qt Stuff
from PyQt4 import QtGui
from PyQt4.QtCore import *

# PyKDE4 Stuff
from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

# Application Stuff
from uimain import Ui_MainManager
from uiitem import Ui_ProfileWidget
from uisettings import Ui_DialogSettings

# Network Tools
import nettools

class MainManager(QtGui.QWidget):
    def __init__(self, parent, standAlone=True):
        QtGui.QWidget.__init__(self, parent)

        # Create the ui
        self.ui = Ui_MainManager()

        if standAlone:
            self.ui.setupUi(self)
        else:
            self.ui.setupUi(parent)

        # Init network
        self.iface = nettools.Iface()

        # Backend info
        self.backendInfo = {}

        # Profile info
        self.profiles = {}

        # Initialize
        self.initialize()

    def initialize(self):
        # Register listeners
        self.iface.listenBackendInfo(self.handleBackendInfo)
        self.iface.listenConnectionInfo(self.handleConnectionInfo)
        self.iface.listenConnectionList(self.handleConnectionList)
        self.iface.listenConnectionNew(self.handleConnectionNew)
        self.iface.listenConnectionEdit(self.handleConnectionEdit)
        self.iface.listenConnectionDel(self.handleConnectionDel)
        self.iface.listenConnectionState(self.handleConnectionState)
        # Get backend info
        self.iface.getBackendInfo()

    def handleBackendInfo(self, package, backendInfo):
        self.backendInfo[package] = backendInfo
        self.iface.getConnectionList(package)

    def handleConnectionList(self, package, profiles):
        for profile in profiles:
            self.iface.getConnectionInfo(package, profile)

    def handleConnectionInfo(self, package, profile, profileInfo):
        if package not in self.profiles:
            self.profiles[package] = {}
        if profile in self.profiles[package]:
            # Updated profile
            widget_item, widget = self.profiles[package][profile]
            widget.initialize(profileInfo)
        else:
            # New profile
            widget_item = ProfileWidgetItem(self.ui.listProfiles, package, self.backendInfo[package], profileInfo)
            widget = ProfileWidget(self, package, self.backendInfo[package], profileInfo)
            self.profiles[package][profile] = (widget_item, widget)
            self.ui.listProfiles.setItemWidget(widget_item, widget)
            widget_item.setSizeHint(QSize(100, 48))

    def handleConnectionNew(self, package, profile):
        self.iface.getConnectionInfo(package, profile)

    def handleConnectionEdit(self, package, profile):
        self.iface.getConnectionInfo(package, profile)

    def handleConnectionDel(self, package, profile):
        item_widget, item = self.profiles[package][profile]
        # Lock list here
        # row = self.ui.listProfiles.row(item_widget)
        # self.ui.listProfiles.takeItem(row)
        # del item
        # Unlock list here

    def handleConnectionState(self, package, profile, state, message):
        widget_item, widget = self.profiles[package][profile]
        widget.setState(state, message)


class Settings(QtGui.QDialog):
    def __init__(self, parent, iface, package, backendInfo, profileInfo):
        QtGui.QDialog.__init__(self, parent)

        # Create the ui
        self.ui = Ui_DialogSettings()
        self.ui.setupUi(self)

        self.iface = iface
        self.package = package
        self.backendInfo = backendInfo
        self.profileInfo = profileInfo

        modes = backendInfo["modes"].split(",")
        if "device" in modes:
            if "devicemode" not in modes:
                self.ui.comboDeviceMode.setVisible(False)
        else:
            self.ui.groupDevice.setVisible(False)
        if "remote" in modes:
            if "scan" not in modes:
                self.ui.pushRemoteScan.setVisible(False)
        else:
            self.ui.groupRemote.setVisible(False)
        if "auth" not in modes:
            self.ui.groupSecurity.setVisible(False)
        if "net" not in modes:
            self.ui.groupSecurity.setAddress(False)

        self.ui.lineName.setText(profileInfo["name"])

        self.resize(400, 1)


class ProfileWidgetItem(QtGui.QListWidgetItem):
    def __init__(self, parent, package, backendInfo, profileInfo):
        QtGui.QListWidgetItem.__init__(self, parent)


class ProfileWidget(QtGui.QWidget):
    def __init__(self, parent, package, backendInfo, profileInfo):
        QtGui.QWidget.__init__(self, None)

        self.ui = Ui_ProfileWidget()
        self.ui.setupUi(self)

        self.toggleButtons()
        self.toggled = False

        self.rootWidget = parent
        self.package = package
        self.backendInfo = backendInfo
        self.profileInfo = profileInfo
        self.initialize()

        self.connect(self.ui.buttonEdit, SIGNAL("clicked()"), self.slotEdit)
        self.connect(self.ui.buttonDelete, SIGNAL("clicked()"), self.slotDelete)
        self.connect(self.ui.checkState, SIGNAL("clicked()"), self.slotState)

    def initialize(self, profileInfo=None):
        if profileInfo:
            self.profileInfo = profileInfo

        self.ui.labelName.setText(self.profileInfo["name"])
        self.ui.labelDesc.setText("")

        if self.backendInfo["type"] == "net":
            self.ui.labelStatus.setPixmap(QtGui.QPixmap("icons/network-wired.png"))
        elif self.backendInfo["type"] == "wifi":
            self.ui.labelStatus.setPixmap(QtGui.QPixmap("icons/network-wireless.png"))

    def setState(self, state, message=""):
        if state == "up":
            self.ui.checkState.setChecked(True)
        else:
            self.ui.checkState.setChecked(False)
        if message:
            self.ui.labelDesc.setText(message)

    def slotEdit(self):
        dialog = Settings(self.rootWidget.parent(), self.rootWidget.iface, self.package, self.backendInfo, self.profileInfo)
        dialog.exec_()

    def slotDelete(self):
        self.rootWidget.iface.deleteConnection(self.package, self.profileInfo["name"])

    def slotState(self):
        if self.ui.checkState.isChecked():
            self.rootWidget.iface.setState(self.package, self.profileInfo["name"], "up")
        else:
            self.rootWidget.iface.setState(self.package, self.profileInfo["name"], "down")

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

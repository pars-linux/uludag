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
import time
import comar

# Qt Stuff
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL, Qt, QTimeLine, QSize

# KDE Stuff
from PyKDE4.kdeui import KMessageBox

# Application Stuff
from backend import NetworkIface
from ui import Ui_mainManager
from widgets import ConnectionItemWidget

# Animation Definitions
SHOW, HIDE     = range(2)
TARGET_HEIGHT  = 0
ANIMATION_TIME = 200
DEFAULT_HEIGHT = 16777215

class MainManager(QtGui.QWidget):
    def __init__(self, parent, standAlone=True):
        QtGui.QWidget.__init__(self, parent)

        # Create the ui
        self.ui = Ui_mainManager()

        # Network Manager can run as KControl Module or Standalone
        if standAlone:
            self.ui.setupUi(self)
            self.baseWidget = self
        else:
            self.ui.setupUi(parent)
            self.baseWidget = parent

        # Call Comar
        self.iface = NetworkIface()
        self.widgets = {}
        self.fillProfileList()

        # Preparing for animation
        self.ui.editBox.setMaximumHeight(TARGET_HEIGHT)
        self.lastAnimation = SHOW

        # Naruto
        self.animator = QTimeLine(ANIMATION_TIME, self)

        # Animator connections, Naruto loves Sakura-chan
        self.connect(self.animator, SIGNAL("frameChanged(int)"), self.animate)
        self.connect(self.animator, SIGNAL("finished()"), self.animateFinished)

        # Hide editBox when clicked Cancel
        self.connect(self.ui.buttonCancel, SIGNAL("clicked()"), self.hideEditBox)

        # Save changes when clicked Apply
        self.connect(self.ui.buttonApply, SIGNAL("clicked()"), self.applyChanges)

        # Filter
        self.connect(self.ui.filterBox, SIGNAL("currentIndexChanged(int)"), self.filterList)

        # Update service status and follow Comar for sate changes
        self.getConnectionStates()

    def filterList(self, filter):

        def setHidden(package=None, hidden=False):
            for widget in self.widgets.values():
                if not package:
                    widget.item.setHidden(False)
                    continue
                if widget.package == package:
                    widget.item.setHidden(hidden)
                else:
                    widget.item.setHidden(not hidden)

        # All profiles
        if filter == 0:
            setHidden()
        # Wireless profiles
        elif filter == 1:
            setHidden("wireless_tools", False)
        # Ethernet profiles
        elif filter == 2:
            setHidden("net_tools", False)

    def fillProfileList(self, ignore = None):
        # Clear the entire list
        self.ui.profileList.clear()
        self.widgets = {}

        # Fill the list with current connections
        for package in ('net_tools', 'wireless_tools'):
            # Fill profile list
            self.connections = self.iface.connections(package)
            self.connections.sort()
            for connection in self.connections:
                if ignore:
                    if package == ignore[0] and connection == ignore[1]:
                        continue
                info = self.iface.info(package, connection)
                state= str(info["state"])
                item = QtGui.QListWidgetItem(self.ui.profileList)
                item.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                self.widgets[connection] = ConnectionItemWidget(package, connection, self, item)
                self.widgets[connection].update(state)
                self.ui.profileList.setItemWidget(item, self.widgets[connection])
                item.setSizeHint(QSize(48,48))
                del item

    # Anime Naruto depends on GUI
    def animate(self, height):
        self.ui.editBox.setMaximumHeight(height)
        self.ui.profileList.setMaximumHeight(self.baseWidget.height()-height)
        self.update()

    def animateFinished(self):
        if self.lastAnimation == SHOW:
            self.ui.editBox.setMaximumHeight(DEFAULT_HEIGHT)
            self.ui.profileList.setMaximumHeight(TARGET_HEIGHT)
            self.ui.editBox.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        elif self.lastAnimation == HIDE:
            self.ui.profileList.setMaximumHeight(DEFAULT_HEIGHT)
            self.ui.editBox.setMaximumHeight(TARGET_HEIGHT)
            self.ui.profileList.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def hideEditBox(self):
        if self.lastAnimation == SHOW:
            self.lastAnimation = HIDE
            self.hideScrollBars()
            self.animator.setFrameRange(self.ui.editBox.height(), TARGET_HEIGHT)
            self.animator.start()

    def showEditBox(self, profile, package):
        sender = self.sender().parent()
        self.lastAnimation = SHOW
        self.hideScrollBars()
        self.buildEditBoxFor(sender.package, sender.profile)
        self.animator.setFrameRange(TARGET_HEIGHT, self.baseWidget.height() - TARGET_HEIGHT)
        self.animator.start()

    def hideScrollBars(self):
        self.ui.editBox.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.profileList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    # Comar operations calls gui
    def buildEditBoxFor(self, package, profile):
        ui = self.ui
        self.lastEditedPackage = package
        self.lastEditedData = data = self.iface.info(package, profile)

        devices = self.iface.devices(package)
        for device in devices:
            ui.deviceList.addItem(device)
        if len(devices) == 1:
            ui.groupDevice.hide()
        else:
            ui.groupDevice.show()

        ui.lineConnectionName.setText(data["name"])
        ui.labelDeviceDescription.setText(data["device_name"])

        if data["net_mode"] == "auto":
            self.ui.useDHCP.setChecked(True)
            if data.has_key("net_address"):
                self.ui.useCustomAddress.setChecked(True)
            if data.has_key("net_gateway"):
                self.ui.useCustomDNS.setChecked(True)
        else:
            ui.useManual.setChecked(True)

        if data.has_key("net_address"):
            ui.lineAddress.setText(data["net_address"])
            ui.lineNetworkMask.lineEdit().setText(data["net_mask"])
        if data.has_key("net_gateway"):
            ui.lineGateway.setText(data["net_gateway"])

        if data["namemode"] == "default":
            ui.useDefault.setChecked(True)
        if data["namemode"] == "auto":
            ui.useAutomatic.setChecked(True)
        if data["namemode"] == "custom":
            ui.useCustom.setChecked(True)
            ui.lineCustomDNS.setText(data["nameserver"])

    def applyChanges(self):
        ui = self.ui
        needsListUpdate = False
        connectionName  = unicode(ui.lineConnectionName.text())
        # Updating a profile
        if self.lastEditedData:
            # If profile name has been changed, delete profile first
            if not self.lastEditedData["name"] == connectionName:
                self.iface.deleteConnection(self.lastEditedPackage, self.lastEditedData["name"])
                needsListUpdate = True
        self.iface.updateConnection(self.lastEditedPackage, connectionName, self.collectDataFromUI())
        if needsListUpdate:
            self.fillProfileList()
        if self.lastEditedData["state"].startswith("up"):
            self.iface.reconnect(self.lastEditedPackage, connectionName)
        self.hideEditBox()

    def collectDataFromUI(self):
        ui = self.ui
        data = {}

        # Default options
        data["name"] = ui.lineConnectionName.text()
        data["device_id"] = ui.deviceList.currentText()

        # Network options
        data["net_mode"] = "auto"
        data["net_address"] = ""
        data["net_mask"] = ""
        data["net_gateway"] = ""
        if ui.useManual.isChecked():
            data["net_mode"] = "manual"
        if ui.lineAddress.isEnabled():
            data["net_address"] = ui.lineAddress.text()
            data["net_mask"] = ui.lineNetworkMask.currentText()
        if ui.lineGateway.isEnabled():
            data["net_gateway"] = ui.lineGateway.text()

        # Nameservics options
        data["namemode"] = "default"
        data["nameserver"] = ""
        if ui.useAutomatic.isChecked():
            data["namemode"] = "auto"
        if ui.useCustom.isChecked():
            data["namemode"] = "custom"
            data["nameserver"] = ui.lineCustomDNS.text()

        # Let them unicode
        for i,j in data.items():
            data[i] = unicode(j)

        return data

    def editConnection(self):
        sender = self.sender().parent()
        profile, package = sender.profile, sender.package
        self.showEditBox(profile, package)

    def deleteConnection(self):
        profile = self.sender().parent().profile
        package = self.sender().parent().package
        if KMessageBox.questionYesNo(self, "Do you really want to remove profile %s ?" % profile,
                                           "Network-Manager") == KMessageBox.Yes:
            self.fillProfileList(ignore=(package, profile))
            self.iface.deleteConnection(package, profile)
        self.fillProfileList()

    def getConnectionStates(self):
        self.iface.listen(self.handler)

    def handler(self, package, signal, args):
        args = map(lambda x: unicode(x), list(args))
        if signal == "stateChanged":
            if self.widgets.has_key(args[0]):
                self.widgets[args[0]].update(args)
        print "Comar call : ", args, signal, package


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
from pardus.netutils import findInterface

# Qt Stuff
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL, Qt, QTimeLine, QSize, QVariant

# KDE Stuff
from PyKDE4.kdeui import KMessageBox
from PyKDE4.kdecore import i18n

# Application Stuff
from backend import NetworkIface
from ui import Ui_mainManager
from widgets import ConnectionItemWidget, WifiPopup, NameServerDialog

# Animation Definitions
SHOW, HIDE     = range(2)
TARGET_HEIGHT  = 0
ANIMATION_TIME = 200
DEFAULT_HEIGHT = 16777215

class MainManager(QtGui.QWidget):
    def __init__(self, parent, standAlone=True, app=None):
        QtGui.QWidget.__init__(self, parent)

        # Create the ui
        self.ui = Ui_mainManager()
        self.app = app
        self.lastEditedPackage = None
        self.lastEditedData = None

        # Network Manager can run as KControl Module or Standalone
        if standAlone:
            self.ui.setupUi(self)
            self.baseWidget = self
        else:
            self.ui.setupUi(parent)
            self.baseWidget = parent

        # Set visibility of indicators
        self.ui.workingLabel.hide()
        self.ui.refreshButton.hide()

        # Call Comar
        self.iface = NetworkIface()
        self.widgets = {}

        # Populate Packages
        self.packages = {}
        for package in self.iface.packages():
            self.packages[package] = self.iface.linkInfo(package)

        # Let look what we can do
        menu = QtGui.QMenu(self)
        for package in self.packages.keys():
            devices = self.iface.devices(package)
            if len(devices) > 0:
                # Create profile menu with current devices
                for device in devices.keys():
                    if self.packages[package]['type'] in ('net', 'wifi'):
                        menuItem = QtGui.QAction("%s - %s" % (self.packages[package]['name'], findInterface(device).name), self)
                        menuItem.setData(QVariant("%s::%s" % (package,device)))
                        self.connect(menuItem, SIGNAL("triggered()"), self.createConnection)
                        menu.addAction(menuItem)
                menu.addSeparator()
            if self.packages[package]['type'] == 'dialup':
                pppMenu = QtGui.QMenu(self.packages[package]['name'], self)
                devices = self.iface.devices(package)
                for device in devices.keys():
                    menuItem = QtGui.QAction(device, self)
                    menuItem.setData(QVariant("%s::%s" % (package,device)))
                    self.connect(menuItem, SIGNAL("triggered()"), self.createConnection)
                    pppMenu.addAction(menuItem)
                menu.addMenu(pppMenu)
                menu.addSeparator()

        ## Add package specific menu entiries
        #if "net_tools" in supportedPackages:
        #    self.ui.filterBox.addItem(i18n("Ethernet Profiles"), QVariant("net_tools"))
        #if "wireless_tools" in supportedPackages:
        #    self.ui.filterBox.addItem(i18n("Wireless Profiles"), QVariant("wireless_tools"))
        #    self.ui.filterBox.addItem(i18n("Available Profiles"), QVariant("essid"))
        #    wifiScanner = WifiPopup(self)
        #    self.ui.buttonScan.setMenu(wifiScanner)
        ## Get authentication types
        #authMods = self.iface.authMethods('wireless_tools')
        #if len(authMods):
        #    self.ui.comboSecurityTypes.addItem(i18n("No Authentication"), QVariant("none"))
        #    for name, desc in authMods:
        #        self.ui.comboSecurityTypes.addItem(desc, QVariant(name))

        if len(self.packages) > 0:
            self.ui.buttonCreate.setMenu(menu)
            self.ui.filterBox.insertItem(0, i18n("All Profiles"), QVariant("all"))
        else:
            self.ui.buttonCreate.setText(i18n("No Device Found"))
            self.ui.buttonCreate.setEnabled(False)
            self.ui.filterBox.insertItem(0, i18n("No Device Found"))
            self.ui.filterBox.setEnabled(False)
        self.ui.filterBox.setCurrentIndex(0)

        # Fill the list
        self.fillProfileList()

        # Preparing for animation
        self.ui.editBox.setMaximumHeight(TARGET_HEIGHT)
        self.lastAnimation = SHOW

        # Naruto
        self.animator = QTimeLine(ANIMATION_TIME, self)

        # Animator connections, Naruto loves Sakura-chan
        self.connect(self.animator, SIGNAL("frameChanged(int)"), self.animate)
        self.connect(self.animator, SIGNAL("finished()"), self.animateFinished)

        # Hide editBox when clicked Cancel*
        self.connect(self.ui.buttonCancel, SIGNAL("clicked()"), self.hideEditBox)
        self.connect(self.ui.buttonCancelMini, SIGNAL("clicked()"), self.hideEditBox)

        # Save changes when clicked Apply
        self.connect(self.ui.buttonApply, SIGNAL("clicked()"), self.applyChanges)

        # Show NameServer Settings Dialog
        self.nameServerDialog = NameServerDialog(self)
        self.connect(self.ui.buttonNameServer, SIGNAL("clicked()"), self.nameServerDialog.run)

        # Filter
        self.connect(self.ui.filterBox, SIGNAL("currentIndexChanged(int)"), self.filterList)

        # Refresh button for scanning remote again..
        self.connect(self.ui.refreshButton, SIGNAL("leftClickedUrl()"), self.filterList)

        # Update service status and follow Comar for sate changes
        self.getConnectionStates()

    def filterList(self, id=-1):
        if id < 0:
            filter = "essid"
        else:
            filter = str(self.ui.filterBox.itemData(id).toString())

        def filterByScan(*args):
            # We have finished the scanning let set widgets to old states
            self.ui.profileList.setEnabled(True)
            self.ui.refreshButton.show()
            self.ui.workingLabel.hide()
            self.setCursor(Qt.ArrowCursor)

            # Update the GUI
            self.app.processEvents()

            # Update List with found remote networks
            availableNetworks = {}
            for result in args[2][0]:
                availableNetworks[unicode(result['remote'])] = int(result['quality'])
            for widget in self.widgets.values():
                if widget.item.isHidden():
                    continue
                print widget.profile, widget.data["remote"], availableNetworks
                if unicode(widget.data["remote"]) in availableNetworks.keys():
                    widget.setSignalStrength(availableNetworks[unicode(widget.data["remote"])])
                    widget.item.setHidden(False)
                else:
                    widget.hideSignalStrength()
                    widget.item.setHidden(True)

        def setHidden(package=None, hidden=False, attr="package"):
            for widget in self.widgets.values():
                widget.hideSignalStrength()
                if not package:
                    widget.item.setHidden(False)
                    continue
                if attr == "essid" and not widget.package == 'wireless_tools':
                    widget.item.setHidden(True)
                    continue
                elif attr == "essid" and widget.package == 'wireless_tools':
                    if not widget.data.has_key("remote"):
                        widget.item.setHidden(True)
                    continue
                if getattr(widget, attr) == package:
                    widget.item.setHidden(hidden)
                else:
                    widget.item.setHidden(not hidden)

        # Set visibility of indicators
        self.ui.workingLabel.hide()
        self.ui.refreshButton.hide()
        # All profiles
        if filter == "all":
            setHidden()
        # Avaliable profiles
        elif filter == "essid":
            # We need to show user, we are working :)
            self.ui.profileList.setEnabled(False)
            self.ui.refreshButton.hide()
            self.ui.workingLabel.show()
            self.setCursor(Qt.WaitCursor)

            # Show all profiles
            setHidden()

            # Hide not usable ones
            setHidden("wireless_tools", False, "essid")

            # Update the GUI
            self.app.processEvents()

            # Scan for availableNetworks
            devices = self.iface.devices("wireless_tools")
            for device in devices.keys():
                self.app.processEvents()
                self.iface.scanRemote(device, "wireless_tools", filterByScan)
        else:
            # Filter by given package
            setHidden(filter, False)

    def fillProfileList(self, ignore = None):
        # Clear the entire list
        self.ui.profileList.clear()
        self.widgets = {}

        # Fill the list with current connections
        for package in self.packages.keys():
            # Fill profile list
            self.connections = self.iface.connections(package)
            self.connections.sort()
            for connection in self.connections:
                if ignore:
                    if package == ignore[0] and connection == ignore[1]:
                        continue
                info = self.iface.info(package, connection)
                state = str(info["state"])
                item = QtGui.QListWidgetItem(self.ui.profileList)
                item.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                item.setSizeHint(QSize(48,48))
                self.widgets[connection] = ConnectionItemWidget(package, connection, info, self, item)
                self.widgets[connection].updateData(state)
                self.ui.profileList.setItemWidget(item, self.widgets[connection])
                del item

        # Filter list with selected filter method
        self.filterList(self.ui.filterBox.currentIndex())

    # Anime Naruto depends on GUI
    def animate(self, height):
        self.ui.editBox.setMaximumHeight(height)
        self.ui.profileList.setMaximumHeight(self.baseWidget.height()-height)
        self.update()

    def animateFinished(self):
        if self.lastAnimation == SHOW:
            self.ui.lineConnectionName.setFocus()
            self.ui.editBox.setMaximumHeight(DEFAULT_HEIGHT)
            self.ui.profileList.setMaximumHeight(TARGET_HEIGHT)
            self.ui.editBox.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.ui.buttonCreate.setEnabled(False)
            self.ui.filterBox.setEnabled(False)
        elif self.lastAnimation == HIDE:
            self.ui.profileList.setFocus()
            self.ui.profileList.setMaximumHeight(DEFAULT_HEIGHT)
            self.ui.editBox.setMaximumHeight(TARGET_HEIGHT)
            self.ui.profileList.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.ui.buttonCreate.setEnabled(True)
            self.ui.filterBox.setEnabled(True)

    def hideEditBox(self):
        if self.lastAnimation == SHOW:
            self.lastAnimation = HIDE
            self.hideScrollBars()
            self.animator.setFrameRange(self.ui.editBox.height(), TARGET_HEIGHT)
            self.animator.start()
            self.resetForm()

    def showEditBox(self, package=None, profile=None):
        sender = self.sender().parent()
        self.lastAnimation = SHOW
        self.hideScrollBars()

        info = self.iface.capabilities(package)

        # Hide all settings first
        self.ui.groupRemote.hide()
        self.ui.groupNetwork.hide()
        self.ui.groupNameServer.hide()

        modes = info["modes"].split(",")

        if "auth" in modes:
            self.ui.comboSecurityTypes.clear()
            self.ui.comboSecurityTypes.addItem(i18n("No Authentication"), QVariant("none"))
            for name, desc in self.iface.authMethods(package):
                self.ui.comboSecurityTypes.addItem(desc, QVariant(name))
        else:
            self.ui.labelSecurity.hide()
            self.ui.comboSecurityTypes.hide()
            self.ui.labelKey.hide()
            self.ui.lineKey.hide()
            self.ui.checkShowPassword.hide()

        if profile:
            self.buildEditBoxFor(sender.package, sender.profile)

        # Then show them by giving package
        if "net" in modes:
            self.ui.groupNetwork.show()
            self.ui.groupNameServer.show()
        if "remote" in modes:
            remote_name = self.iface.remoteName(package)
            self.ui.labelRemote.setText("%s :" % remote_name)
            if "remote_scan" in modes:
                wifiScanner = WifiPopup(self)
                self.ui.buttonScan.setMenu(wifiScanner)
                self.ui.buttonScan.show()
            else:
                self.ui.buttonScan.hide()
            self.ui.groupRemote.show()
        if "device" in modes:
            self.fillDeviceList(package)

        self.animator.setFrameRange(TARGET_HEIGHT, self.baseWidget.height() - TARGET_HEIGHT)
        self.animator.start()

    def hideScrollBars(self):
        self.ui.editBox.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.profileList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def fillDeviceList(self, package):
        ui = self.ui
        devices = self.iface.devices(package)
        # print devices
        for device in devices:
            ui.deviceList.addItem(device)
        if len(devices) == 1:
            ui.deviceList.hide()
            ui.labelDeviceDescription.show()
            ui.labelDeviceDescription.setText(devices[device])
        else:
            ui.deviceList.show()
            ui.labelDeviceDescription.hide()

    # Comar operations calls gui
    def buildEditBoxFor(self, package, profile):
        ui = self.ui
        self.lastEditedPackage = package
        self.lastEditedData = data = self.iface.info(package, profile)

        ui.lineConnectionName.setText(data["name"])

        if "device_id" in data:
            ui.labelDeviceDescription.setText(data["device_name"])
        if "device_name" in data:
            ui.deviceList.setCurrentIndex(ui.deviceList.findText(data["device_id"]))

        if "remote" in data:
            ui.lineRemote.setText(data["remote"])

        authType = self.iface.authType(package, profile)
        authInfo = self.iface.authInfo(package, profile)
        ui.comboSecurityTypes.setCurrentIndex(ui.comboSecurityTypes.findData(QVariant(authType)))

        if len(authInfo) == 1:
            password = authInfo.values()[0]
            ui.lineKey.setText(password)
        else:
            # FIXME: More than one authentication parameter not supported yet!
            pass

        if data.has_key("net_mode"):
            if data["net_mode"] == "auto":
                ui.useDHCP.setChecked(True)
                if data.has_key("net_address"):
                    ui.useCustomAddress.setChecked(True)
                if data.has_key("net_gateway"):
                    ui.useCustomDNS.setChecked(True)
            else:
                ui.useManual.setChecked(True)

        if data.has_key("net_address"):
            ui.lineAddress.setText(data["net_address"])
        if data.has_key("net_mask"):
            ui.lineNetworkMask.lineEdit().setText(data["net_mask"])
        if data.has_key("net_gateway"):
            ui.lineGateway.setText(data["net_gateway"])

        if data.has_key("name_mode"):
            if data["name_mode"] == "default":
                ui.useDefault.setChecked(True)
            if data["name_mode"] == "auto":
                ui.useAutomatic.setChecked(True)
            if data["name_mode"] == "custom":
                ui.useCustom.setChecked(True)
                ui.lineCustomDNS.setText(data["name_server"])

    def resetForm(self):
        ui = self.ui
        ui.lineConnectionName.setText("")
        ui.deviceList.clear()
        ui.labelDeviceDescription.setText("")
        ui.useDHCP.setChecked(True)
        ui.useCustomAddress.setChecked(False)
        ui.useCustomDNS.setChecked(False)
        ui.useManual.setChecked(False)
        ui.lineAddress.setText("")
        ui.lineNetworkMask.lineEdit().setText("")
        ui.lineGateway.setText("")
        ui.lineRemote.setText("")
        ui.useDefault.setChecked(True)
        ui.useAutomatic.setChecked(False)
        ui.useCustom.setChecked(False)
        ui.lineCustomDNS.setText("")
        ui.lineKey.setText("")
        ui.comboSecurityTypes.setCurrentIndex(0)
        self.lastEditedData = None
        self.lastEditedPackage = None

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
        if self.lastEditedData:
            if self.lastEditedData.has_key("state"):
                if self.lastEditedData["state"].startswith("up"):
                    self.iface.connect(self.lastEditedPackage, connectionName)
        else:
            needsListUpdate = True
        if needsListUpdate:
            self.fillProfileList()
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

        # Nameservice options
        data["name_mode"] = "default"
        data["name_server"] = ""
        if ui.useAutomatic.isChecked():
            data["name_mode"] = "auto"
        if ui.useCustom.isChecked():
            data["name_mode"] = "custom"
            data["name_server"] = ui.lineCustomDNS.text()

        # Remote and security options
        if ui.groupRemote.isVisible():

            # Remote
            data["remote"] = ui.lineRemote.text()
            data["apmac"]  = ""

            # Security
            data["auth"] = str(ui.comboSecurityTypes.itemData(ui.comboSecurityTypes.currentIndex()).toString())
            data["auth_password"] = ui.lineKey.text()

        # Let them unicode
        for i,j in data.items():
            data[i] = unicode(j)

        return data

    def createConnection(self):
        package, device = str(self.sender().data().toString()).split('::')
        # print package, device
        self.resetForm()
        self.lastEditedPackage = package
        self.showEditBox(package)

    def editConnection(self):
        sender = self.sender().parent()
        profile, package = sender.profile, sender.package
        self.showEditBox(package, profile)

    def deleteConnection(self):
        profile = self.sender().parent().profile
        package = self.sender().parent().package
        if KMessageBox.questionYesNo(self, i18n("Do you really want to remove profile %s ?" % profile),
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
                self.widgets[args[0]].updateData(args)
        print "Comar call : ", args, signal, package


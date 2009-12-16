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
from PyKDE4.kdeui import KIcon, KUrlLabel, KMessageBox, KPasswordDialog
from PyKDE4.kdecore import i18n

# Application Stuff
from networkmanager.ui_ap           import Ui_APItemWidget
from networkmanager.ui_main         import Ui_mainManager
from networkmanager.ui_item         import Ui_ConnectionItemWidget
from networkmanager.ui_security     import Ui_DialogSecurity
from networkmanager.ui_nameserver   import Ui_nameServer
from networkmanager.ui_securityitem import Ui_SecurityWidget
from networkmanager.ui_nmwizard     import Ui_NMWizard

# FIXME: The ideal is to have the icon names from the backends
def getIconForPackage(package):

    d = {
            "net_tools": "network-wired",
            "wireless_tools": "network-wireless",
            "ModemManager": "modem",
            "ppp": "modem",
        }

    return d.get(package, "modem")

class SecurityWidget(QtGui.QWidget):
    def __init__(self, parent, key, label, type_):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_SecurityWidget()
        self.ui.setupUi(self)

        self.key = key
        if type_ == "pass":
            self.ui.lineFieldValue.setEchoMode(QtGui.QLineEdit.Password)
        if type_ != "file":
            self.ui.pushBrowse.hide()

        self.ui.labelFieldName.setText(unicode(label))

    def setValue(self, value):
        self.ui.lineFieldValue.setText(unicode(value))

    def getValue(self):
        return unicode(self.ui.lineFieldValue.text())


class PINDialog(KPasswordDialog):
    def __init__(self, parent, deviceName, maxTries=3, showKeepPassword=True):
        if showKeepPassword:
            flags = KPasswordDialog.ShowKeepPassword
        else:
            flags = KPasswordDialog.NoFlags

        KPasswordDialog.__init__(self, parent, flags)

        # Set UI
        self.setCaption(i18n("Enter PIN"))
        self.setPrompt("%s <b>%s</b>" % (i18n("Please Enter PIN Code for"), deviceName))
        self.setPixmap(KIcon("preferences-desktop-notification").pixmap(64))

        self.maxTries = maxTries


class ConnectionWizard(QtGui.QDialog):
    def __init__(self, parent, package, deviceID, deviceName):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_NMWizard()
        self.ui.setupUi(self)

        self.isAvailable = False

        self.iface = parent.iface
        self.package = package
        self.device = deviceID
        self.pin = ""

        self.ui.txtDevice.setText(deviceName)
        self.ui.txtIMEI.setText(deviceID.split(":")[-1])

        # Create PIN Dialog
        self.pinDialog = PINDialog(self, deviceName)

        # Signals & Slots
        self.connect(self.ui.buttonBox, SIGNAL("accepted()"), self.applyChanges)
        self.connect(self.ui.buttonBox, SIGNAL("rejected()"), self.reject)
        self.connect(self.ui.lineEditPIN, SIGNAL("editingFinished()"), self.savePIN)

        # Ask for pin and scan if OK
        self.isAvailable = self.askForPIN()

    def savePIN(self):
        self.pin = str(self.ui.lineEditPIN.text())

    def applyChanges(self):
        def collectDataFromUI():
            data = {}

            data["device_id"] = self.device
            data["name"] = self.connectionName
            data["auth"] = "pin"

            if self.pin:
                print "******** %s" % self.pin
                data["auth_pin"] = self.pin

            print data
            return data

        self.connectionName = str(self.ui.comboBoxOperators.itemData(self.ui.comboBoxOperators.currentIndex()).toString())

        try:
            self.iface.updateConnection(self.package, self.connectionName, collectDataFromUI())
            self.accept()
        except Exception, e:
            KMessageBox.error(self, unicode(e))
            return

    def show(self):
        if self.isAvailable:
            self.scan(self.package, self.device)
            return self.exec_()

    def askForPIN(self):
        if "pin" in self.iface.capabilities(self.package)["modes"] and self.iface.requiresPIN(self.package, self.device):
            # Loop 3 times by default
            for c in range(self.pinDialog.maxTries):
                # Clear textbox
                self.pinDialog.setPassword("")
                if self.pinDialog.exec_():
                    # Clicked OK
                    pin = self.pinDialog.password()

                    # Send PIN to the card, returns True if PIN is valid.
                    if self.iface.sendPIN(self.package, self.device, str(pin)):
                        self.pin = str(pin)
                        self.ui.lineEditPIN.setText(self.pin)
                        return True
                else:
                    break

            # Verification failed for 3 times
            if c == self.pinDialog.maxTries-1:
                KMessageBox.error(self, i18n("You've typed the wrong PIN code for 3 times"))
                return False
            else:
                # Canceled
                return True

        else:
            # PIN is already entered or the backend doesn't support PIN operations
            return True


    def scan(self, package, deviceID):
        def scan_handler(*args):
            if args[2][0]:
                self.ui.progressBar.hide()
                self.ui.comboBoxOperators.setEnabled(True)
                self.ui.lineEditPIN.setEnabled(True)

                for p in args[2][0]:
                    oplong, opshort, status = p['remote'].split(",")
                    self.ui.comboBoxOperators.addItem(oplong, QVariant(opshort))
                    if status < 3:
                        # Operator is available
                        self.ui.comboBoxOperators.setCurrentItem(oplong)

        # Asynchronously scan for operators
        self.iface.scanRemote(deviceID, package, func=scan_handler)


class SecurityDialog(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_DialogSecurity()
        self.ui.setupUi(self)

        self.layout = QtGui.QVBoxLayout(self.ui.frameFields)
        self.widgets = {}

        self.connect(self.ui.buttonBox, SIGNAL("accepted()"), self.accept)
        self.connect(self.ui.buttonBox, SIGNAL("rejected()"), self.reject)

    def setFields(self, fields=[]):
        for key, widget in self.widgets.iteritems():
            self.layout.removeWidget(widget)
            widget.hide()
        self.widgets = {}
        for key, label, _type in fields:
            widget = SecurityWidget(self.ui.frameFields, key, label, _type)
            self.layout.addWidget(widget)
            self.widgets[key] = widget

    def setValues(self, values={}):
        for key, value in values.iteritems():
            if key in self.widgets:
                self.widgets[key].setValue(value)

    def getValues(self):
        values = {}
        for key, widget in self.widgets.iteritems():
            values[key] = widget.getValue()
        return values

class NameServerDialog(QtGui.QDialog):

    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_nameServer()
        self.ui.setupUi(self)

        self.connect(self.ui.buttonBox, SIGNAL("accepted()"), self.accept)
        self.connect(self.ui.buttonBox, SIGNAL("rejected()"), self.reject)

    def setNameservers(self, servers=[]):
        self.ui.listBox.clear()
        for server in servers:
            self.ui.listBox.insertItem(unicode(server))

    def setHostname(self, hostname):
        self.ui.lineMachineName.setText(unicode(hostname))

    def getHostname(self):
        return unicode(self.ui.lineMachineName.text())

    def getNameservers(self):
        servers = []
        for item in self.ui.listBox.items():
            servers.append(unicode(item))
        return servers

class APItemWidget(QtGui.QWidget):

    def __init__(self, data, parent, item):
        QtGui.QWidget.__init__(self, parent)

        self.ui = Ui_APItemWidget()
        self.ui.setupUi(self)
        self.item = item
        self.data = data
        self.ui.labelName.setText(data['remote'])
        self.setToolTip("%s - %s" % (data['encryption'], data['mac']))
        self.ui.signalStrength.setValue(int(data['quality']))
        icon = "document-encrypt"
        if data['encryption'] == 'none':
            icon = "document-decrypt"
        self.ui.labelStatus.setPixmap(KIcon(icon).pixmap(22))

class APPopup(QtGui.QMenu):
    def __init__(self, parent, package):
        QtGui.QMenu.__init__(self, parent)
        self.parent = parent
        self.iface  = parent.iface
        self.package= package

        # Layout & Widgets
        self.gridLayout = QtGui.QGridLayout(self)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.listWidget = QtGui.QListWidget(self)
        self.listWidget.setMinimumSize(QSize(280, 160))
        self.gridLayout.addWidget(self.listWidget, 0, 0, 1, 1)
        self.refreshButton = QtGui.QPushButton(self)
        self.refreshButton.setText(i18n("Refresh"))
        self.gridLayout.addWidget(self.refreshButton, 1, 0, 1, 1)

        # Connections
        self.connect(self, SIGNAL("aboutToShow()"), self.rescan)
        self.connect(self.refreshButton, SIGNAL("clicked()"), self.rescan)
        self.connect(self.listWidget, SIGNAL("itemClicked(QListWidgetItem*)"), self.useSelected)
        self.refreshButton.hide()

    def useSelected(self, item):
        self.hide()
        data = self.listWidget.itemWidget(item).data
        self.parent.ui.lineRemote.setText(data['remote'])
        self.parent.ui.comboSecurityTypes.setCurrentIndex(self.parent.ui.comboSecurityTypes.findData(QVariant(data['encryption'])))

    def fillList(self, package, exception, args):
        if not exception:
            self.refreshButton.show()
            self.listWidget.clear()
            for remote in args[0]:
                item = QtGui.QListWidgetItem(self.listWidget)
                item.setSizeHint(QSize(22,30))
                ap = APItemWidget(remote, self, item)
                self.listWidget.setItemWidget(item, ap)
        else:
            print exception

    def rescan(self):
        self.listWidget.clear()
        self.refreshButton.hide()

        # Show notification
        self.listWidget.addItem(i18n("Scanning..."))
        self.listWidget.item(0).setFlags(Qt.NoItemFlags)

        # Scan with current device
        device = str(self.parent.ui.deviceList.currentText())
        self.iface.scanRemote(device, self.package, self.fillList)

class ConnectionItemWidget(QtGui.QWidget):

    def __init__(self, package, profile, data, parent, item):
        QtGui.QWidget.__init__(self, parent)

        self.ui = Ui_ConnectionItemWidget()
        self.ui.setupUi(self)
        self.ui.signalStrength.hide()

        self.ui.labelName.setText(profile)

        # Class members
        self.iface = parent.iface
        self.item = item
        self.package = package
        self.profile = profile
        self.desc = None
        self.data = data

        # Get backend capabilities
        self.capabilities = self.iface.capabilities(self.package)["modes"]

        # Check if package supports PIN operations
        self.supportsPIN = "pin" in self.capabilities
        print "** Profile %s supports PIN: %s" % (profile, str(self.supportsPIN))

        # Connect signals for edit and delete
        self.connect(self.ui.buttonEdit, SIGNAL("clicked()"), parent.editConnection)
        self.connect(self.ui.buttonDelete, SIGNAL("clicked()"), parent.deleteConnection)

        # Hide editButton for "wizard" like backends
        if "wizard" in self.capabilities:
            self.ui.buttonEdit.hide()

        # Toggle functionality depends on PIN support for some devices
        self.connect(self.ui.checkToggler, SIGNAL("clicked()"), self.toggleConnection)

    def setSignalStrength(self, value):
        self.ui.signalStrength.setValue(value)
        self.ui.signalStrength.show()

    def hideSignalStrength(self):
        self.ui.signalStrength.hide()

    def mouseDoubleClickEvent(self, event):
        self.ui.buttonEdit.animateClick(100)

    def updateData(self, data):
        if type(data) == list:
            if len(data) == 2:
                name, state = data
                detail = ''
            elif len(data) == 3:
                name, state, detail = data
        elif type(data) == str:
            splitted = data.split(' ',1)
            state = splitted[0]
            detail = ""
            if len(splitted) > 1:
                detail = splitted[1]
        if state == "down":
            self.ui.labelDesc.setText(i18n("Disconnected"))
            self.ui.checkToggler.setChecked(False)
            self.ui.labelStatus.setPixmap(KIcon(getIconForPackage(self.package)).pixmap(32))
            self.setState(True)
        elif state == "up":
            self.ui.labelDesc.setText(unicode(i18n("Connected: %s")) % detail)
            self.ui.checkToggler.setChecked(True)
            self.ui.labelStatus.setPixmap(KIcon("dialog-ok-apply").pixmap(32))
            self.setState(True)
        elif state == "connecting":
            self.ui.labelDesc.setText(i18n("Connecting"))
            self.ui.labelStatus.setPixmap(KIcon("chronometer").pixmap(32))
            self.setState(True)
        elif state == "inaccessible":
            self.ui.labelDesc.setText(unicode(detail))
            self.ui.labelStatus.setPixmap(KIcon("emblem-important").pixmap(32))
            self.setState(True)
        elif state == "unplugged":
            self.ui.labelDesc.setText(i18n("Cable or device is unplugged"))
            self.ui.labelStatus.setPixmap(KIcon("dialog-warning").pixmap(32))
            self.setState(False)

    def setState(self, state):
        pass

    def toggleConnection(self):
        def handler(package, exception, args):
            if exception:
                if self.ui.checkToggler.isChecked():
                    self.ui.checkToggler.setChecked(False)
                else:
                    self.ui.checkToggler.setChecked(True)
                if "Comar.PolicyKit" in exception._dbus_error_name:
                    KMessageBox.error(self, i18n("Access denied"))
                else:
                    KMessageBox.error(self, unicode(exception))

        if self.supportsPIN:
            # We may need to set PIN before any toggling action
            pass

        if self.ui.checkToggler.isChecked():
            self.iface.connect(self.package, self.profile, handler=handler)
        else:
            self.iface.disconnect(self.package, self.profile, handler=handler)


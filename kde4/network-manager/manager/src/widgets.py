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
from PyKDE4.kdeui import KIcon, KUrlLabel, KMessageBox
from PyKDE4.kdecore import i18n

# Application Stuff
from ui import Ui_mainManager
from uiitem import Ui_ConnectionItemWidget
from uiwifiitem import Ui_WifiItemWidget
from uinameserver import Ui_nameServer
from uisecurity import Ui_DialogSecurity
from uisecurityitem import Ui_SecurityWidget

iconForPackage = {
    "net_tools": "network-wired",
    "wireless_tools": "network-wireless",
    "ppp": "modem",
}

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

class WifiItemWidget(QtGui.QWidget):

    def __init__(self, data, parent, item):
        QtGui.QWidget.__init__(self, parent)

        self.ui = Ui_WifiItemWidget()
        self.ui.setupUi(self)
        self.item = item
        self.data = data
        self.ui.labelName.setText(data['remote'])
        self.setToolTip("%s - %s" % (data['encryption'], data['mac']))
        self.ui.wifiStrength.setValue(int(data['quality']))
        icon = "document-encrypt"
        if data['encryption'] == 'none':
            icon = "document-decrypt"
        self.ui.labelStatus.setPixmap(KIcon(icon).pixmap(22))

class WifiPopup(QtGui.QMenu):
    def __init__(self, parent):
        QtGui.QMenu.__init__(self, parent)
        self.parent = parent
        self.iface  = parent.iface

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

    def fillList(self, *args):
        self.refreshButton.show()
        self.listWidget.clear()
        for remote in args[2][0]:
            item = QtGui.QListWidgetItem(self.listWidget)
            item.setSizeHint(QSize(22,30))
            wifi = WifiItemWidget(remote, self, item)
            self.listWidget.setItemWidget(item, wifi)

    def rescan(self):
        self.listWidget.clear()
        self.refreshButton.hide()

        # Show notification
        self.listWidget.addItem(i18n("Scanning..."))
        self.listWidget.item(0).setFlags(Qt.NoItemFlags)

        # Scan with current device
        device = str(self.parent.ui.deviceList.currentText())
        self.iface.scanRemote(device, "wireless_tools", self.fillList)

class ConnectionItemWidget(QtGui.QWidget):

    def __init__(self, package, profile, data, parent, item):
        QtGui.QWidget.__init__(self, parent)

        self.ui = Ui_ConnectionItemWidget()
        self.ui.setupUi(self)
        self.ui.wifiStrength.hide()

        self.ui.labelName.setText(profile)

        self.iface = parent.iface
        self.item = item
        self.package = package
        self.profile = profile
        self.desc = None
        self.data = data

        self.connect(self.ui.buttonEdit,   SIGNAL("clicked()"), parent.editConnection)
        self.connect(self.ui.buttonDelete, SIGNAL("clicked()"), parent.deleteConnection)
        self.connect(self.ui.checkToggler, SIGNAL("clicked()"), self.toggleConnection)

    def setSignalStrength(self, value):
        self.ui.wifiStrength.setValue(value)
        self.ui.wifiStrength.show()

    def hideSignalStrength(self):
        self.ui.wifiStrength.hide()

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
            self.ui.labelStatus.setPixmap(KIcon(iconForPackage[self.package]).pixmap(32))
        elif state == "up":
            self.ui.labelDesc.setText(unicode(i18n("Connected: %s")) % detail)
            self.ui.checkToggler.setChecked(True)
            self.ui.labelStatus.setPixmap(KIcon("games-endturn").pixmap(32))
        elif state == "connecting":
            self.ui.labelDesc.setText(i18n("Connecting"))
            self.ui.labelStatus.setPixmap(KIcon("chronometer").pixmap(32))
        elif state == "inaccessible":
            self.ui.labelDesc.setText(unicode(detail))
            self.ui.labelStatus.setPixmap(KIcon("emblem-important").pixmap(32))
        elif state == "unplugged":
            self.ui.labelDesc.setText(i18n("Cable or device is unplugged."))
            self.ui.labelStatus.setPixmap(KIcon("dialog-warning").pixmap(32))

    def toggleConnection(self):
        def handler(package, exception, args):
            if exception:
                if self.ui.checkToggler.isChecked():
                    self.ui.checkToggler.setChecked(False)
                else:
                    self.ui.checkToggler.setChecked(True)
                print exception._dbus_error_name
                if "Comar.PolicyKit" in exception._dbus_error_name:
                    KMessageBox.error(self, i18n("Access denied."))
                else:
                    KMessageBox.error(self, unicode(exception))

        if self.ui.checkToggler.isChecked():
            self.iface.connect(self.package, self.profile, handler=handler)
        else:
            self.iface.disconnect(self.package, self.profile, handler=handler)


#!/usr/bin/python
# -*- coding: utf-8 -*-

# QT Libs
from PyQt4.QtGui import QWidget, QFrame, QGraphicsLinearLayout, QPixmap

# Custom Widgets
from popupui import Ui_Connection
from item import ConnectionItem

class Popup(QWidget):

    def __init__(self, parent, applet):
        QWidget.__init__(self, parent)

        self.ui = Ui_Connection()
        self.ui.setupUi(parent)
        self.parent = parent
        self.iface = applet.iface
        self.connections = {"net_tools":{}, "wireless_tools":{}}
        self.init()

    def init(self):
        for package in self.connections.keys():
            connections = self.iface.connections(package)
            for connection in connections:
                self.addConnectionItem(package, str(connection))
                info = self.iface.info(package, connection)
                self.connections[package][connection].setState(str(info['state']))

    def setConnectionStatus(self, package, message):
        if package == "wireless_tools":
            self.ui.wirelessStatus.setText(message)
        elif package == "net_tools":
            self.ui.ethernetStatus.setText(message)

    def addConnectionItem(self, package, name):
        if package == "wireless_tools":
            item = ConnectionItem(self.ui.wirelessConnections, package, name, self)
            self.ui.wirelessLayout.addWidget(item)
        elif package == "net_tools":
            item = ConnectionItem(self.ui.ethernetConnections, package, name, self)
            self.ui.ethernetLayout.addWidget(item)
        self.connections[package][name] = item



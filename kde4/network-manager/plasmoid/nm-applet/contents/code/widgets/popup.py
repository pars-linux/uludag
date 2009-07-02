#!/usr/bin/python
# -*- coding: utf-8 -*-

# QT Libs
from PyQt4.QtGui import QWidget, QFrame, QGraphicsLinearLayout, QPixmap
from PyQt4.QtCore import Qt, QTimer, SIGNAL, QString

# Plasma Libs
from PyKDE4.plasma import Plasma

# Custom Widgets
from popupui import Ui_Connection
from item import ConnectionItem

class NmIcon(Plasma.IconWidget):
    def __init__(self, parent):
        Plasma.IconWidget.__init__(self)

class Blinker:
    def __init__(self, parent, color=Qt.green):
        self.parent = parent
        self.timer = QTimer(parent)
        self.parent.connect(self.timer, SIGNAL("timeout()"), self.blink)
        self.defaultColor = self.color = color
        self.transfer = 0

    def blink(self):
        if self.color == self.defaultColor:
            self.color = Qt.transparent
        else:
            self.color = self.defaultColor
        self.parent.update()

    def update(self, data):
        if not data == self.transfer:
            self.timer.start(100)
        else:
            self.stop()
        self.transfer = data

    def isActive(self):
        return self.timer.isActive()

    def stop(self):
        self.timer.stop()
        self.color = Qt.transparent
        self.parent.update()

class Popup(QWidget):

    def __init__(self, parent, applet):
        QWidget.__init__(self, parent)

        self.ui = Ui_Connection()
        self.ui.setupUi(parent)
        self.parent = parent
        self.iface = applet.iface
        self.applet = applet
        self.connections = {"net_tools":{}, "wireless_tools":{}}

    def init(self):
        hasProfile = False
        for package in self.connections.keys():
            connections = self.iface.connections(package)
            for connection in connections:
                hasProfile = True
                self.addConnectionItem(package, str(connection))
                info = self.iface.info(package, connection)
                if str(info['state']).startswith('up'):
                    # Sometimes COMAR doesnt send ip with up state, we need to fix it
                    try:
                        ip = str(info['state'].split()[1])
                    except IndexError:
                        ip = 'N/A'
                    self.applet.handler(package, 'stateChanged', [connection, 'up', ip])
                else:
                    self.connections[package][connection].setState(str(info['state']))

        self.ui.nmButton.setHidden(hasProfile)
        self.ui.noProfile.setHidden(hasProfile)
        self.ui.warning.setHidden(hasProfile)
        if not hasProfile:
            self.parent.setMaximumHeight(100)

        for package in self.connections.keys():
            if len(self.connections[package]) == 0:
                getattr(self.ui,package).hide()

    def setConnectionStatus(self, package, message):
        if package == "wireless_tools":
            self.ui.wirelessStatus.setText(message)
        elif package == "net_tools":
            self.ui.ethernetStatus.setText(message)

    def addConnectionItem(self, package, name):
        name = unicode(name)
        if package == "wireless_tools":
            item = ConnectionItem(self.ui.wirelessConnections, package, name, self)
            self.ui.wirelessLayout.addWidget(item)
        elif package == "net_tools":
            item = ConnectionItem(self.ui.ethernetConnections, package, name, self)
            self.ui.ethernetLayout.addWidget(item)
        self.connections[package][name] = item


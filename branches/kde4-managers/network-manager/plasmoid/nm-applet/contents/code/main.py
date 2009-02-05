#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pardus Libs
import comar

# Qt Libs
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# KDE Libs
from PyKDE4.kdecore import *
from PyKDE4.kdeui import *

# Plasma Libs
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript

# Popup Widget
from popup import *
from item import *

# DBUS-QT
from dbus.mainloop.qt import DBusQtMainLoop

# DBUS MainLoop
DBusQtMainLoop(set_as_default = True)

# Our Comar Link
link = comar.Link()

class ConnectionItem(QWidget):

    def __init__(self, parent, package, name, dialog):
        QWidget.__init__(self, parent)
        self.ui = Ui_connectionItem()
        self.ui.setupUi(self)
        self.ui.connectionSignal.hide()
        self.dialog = dialog
        self.name = name
        self.package = package
        self.setText(name)
        self.setState(False)

    def enterEvent(self, event):
        self.ui.frame.setFrameShadow(QFrame.Raised)

    def leaveEvent(self, event):
        self.ui.frame.setFrameShadow(QFrame.Plain)

    def mousePressEvent(self, event):
        if self.lastState == "down":
            link.Net.Link[self.package].setState(self.name,"up")
        else:
            link.Net.Link[self.package].setState(self.name,"down")
        self.dialog.hide()

    def setText(self, text):
        self.ui.connectionName.setText(text)

    def setState(self, state="down"):
        if state == "up":
            self.ui.connectionStatus.setPixmap(QPixmap(":/icons/icons/check.png"))
        elif state == "connecting":
            self.ui.connectionStatus.setPixmap(QPixmap(":/icons/icons/working.png"))
        else:
            self.ui.connectionStatus.setPixmap(
                    QPixmap(":/icons/icons/network-%s.png" % self.package))
        self.lastState = state

class Popup(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.ui = Ui_Connection()
        self.ui.setupUi(parent)
        self.parent = parent
        self.connections = {"net_tools":{}, "wireless_tools":{}}

        self.init()

    def init(self):
        for package in self.connections.keys():
            connections = list(link.Net.Link[package].connections())
            for connection in connections:
                self.addConnectionItem(package, str(connection))

        link.listenSignals("Net.Link", self.handler)

    def handler(self, package, signal, args):
        args = list(args)
        if (str(args[1]) == "up"):
            self.setConnectionStatus(package, "Connected, IP: <b>%s</b>" % args[2])
        elif (str(args[1]) == "connecting"):
            self.setConnectionStatus(package, "Connecting to <b>%s</b>" % args[0])
        else:
            self.setConnectionStatus(package, "Not connected.")
        self.connections[package][str(args[0])].setState(str(args[1]))

    def setConnectionStatus(self, package, message):
        if package == "wireless_tools":
            self.ui.wirelessStatus.setText(message)
        elif package == "net_tools":
            self.ui.ethernetStatus.setText(message)

    def addConnectionItem(self, package, name):
        if package == "wireless_tools":
            item = ConnectionItem(self.ui.wirelessConnections, package, name, self.parent)
            self.ui.wirelessLayout.addWidget(item)
        elif package == "net_tools":
            item = ConnectionItem(self.ui.ethernetConnections, package, name, self.parent)
            self.ui.ethernetLayout.addWidget(item)
        self.connections[package][name] = item

class NmApplet(plasmascript.Applet):
    """ Our main applet derived from plasmascript.Applet """

    def __init__(self, parent):
        plasmascript.Applet.__init__(self, parent)

    def init(self):
        """ Const method for initializing the applet """

        # Configuration interface support comes with plasma
        self.setHasConfigurationInterface(False)

        # Aspect ratio defined in Plasma
        self.setAspectRatioMode(Plasma.Square)

        self.icon = Plasma.IconWidget()
        self.icon.setIcon("applications-internet")
        self.icon.setToolTip("Click here to show connections..")

        self.dialog = Plasma.Dialog()
        self.dialog.setWindowFlags(Qt.Popup)

        self.popup = Popup(self.dialog)

        self.dialog.resize(self.size().toSize())
        self.dialog.adjustSize()

        self.layout = QGraphicsLinearLayout(self.applet)
        self.layout.addItem(self.icon)

        self.connect(self.icon, SIGNAL("clicked()"), self.showDialog)

    def showDialog(self):
        if self.dialog.isVisible():
            self.dialog.hide()
        else:
            self.dialog.show()
            self.dialog.move(self.popupPosition(self.dialog.sizeHint()))

    def getWifi(self):
        devices = list(link.Net.Link["wireless_tools"].deviceList())
        if len(devices) == 0:
            return (False, 'No wifi device found')
        hotspots = list(link.Net.Link["wireless_tools"].scanRemote(list(devices)[0]))
        if len(hotspots) == 0:
            return (False, 'No hotspot found')
        return (True, hotspots)

def CreateApplet(parent):
    return NmApplet(parent)

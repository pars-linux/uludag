#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pardus Libs
import comar
import dbus

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

from dbus.mainloop.qt import DBusQtMainLoop
# DBUS MainLoop
DBusQtMainLoop(set_as_default = True)

# Our Comar Link
link = comar.Link()

# Session Bus
#sessionBus = dbus.SessionBus()
lastId = -1

def notify(message, timeout=2000):
    global lastId
    try:
        notifierProxy = sessionBus.get_object('org.kde.VisualNotifications', '/VisualNotifications')
        notifierObj = dbus.Interface(notifierProxy, "org.kde.VisualNotifications")
        if lastId>0:
            notifierObj.CloseNotification(lastId)
        lastId = notifierObj.Notify("NM", 0, "", "applications-internet", "Network Manager", message, [], {}, timeout)
    except:
        pass

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

    def mouseReleaseEvent(self, event):
        self.dialog.parent.hide()
        if self.lastState == "down":
            link.Net.Link[self.package].setState(self.name,"up")
        else:
            link.Net.Link[self.package].setState(self.name,"down")

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

        self.layout = QGraphicsLinearLayout(self.applet)
        self.layout.addItem(self.icon)

        self.dialog = Plasma.Dialog()
        self.dialog.setWindowFlags(Qt.Popup)

        self.popup = Popup(self.dialog)

        self.dialog.resize(self.size().toSize())
        self.dialog.adjustSize()

        self.connect(self.icon, SIGNAL("clicked()"), self.showDialog)
        link.listenSignals("Net.Link", self.handler)

    def handler(self, package, signal, args):
        args = list(args)
        if (str(args[1]) == "up"):
            self.popup.setConnectionStatus(package, "Connected, IP: <b>%s</b>" % args[2])
            #notify("Connected to <b>%s</b>, IP: <b>%s</b>" % (args[0], args[2]))
            self.icon.setIcon("preferences-web-browser-shortcuts")
        elif (str(args[1]) == "connecting"):
            #notify("Connecting to <b>%s</b>" % args[0], 5000)
            self.popup.setConnectionStatus(package, "Connecting to <b>%s</b>" % args[0])
        else:
            self.icon.setIcon("applications-internet")
            #notify("Not connected")
            self.popup.setConnectionStatus(package, "Not connected.")
        self.popup.connections[package][str(args[0])].setState(str(args[1]))

    def showDialog(self):
        if self.dialog.isVisible():
            self.dialog.hide()
        else:
            self.dialog.show()
            self.dialog.move(self.popupPosition(self.dialog.sizeHint()))

def CreateApplet(parent):
    return NmApplet(parent)

#!/usr/bin/python
# -*- coding: utf-8 -*-

# Network Interface
from backend.pardus import NetworkIface

# Qt Libs
from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import QWidget, QFrame, QGraphicsLinearLayout, QPixmap

# Plasma Libs
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript

# Custom Widgets
from widgets.popup import Popup

# Network Interface for operations
iface = NetworkIface()

class NmApplet(plasmascript.Applet):
    """ Our main applet derived from plasmascript.Applet """

    def __init__(self, parent):
        plasmascript.Applet.__init__(self, parent)
        self.iface = iface

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
        self.updateTheme()

        self.popup = Popup(self.dialog, self)

        self.dialog.resize(self.size().toSize())
        self.dialog.adjustSize()

        self.connect(self.icon, SIGNAL("clicked()"), self.showDialog)

        # It may cause crashes in PlasmoidViewer but luckly not in Plasma :)
        self.connect(Plasma.Theme.defaultTheme(), SIGNAL("themeChanged()"), self.updateTheme)

        # Listen network status from comar
        self.iface.listen(self.handler)

    def handler(self, package, signal, args):
        args = list(args)
        if (str(args[1]) == "up"):
            self.popup.setConnectionStatus(package, "Connected, IP: <b>%s</b>" % args[2])
            self.icon.setIcon("preferences-web-browser-shortcuts")
        elif (str(args[1]) == "connecting"):
            self.popup.setConnectionStatus(package, "Connecting to <b>%s</b>" % args[0])
        else:
            self.icon.setIcon("applications-internet")
            self.popup.setConnectionStatus(package, "Not connected.")
        self.popup.connections[package][str(args[0])].setState(str(args[1]))

    def updateTheme(self):
        self.dialog.setStyleSheet("color: %s;" % Plasma.Theme.defaultTheme().color(Plasma.Theme.TextColor).name())

    def showDialog(self):
        if self.dialog.isVisible():
            self.dialog.hide()
        else:
            self.dialog.show()
            self.dialog.move(self.popupPosition(self.dialog.sizeHint()))

def CreateApplet(parent):
    return NmApplet(parent)

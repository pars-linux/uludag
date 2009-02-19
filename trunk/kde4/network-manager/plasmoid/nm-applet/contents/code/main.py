#!/usr/bin/python
# -*- coding: utf-8 -*-

# D-Bus
import dbus

# Qt Libs
from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import QWidget, QFrame, QGraphicsLinearLayout, QPixmap

# Plasma Libs
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript

# Custom Widgets
from widgets.popup import Popup

# KDE4 Notifier
from widgets.notify import Notifier

# Network Interface for operations
from backend.pardus import NetworkIface
iface = NetworkIface()

class NmApplet(plasmascript.Applet):
    """ Our main applet derived from plasmascript.Applet """

    def __init__(self, parent):
        plasmascript.Applet.__init__(self, parent)
        self.iface = iface
        self.notifyface = Notifier(dbus.get_default_main_loop())

    def init(self):
        """ Const method for initializing the applet """

        self.defaultIcon = "%s/contents/code/icons/icon.svgz" % self.package().path()

        # Aspect ratio defined in Plasma
        self.setAspectRatioMode(Plasma.ConstrainedSquare)

        self.layout = QGraphicsLinearLayout(self.applet)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.icon = Plasma.IconWidget()
        self.layout.addItem(self.icon)

        self.icon.setSvg(self.defaultIcon, "native")
        self.icon.setToolTip("Click here to show connections..")

        try:
            # new kdebindings4 and kdebase4-workspace are required.
            self.registerAsDragHandle(self.icon)
        except:
            print "Please update your kde4 packages !"

        self.connect(self.icon, SIGNAL("clicked()"), self.showDialog)

        self.dialog = Plasma.Dialog()
        self.dialog.setWindowFlags(Qt.Popup)
        self.updateTheme()

        self.popup = Popup(self.dialog, self)
        self.popup.init()

        self.dialog.resize(self.size().toSize())
        self.dialog.adjustSize()

        # It may cause crashes in PlasmoidViewer but luckly not in Plasma :)
        self.connect(Plasma.Theme.defaultTheme(), SIGNAL("themeChanged()"), self.updateTheme)

        # Listen network status from comar
        self.iface.listen(self.handler)

    def constraintsEvent(self, constraints):
        if constraints & Plasma.FormFactorConstraint:
            return

    def handler(self, package, signal, args):
        args = map(lambda x: str(x), list(args))
        ip = ''

        if (str(args[1]) == "up"):
            msg = "Connected to <b>%s</b> IP: %s" % (args[0], args[2])
            ip = args[2]
            self.popup.setConnectionStatus(package, "Connected")
            self.icon.setSvg(self.defaultIcon)
        elif (str(args[1]) == "connecting"):
            msg = "Connecting to <b>%s</b> .." % args[0]
            self.popup.setConnectionStatus(package, "Connecting..")
        else:
            msg = "Disconnected"
            self.popup.setConnectionStatus(package, msg)
            self.icon.setSvg(self.defaultIcon, "native")

        if signal == 'stateChanged':
            self.popup.connections[package][str(args[0])].setState(str(args[1]), ip)
            self.notifyface.notify(str(msg))

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

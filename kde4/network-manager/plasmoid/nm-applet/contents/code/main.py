#!/usr/bin/python
# -*- coding: utf-8 -*-

# OS
import os
import time

# D-Bus
import dbus

# Qt Libs
from PyQt4.QtCore import Qt, SIGNAL, SLOT, pyqtSignature, QString, QTimer, QRectF, QTimer
from PyQt4.QtGui import QWidget, QFrame, QGraphicsLinearLayout, QPixmap, QColor, QPainterPath, QPainter, QIcon

# KDE Libs
from PyKDE4.kdecore import i18n

# Plasma Libs
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
from PyKDE4.kdeui import KIconLoader

# Custom Widgets
from widgets.popup import Popup, NmIcon, Blinker

# KDE4 Notifier
from widgets.notify import Notifier

# Solid
from PyKDE4.solid import Solid

# Network Interface for operations
# It creates a dbus-mainlook or registers 
# itself to the current dbus mainloop if exists
from backend.pardusBackend import NetworkIface

WIRED           = "network-wired"

CONNECTED       = {"title"  :i18n("Connected"),
                   "emblem" :"dialog-ok-apply",
                   "solid"  :Solid.Networking.Connected}
DISCONNECTED    = {"title"  :i18n("Disconnected"),
                   "emblem" :"edit-delete",
                   "solid"  :Solid.Networking.Unconnected}
CONNECTING      = {"title"  :i18n("Connecting"),
                   "emblem" :"chronometer",
                   "solid"  :Solid.Networking.Connecting}

ICONPATH        = "%s/contents/code/icons/%s.png"

class NmApplet(plasmascript.Applet):
    """ Our main applet derived from plasmascript.Applet """

    def __init__(self, parent):
        plasmascript.Applet.__init__(self, parent)

    def init(self):
        """ Const method for initializing the applet """

        self.iface = NetworkIface()
        self.notifyface = Notifier(dbus.get_default_main_loop())
        self.notifyface.registerNetwork()

        # Aspect ratio defined in Plasma
        self.setAspectRatioMode(Plasma.Square)

        self.loader = KIconLoader()
        self.defaultIcon = ICONPATH % (self.package().path(), WIRED)
        self.emblem = DISCONNECTED["emblem"]

        self.icon = NmIcon(self)
        self.icon.setToolTip(i18n("Click here to show connections.."))

        self.layout = QGraphicsLinearLayout(self.applet)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addItem(self.icon)

        self.connect(self.icon, SIGNAL("clicked()"), self.showDialog)

        self.receiverBlinker = Blinker(self)
        self.transmitterBlinker = Blinker(self, QColor(255,114,32))

        # Listen data transfers from lastUsed Device ..
        self.lastActiveDevice = None
        self.lastActivePackage = None

        self.dialog = Plasma.Dialog()
        self.dialog.setWindowFlags(Qt.Popup)

        self.updateTheme()

        self.popup = Popup(self.dialog, self)
        self.popup.init()

        self.dialog.resize(self.size().toSize())

        # It may cause crashes in PlasmoidViewer but luckly not in Plasma :)
        self.connect(Plasma.Theme.defaultTheme(), SIGNAL("themeChanged()"), self.updateTheme)

        self.connect(self.popup.ui.nmButton, SIGNAL("clicked()"), self.openNM)

        # Listen network status from comar
        self.iface.listen(self.handler)

        QTimer.singleShot(4000, self.dataUpdated)

    def paintInterface(self, painter, option, rect):
        size = min(rect.width(),rect.height())*2

        # Current Icon
        pix    = self.loader.loadIcon(self.defaultIcon, KIconLoader.NoGroup, size)

        # Current Emblem
        emblem = self.loader.loadIcon(self.emblem, KIconLoader.NoGroup, size/3)

        paint = QPainter(pix)
        paint.setRenderHint(QPainter.SmoothPixmapTransform)
        paint.setRenderHint(QPainter.Antialiasing)

        f = rect.width() * 0.1
        # Draw Rx
        if self.receiverBlinker.isActive():
            _path = QPainterPath()
            _path.addEllipse(QRectF(size * 0.9, size * 0.9, f, f))
            paint.fillPath(_path, self.receiverBlinker.color)

        # Draw Tx
        if self.transmitterBlinker.isActive():
            _path = QPainterPath()
            _path.addEllipse(QRectF(size * 0.8, size * 0.9, f, f))
            paint.fillPath(_path, self.transmitterBlinker.color)

        # Draw Emblem
        paint.drawPixmap(0,0,emblem)
        paint.end()

        # Update the icon
        self.icon.setIcon(QIcon(pix))
        self.icon.update()

    def dataUpdated(self):
        if self.lastActiveDevice:
            if self.lastActivePackage == 'wireless_tools':
                # Show SIGNAL Strength
                icon =  self.iface.strength(self.lastActiveDevice)/17
                if not icon in range(1,6):
                    icon = 1
                self.defaultIcon = ICONPATH % (self.package().path(), icon)
            else:
                self.defaultIcon = ICONPATH % (self.package().path(), WIRED)
            self.receiverBlinker.update(self.iface.stat(self.lastActiveDevice)[0])
            self.transmitterBlinker.update(self.iface.stat(self.lastActiveDevice)[1])
        else:
            self.receiverBlinker.stop()
            self.transmitterBlinker.stop()
        self.update()
        QTimer.singleShot(5000, self.dataUpdated)

    def constraintsEvent(self, constraints):
        self.setBackgroundHints(Plasma.Applet.NoBackground)

    def openNM(self):
        self.dialog.hide()
        os.popen('network-manager')

    def handler(self, package, signal, args):
        args = map(lambda x: str(x), list(args))

        # Network StateChanged
        if signal == "stateChanged":

            lastState = {"title":i18n("Unknown"),
                         "emblem":"dialog-warning",
                         "solid":Solid.Networking.Unknown}

            ip = None
            self.lastActiveDevice  = self.iface.info(package, args[0])['device_id']
            self.lastActivePackage = package

            # Network UP
            if (str(args[1]) == "up"):
                msg = i18n("Connected to <b>%s</b> IP: %s" % (args[0], args[2]))
                lastState = CONNECTED

                # Current Ip
                ip = args[2]

            # Network CONNECTING
            elif (str(args[1]) == "connecting"):
                msg = i18n("Connecting to <b>%s</b> .." % args[0])
                lastState = CONNECTING

            # Network DOWN
            else:
                if self.lastActivePackage == 'wireless_tools':
                    self.defaultIcon = ICONPATH % (self.package().path(), "off")

                self.lastActiveDevice  = None
                self.lastActivePackage = None

                msg = i18n("Disconnected")
                lastState = DISCONNECTED

            # Update Connection
            self.popup.setConnectionStatus(package, lastState["title"])
            self.popup.connections[package][unicode(args[0])].setState(str(args[1]), ip or '')

            # Show Notification
            self.notifyface.notify(str(msg), lastState["solid"])

            # Update Icon
            self.emblem = lastState["emblem"]
            self.dataUpdated()

        # ConnectionChanged
        elif signal == "connectionChanged":
            if args[0] == 'deleted':
                self.popup.connections[package][unicode(args[1])].hide()
            if args[0] == 'added':
                self.popup.addConnectionItem(package, unicode(args[1]))

    def updateTheme(self):
        self.dialog.setStyleSheet("padding-left:0;color: %s;" % Plasma.Theme.defaultTheme().color(Plasma.Theme.TextColor).name())

    def showDialog(self):
        self.dialog.show()
        self.dialog.move(self.popupPosition(self.dialog.sizeHint()))

def CreateApplet(parent):
    return NmApplet(parent)

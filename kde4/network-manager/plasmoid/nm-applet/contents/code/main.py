#!/usr/bin/python
# -*- coding: utf-8 -*-

# OS
import os
import time

# D-Bus
import dbus

# Qt Libs
from PyQt4.QtCore import Qt, SIGNAL, SLOT, pyqtSignature, QString, QTimer, QRectF, QTimer
from PyQt4.QtGui import QWidget, QFrame, QGraphicsLinearLayout, QPixmap, QColor, QPainterPath, QPainter

# Plasma Libs
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript

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

receiverPath = "network/interfaces/%s/receiver/data"
transmitterPath = "network/interfaces/%s/transmitter/data"

class NmApplet(plasmascript.Applet):
    """ Our main applet derived from plasmascript.Applet """

    def __init__(self, parent):
        plasmascript.Applet.__init__(self, parent)
        self.iface = NetworkIface()
        self.notifyface = Notifier(dbus.get_default_main_loop())
        self.notifyface.registerNetwork()
        self.timer = QTimer()

    def init(self):
        """ Const method for initializing the applet """

        # Aspect ratio defined in Plasma
        self.setAspectRatioMode(Plasma.ConstrainedSquare)
        self.defaultIcon = "%s/contents/code/icons/icon.svgz" % self.package().path()

        self.icon = NmIcon(self)
        self.icon.setSvg(self.defaultIcon, "native")
        self.icon.setToolTip("Click here to show connections..")

        self.layout = QGraphicsLinearLayout(self.applet)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addItem(self.icon)

        self.connect(self.icon, SIGNAL("clicked()"), self.showDialog)

        self.receiverBlinker = Blinker(self)
        self.transmitterBlinker = Blinker(self, QColor(255,114,32))

        # Listen data transfers from lastUsed Device ..
        self.lastActiveDevice = None
        self.connect(self.timer, SIGNAL("timeout()"), self.dataUpdate);
        self.timer.start(5000)

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

    def paintInterface(self, painter, option, rect):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.save()
        f = rect.width()/12
        if self.receiverBlinker.isActive():
            _rect = QRectF(rect.x()+rect.width()-f*1.2, rect.y()+rect.height()-f*1.3, f, f)
            _path = QPainterPath()
            _path.addEllipse(_rect)
            painter.fillPath(_path, self.receiverBlinker.color)
        if self.transmitterBlinker.isActive():
            _rect = QRectF(rect.x()+rect.width()-f*2*1.2-4, rect.y()+rect.height()-f*1.3, f, f)
            _path = QPainterPath()
            _path.addEllipse(_rect)
            painter.fillPath(_path, self.transmitterBlinker.color)
        painter.restore()

    def dataUpdate(self):
        print "Updating .... "
        if self.lastActiveDevice:
            self.receiverBlinker.update(self.iface.stat(self.lastActiveDevice)[0])
            self.transmitterBlinker.update(self.iface.stat(self.lastActiveDevice)[1])

    def constraintsEvent(self, constraints):
        self.setBackgroundHints(Plasma.Applet.NoBackground)

    def openNM(self):
        self.dialog.hide()
        os.popen('network-manager')

    def handler(self, package, signal, args):
        args = map(lambda x: str(x), list(args))
        if signal == "stateChanged":
            solidState = Solid.Networking.Unknown
            ip = str()
            if (str(args[1]) == "up"):
                lastDevice = self.iface.info(package, args[0])['device_id']
                msg = "Connected to <b>%s</b> IP: %s" % (args[0], args[2])
                ip = args[2]
                self.lastActiveDevice = lastDevice
                self.popup.setConnectionStatus(package, "Connected")
                self.icon.setSvg(self.defaultIcon)
                solidState = Solid.Networking.Connected
            elif (str(args[1]) == "connecting"):
                msg = "Connecting to <b>%s</b> .." % args[0]
                self.popup.setConnectionStatus(package, "Connecting..")
                solidState = Solid.Networking.Connecting
            else:
                msg = "Disconnected"
                self.popup.setConnectionStatus(package, msg)
                self.lastActiveDevice = None
                self.icon.setSvg(self.defaultIcon, "native")
                solidState = Solid.Networking.Unconnected
            self.popup.connections[package][unicode(args[0])].setState(str(args[1]), ip)
            self.notifyface.notify(str(msg), solidState)

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

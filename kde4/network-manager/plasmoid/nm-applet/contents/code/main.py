#!/usr/bin/python
# -*- coding: utf-8 -*-

# OS
import os
import time

# D-Bus
import dbus

# Qt Libs
from PyQt4.QtCore import Qt, SIGNAL, SLOT, pyqtSignature, QString, QTimer
from PyQt4.QtGui import QWidget, QFrame, QGraphicsLinearLayout, QPixmap

# Plasma Libs
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript

# Custom Widgets
from widgets.popup import Popup

# KDE4 Notifier
from widgets.notify import Notifier

# Solid
from PyKDE4.solid import Solid

# Network Interface for operations
# It creates a dbus-mainlook or registers 
# itself to the current dbus mainloop if exists
from backend.pardus import NetworkIface

iface = NetworkIface()

def getDevice(info):
    return info['device_id'].split(':')[1].split('_')[-1]

class NmApplet(plasmascript.Applet):
    """ Our main applet derived from plasmascript.Applet """

    def __init__(self, parent):
        plasmascript.Applet.__init__(self, parent)
        self.iface = iface
        self.notifyface = Notifier(dbus.get_default_main_loop())
        self.notifyface.registerNetwork()

    def init(self):
        """ Const method for initializing the applet """

        self.defaultIcon = "%s/contents/code/icons/icon.svgz" % self.package().path()

        # Aspect ratio defined in Plasma
        self.setAspectRatioMode(Plasma.ConstrainedSquare)

        self.layout = QGraphicsLinearLayout(self.applet)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.icon = Plasma.IconWidget()
        self.icon.setSvg(self.defaultIcon, "native")
        self.icon.setToolTip("Click here to show connections..")

        self.layout.addItem(self.icon)

        try:
            # new kdebindings4 and kdebase4-workspace are required.
            self.registerAsDragHandle(self.icon)
        except:
            print "Please update your kde4 packages !"

        self.connect(self.icon, SIGNAL("clicked()"), self.showDialog)

        # Listen data transfers from systemmonitor data engine ..
        self.lastActiveDevice = None
        self.listenDataTransfers()
        self.color = Qt.green
        self.activityTimer = QTimer(self)
        self.connect(self.activityTimer, SIGNAL("timeout()"), self.blinkLight)

        self.dialog = Plasma.Dialog()
        self.dialog.setWindowFlags(Qt.Popup)
        self.updateTheme()

        self.popup = Popup(self.dialog, self)
        self.popup.init()

        self.dialog.resize(self.size().toSize())
        self.dialog.adjustSize()

        # It may cause crashes in PlasmoidViewer but luckly not in Plasma :)
        self.connect(Plasma.Theme.defaultTheme(), SIGNAL("themeChanged()"), self.updateTheme)

        self.connect(self.popup.ui.nmButton, SIGNAL("clicked()"), self.openNM)

        # Listen network status from comar
        self.iface.listen(self.handler)
        self.activityTimer.start(100)

    def listenDataTransfers(self):
        self.engine = self.dataEngine("systemmonitor")
        if self.engine.sources().count() == 0:
            self.connect(self.engine, SIGNAL("sourceAdded(QString)"), SLOT("initLater(QString)"))
        else:
            self.parseSources()

    def paintInterface(self, painter, option, rect):
        painter.save()
        f = rect.width()/10
        if self.activityTimer.isActive():
            painter.fillRect(rect.x()+rect.width()-f, rect.y()+rect.height()-f, f, f, self.color)
        painter.restore()

    def blinkLight(self):
        if self.color == Qt.green:
            self.color = Qt.transparent
        else:
            self.color = Qt.green
        self.update()

    @pyqtSignature("initLater(const QString &)")
    def initLater(self, name):
        if name == "ps":
            QTimer.singleShot(0, self.parseSources)

    def parseSources(self):
        statePath = "network/interfaces/%s/receiver/data"
        if self.lastActiveDevice:
            self.engine.connectSource(statePath % self.lastActiveDevice, self, 500)

    def stopFollowing(self, device):
        statePath = "network/interfaces/%s/receiver/data"
        self.engine.disconnectSource(statePath % device, self)
        self.activityTimer.stop()

    @pyqtSignature("dataUpdated(const QString &, const Plasma::DataEngine::Data &)")
    def dataUpdated(self, sourceName, data):
        if data.has_key(QString('value')):
            if data[QString('value')].toInt()[0] == 0:
                self.activityTimer.stop()
                self.color = Qt.transparent
                self.update()
            else:
                self.activityTimer.start(100)

    def constraintsEvent(self, constraints):
        self.setBackgroundHints(Plasma.Applet.NoBackground)

    def openNM(self):
        self.dialog.hide()
        os.system('network-manager')

    def handler(self, package, signal, args):
        args = map(lambda x: str(x), list(args))
        if signal == "stateChanged":
            solidState = Solid.Networking.Unknown
            lastDevice = getDevice(iface.info(package, args[0]))
            ip = str()
            if (str(args[1]) == "up"):
                msg = "Connected to <b>%s</b> IP: %s" % (args[0], args[2])
                ip = args[2]
                self.lastActiveDevice = lastDevice
                self.parseSources()
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
                self.stopFollowing(lastDevice)
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
        self.dialog.setStyleSheet("color: %s;" % Plasma.Theme.defaultTheme().color(Plasma.Theme.TextColor).name())

    def showDialog(self):
        if self.dialog.isVisible():
            self.dialog.hide()
        else:
            self.dialog.show()
            self.dialog.move(self.popupPosition(self.dialog.sizeHint()))

def CreateApplet(parent):
    return NmApplet(parent)

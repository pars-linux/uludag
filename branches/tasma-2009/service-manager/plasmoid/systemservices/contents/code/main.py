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

try:
    from PyKDE4 import plasmascript
except:
    import plasmascript

# DBUS-QT
from dbus.mainloop.qt import DBusQtMainLoop

class SystemServicesApplet(plasmascript.Applet):
    def __init__(self, parent, args=None):
        plasmascript.Applet.__init__(self,parent)
        self.link = comar.Link()

    def init(self):
        self.setHasConfigurationInterface(False)
        self.resize(125, 125)
        self.setAspectRatioMode(Plasma.Square)

        self.theme = Plasma.Svg(self)
        self.theme.setImagePath("widgets/background")

        self.layout = QGraphicsLinearLayout(Qt.Vertical, self.applet)

        self.theme.resize(self.size())
        self.getServices()

    def handleServices(self, package, exception, results):
        lab = Plasma.Label(self.applet)
        lab.setText(package)
        self.layout.addItem(lab)

    def handler(self, package, signal, args):
        pass
        # self.widgets[package].setState(args[1])
        # print args, signal, package

    def getServices(self):
        self.link.listenSignals("System.Service", self.handler)
        # Get service list from comar link
        self.link.System.Service.info(async=self.handleServices)

def CreateApplet(parent):
    # DBUS MainLoop
    DBusQtMainLoop(set_as_default = True)
    return SystemServicesApplet(parent)

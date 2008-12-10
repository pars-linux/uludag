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

# We dont have this module in our kdebindings
try:
    from PyKDE4 import plasmascript
except:
    import plasmascript

# Plasmoid Config
from config import SystemServicesConfig

# DBUS-QT
from dbus.mainloop.qt import DBusQtMainLoop

class SystemServicesApplet(plasmascript.Applet):
    """ Our main applet derived from plasmascript.Applet """

    def __init__(self, parent, args=None):
        plasmascript.Applet.__init__(self, parent)

        # Our Comar Link
        self.link = comar.Link()

    def init(self):
        """ Const method for initializing the applet """

        # Configuration interface support comes with plasma
        self.setHasConfigurationInterface(True)

        # Aspect ratio defined in Plasma
        self.setAspectRatioMode(Plasma.IgnoreAspectRatio)

        # Theme is a const variable holds Applet Theme
        self.theme = Plasma.Svg(self)

        # It gets default plasma theme's background
        self.theme.setImagePath("widgets/background")

        # Main layout for ServiceItemWidgets
        self.layout = QGraphicsLinearLayout(Qt.Vertical, self.applet)

        # Initial size
        self.resize(125, 125)

        # Resize current theme as applet size
        self.theme.resize(self.size())

        # Create config dialog
        self.prepareConfigDialog()

        # Call comar to get all services infos
        self.getServices()

    def handleServices(self, package, exception, results):
        """ Handles comar feedbacks and creates the widgets in applet."""
        if not exception:
            package = str(package)
            if package in self.config_ui.enabledServices:
                lab = Plasma.Label(self.applet)
                lab.setText(package)
                self.layout.addItem(lab)
            self.config_ui.addItemToList(package)

    def handler(self, package, signal, args):
        pass

    def getServices(self):
        """ Makes comar call to get all services information """

        # It listens System.Service signals and route them to handler method
        self.link.listenSignals("System.Service", self.handler)

        # Get service list from comar link
        self.link.System.Service.info(async=self.handleServices)

    def updateServiceList(self):
        # delete the current layout
        del self.layout

        # and create new one
        self.layout = QGraphicsLinearLayout(Qt.Vertical, self.applet)

        # Get service list from comar link
        self.link.System.Service.info(async=self.handleServices)

    def prepareConfigDialog(self):
        windowTitle = str(self.applet.name()) + " Settings"

        self.dialog = KDialog(None)
        self.dialog.setWindowTitle(windowTitle)

        self.config_ui = SystemServicesConfig(self.dialog, self.config)
        self.dialog.setMainWidget(self.config_ui)

        self.dialog.setButtons(KDialog.ButtonCodes(KDialog.ButtonCode(KDialog.Ok | KDialog.Cancel | KDialog.Apply)))
        self.dialog.showButton(KDialog.Apply, False)

        self.connect(self.dialog, SIGNAL("applyClicked()"), self, SLOT("configAccepted()"))
        self.connect(self.dialog, SIGNAL("okClicked()"), self, SLOT("configAccepted()"))

    def showConfigurationInterface(self):
        self.dialog.show()

    @pyqtSignature("configAccepted()")
    def configAccepted(self):

        # Find enabled services from list
        _enabledServices = []
        _target = self.config_ui.serviceList
        for row in range(_target.count()):
            item = _target.itemWidget(_target.item(row))
            if item.isChecked():
                # I don't know why it is happening but some service strings includes & :S
                _enabledServices.append(str(item.text()).replace('&',''))

        # Write them into the config file
        cg = self.config()
        cg.writeEntry("services", QVariant(_enabledServices))

        # Emit const Signal to save config file
        self.emit(SIGNAL("configNeedsSaving()"))
        # Update enabled services with current ones
        self.config_ui.enabledServices = _enabledServices

def CreateApplet(parent):
    # DBUS MainLoop
    DBusQtMainLoop(set_as_default = True)

    return SystemServicesApplet(parent)

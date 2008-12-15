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
import plasmascript

# Plasmoid Config
from config import SystemServicesConfig

# DBUS-QT
from dbus.mainloop.qt import DBusQtMainLoop

class WidgetSystemServices(QWidget):
    def __init__(self, data):
        QWidget.__init__(self)
        self.setStyleSheet("background-color: rgba(255, 255, 255, 0);color: rgb(255, 255, 255)")
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setMargin(0)

        self.label = QLabel(self)
        self.label.setText(data)
        self.horizontalLayout.addWidget(self.label)

        spacerItem = QSpacerItem(130, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        self.start = QPushButton(self)
        self.start.setText("Start")
        self.horizontalLayout.addWidget(self.start)

        self.stop = QPushButton(self)
        self.stop.setText("Stop")
        self.horizontalLayout.addWidget(self.stop)

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

        # Our widget stack
        self._widgets = {}

        # Our animator instance to animate adding/deleting widgets
        self.animator = Plasma.Animator.self()

        # Call comar to get all services infos
        self._just_update = False
        self.getServices()

    def handleServices(self, package, exception, results):
        """ Handles comar feedbacks and creates the widgets in applet."""
        if not exception:
            package = str(package)

            # If service is enabled create a proper widget and add it to the plasmoid
            if package in self.config_ui.enabledServices:
                # We need to use QGraphicsProxy
                proxy = QGraphicsProxyWidget()

                # Create widget which describes and handles service state
                widget = WidgetSystemServices(package)

                # Set our widget as QGraphicsWidget
                proxy.setWidget(widget)

                # Add item to widget
                self.layout.addItem(proxy)

                # Animate creation of widget
                self.animator.animateItem(proxy,0)

                # Add widget to our widget stack
                self._widgets[package] = widget

                # Update the size of Plasmoid
                self.constraintsEvent(Plasma.SizeConstraint)

            # This method handles all service info request
            # but in configuration list we don't need to add them again..
            if not self._just_update:
                self.config_ui.addItemToList(package)

    def constraintsEvent(self, constraints):
        if constraints & Plasma.SizeConstraint:
            # Update plasmoid size according to number of enabled services
            bh = len(self._widgets) * 40
            resize = False
            if bh > 0:
                size = self.size()
                height = size.height()
                width = size.width()
                bw = self._widgets.values()[0].width() + 40
                if size.height() < bh:
                    height = bh
                    resize = True
                if size.width() < bw:
                    width = bw
                    resize = True
                if resize:
                    self.resize(width,height)
                    self.theme.resize(self.size())

    def handler(self, package, signal, args):
        pass

    def getServices(self):
        """ Makes comar call to get all services information """

        # It listens System.Service signals and route them to handler method
        self.link.listenSignals("System.Service", self.handler)

        # Get service list from comar link
        self.link.System.Service.info(async=self.handleServices)

    def updateList(self):

        # call hide for each widget
        for wi in self._widgets.values():
            wi.hide()

        # remove them from layout
        for i in range(self.layout.count()):
            self.layout.removeAt(i)

        # and reset the widgets stack
        self._widgets = {}

        # and create a new layout
        self.layout = QGraphicsLinearLayout(Qt.Vertical, self.applet)

        # Get service list from comar link again and again..
        self._just_update = True
        self.link.System.Service.info(async=self.handleServices)

    def prepareConfigDialog(self):
        windowTitle = str(self.applet.name()) + " Settings"

        self.dialog = KDialog(None)
        self.dialog.setWindowTitle(windowTitle)

        self.config_ui = SystemServicesConfig(self.dialog, self.config())
        self.dialog.setMainWidget(self.config_ui)

        self.dialog.setButtons(KDialog.ButtonCodes(KDialog.ButtonCode(KDialog.Ok | KDialog.Cancel | KDialog.Apply)))
        self.dialog.showButton(KDialog.Apply, False)

        self.connect(self.dialog, SIGNAL("applyClicked()"), self, SLOT("configAccepted()"))
        self.connect(self.dialog, SIGNAL("okClicked()"), self, SLOT("configAccepted()"))

        if self.config_ui.enabledServices[0] == '':
            # we need new kdebindings for that
            self.setConfigurationRequired(True, "Click configure to select services")

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
        self.config_ui.config.writeEntry("services", QVariant(_enabledServices))

        # Update enabled services with current ones
        self.config_ui.enabledServices = _enabledServices

        # It is very important to sync config before saving !
        self.config_ui.config.sync()

        # Emit const Signal to save config file
        self.emit(SIGNAL("configNeedsSaving()"))

        # if there is a enabled services we dont need configure button anymore !
        if len(_enabledServices) > 0:
            self.setConfigurationRequired(False)

        # and update the widget
        self.updateList()

def CreateApplet(parent):
    # DBUS MainLoop
    DBusQtMainLoop(set_as_default = True)

    return SystemServicesApplet(parent)

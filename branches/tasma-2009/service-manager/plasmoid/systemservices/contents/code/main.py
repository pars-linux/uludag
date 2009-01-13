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

# Plasmoid Config
from config import SystemServicesConfig

# DBUS-QT
from dbus.mainloop.qt import DBusQtMainLoop

class WidgetSystemServices(QGraphicsWidget):
    def __init__(self, parent, name, state=None):
        QGraphicsWidget.__init__(self, parent)
        self.name = name
        self.layout = QGraphicsLinearLayout(Qt.Horizontal, self)

        self.label = Plasma.Label(self)
        self.label.setText(name)
        self.layout.addItem(self.label)

        self.layout.addStretch()

        self.switcher = Plasma.TabBar(self)
        self.switcher.addTab("Start")
        self.switcher.addTab("Stop")
        self.layout.addItem(self.switcher)

class WidgetStack(QGraphicsWidget):
    def __init__(self, parent):
        QGraphicsWidget.__init__(self, parent)
        self.layout = QGraphicsLinearLayout(Qt.Vertical, self)
        self._widgets = {}

        # Our animator instance to animate adding/deleting widgets
        self.animator = Plasma.Animator.self()

    def addItem(self, widget):
        # Animate creation of widget
        self.animator.animateItem(widget, 0)
        self.layout.addItem(widget)

        self._widgets[widget.name] = widget

class SystemServicesApplet(plasmascript.Applet):
    """ Our main applet derived from plasmascript.Applet """

    def __init__(self, parent, args=None):
        plasmascript.Applet.__init__(self, parent)

        # Our Comar Link
        self.link = comar.Link()

        # Available services
        self._services = list(self.link.System.Service)

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

        # Resize current theme as applet size
        self.theme.resize(self.size())

        self.mainWidget = None
        self.layout = None

        # Create config dialog
        if self.prepareConfigDialog():
            self.initPlasmoid()

    def prepareConfigDialog(self):
        windowTitle = str(self.applet.name()) + " Settings"

        self.dialog = KDialog(None)
        self.dialog.setWindowTitle(windowTitle)

        self.config_ui = SystemServicesConfig(self.dialog, self.config())
        self.dialog.setMainWidget(self.config_ui)

        for package in self._services:
            self.config_ui.addItemToList(package)

        self.dialog.setButtons(KDialog.ButtonCodes(KDialog.ButtonCode(KDialog.Ok | KDialog.Cancel | KDialog.Apply)))
        self.dialog.showButton(KDialog.Apply, False)

        self.connect(self.dialog, SIGNAL("applyClicked()"), self, SLOT("configAccepted()"))
        self.connect(self.dialog, SIGNAL("okClicked()"), self, SLOT("configAccepted()"))

        if self.config_ui.enabledServices[0] == '':
            self.setConfigurationRequired(True, "Click configure to select services")
            self.resize(200,200)
            return False
        return True

    def initPlasmoid(self):
        # Layout
        if not self.layout:
            self.layout = QGraphicsLinearLayout(Qt.Vertical, self.applet)
            self.layout.setContentsMargins(0,0,0,0)
            self.layout.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

            self.setLayout(self.layout)
            self.constraintsEvent(Plasma.SizeConstraint)

        if self.mainWidget:
            self.mainWidget.hide()
            self.layout.removeAt(0)
            del self.mainWidget

        self.mainWidget = WidgetStack(self.applet)
        self.layout.addItem(self.mainWidget)

        for package in self._services:
            # If service is enabled create a proper widget and add it to the plasmoid
            if package in self.config_ui.enabledServices:
                # Create widget which describes and handles service state
                widget = WidgetSystemServices(self.applet, package)

                # Add widget to mainWidget
                self.mainWidget.addItem(widget)

                # Update the size of Plasmoid
                self.constraintsEvent(Plasma.SizeConstraint)

    def constraintsEvent(self, constraints):
        if constraints & Plasma.SizeConstraint:
            self.layout.updateGeometry()
            self.theme.resize(self.size())

    def handler(self, package, signal, args):
        import os
        os.system("notify bibi bibi ...")

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
            # FIXME It should be fixed in plasmascript.py, 
            # when we dont need configuration means we dont have any reason..
            self.setConfigurationRequired(False, '')

        # and update the widget
        self.initPlasmoid()

def CreateApplet(parent):
    applet = SystemServicesApplet(parent)
    return applet


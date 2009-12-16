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

# Our Comar Link
link = comar.Link()

class WifiItem_Qt(QWidget):
    def __init__(self, parent, data):
        QWidget.__init__(self)
        self.setStyleSheet("background-color: transparent;color: white")
        self.layout = QHBoxLayout(self)
        self.layout.setMargin(0)

        self.label = QLabel(self)
        self.label.setText(data['remote'])
        self.layout.addWidget(self.label)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        spacerItem = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout.addItem(spacerItem)

        self.quality = QProgressBar(self)
        self.quality.setSizePolicy(sizePolicy)
        self.layout.addWidget(self.quality)
        self.quality.setValue(int(data['quality']))


class WifiItem_Plasma(QGraphicsWidget):
    def __init__(self, parent, data):
        QGraphicsWidget.__init__(self, parent)
        self.layout = QGraphicsLinearLayout(Qt.Horizontal, self)

        self.label = Plasma.Label(self)
        self.label.setText(data['remote'])
        self.layout.addItem(self.label)

        self.layout.addStretch()

        self.meter = Plasma.Meter(self)
        self.meter.setMeterType(Plasma.Meter.BarMeterHorizontal)
        self.meter.setValue(int(data['quality']))
        self.layout.addItem(self.meter)

class WidgetStack(QGraphicsWidget):
    def __init__(self, parent):
        QGraphicsWidget.__init__(self, parent)
        self.layout = QGraphicsLinearLayout(Qt.Vertical, self)

    def addItem(self, widget):
        try:
            self.layout.addItem(widget)
        except TypeError:
            proxy = QGraphicsProxyWidget()
            proxy.setWidget(widget)
            self.layout.addItem(proxy)

class WifiRadarApplet(plasmascript.Applet):
    """ Our main applet derived from plasmascript.Applet """

    def __init__(self, parent, args=None):
        plasmascript.Applet.__init__(self, parent)
        timer = QTimer(self)
        self.connect(timer, SIGNAL('timeout()'), self.initPlasmoid)
        timer.start(5000)

    def init(self):
        """ Const method for initializing the applet """

        # Configuration interface support comes with plasma
        self.setHasConfigurationInterface(False)

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

        self.initPlasmoid()

    def getWifi(self):
        devices = list(link.Net.Link["wireless_tools"].deviceList())
        if len(devices) == 0:
            return (False, 'No wifi device found')
        hotspots = list(link.Net.Link["wireless_tools"].scanRemote(list(devices)[0]))
        if len(hotspots) == 0:
            return (False, 'No hotspot found')
        return (True, hotspots)

    def initPlasmoid(self):
        # Layout
        if not self.layout:
            self.layout = QGraphicsLinearLayout(Qt.Vertical, self.applet)
            self.layout.setContentsMargins(0,0,0,0)
            self.layout.setSpacing(0)
            self.layout.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))

            self.setLayout(self.layout)
            self.constraintsEvent(Plasma.SizeConstraint)

        if self.mainWidget:
            self.mainWidget.hide()
            self.layout.removeAt(0)
            del self.mainWidget

        self.mainWidget = WidgetStack(self.applet)
        self.layout.addItem(self.mainWidget)

        hotspots = self.getWifi()
        if hotspots[0] == False:
            label = Plasma.Label()
            label.setText(hotspots[1])
            self.mainWidget.addItem(label)
        else:
            for spot in hotspots[1]:
                self.mainWidget.addItem(WifiItem_Plasma(self.mainWidget, spot))

        # Update the size of Plasmoid
        self.constraintsEvent(Plasma.SizeConstraint)

    def constraintsEvent(self, constraints):
        if constraints & Plasma.SizeConstraint:
            self.theme.resize(self.size())
            if self.mainWidget:
                self.applet.setMinimumSize(self.mainWidget.minimumSize())# * len(self.mainWidget._widgets))

def CreateApplet(parent):
    return WifiRadarApplet(parent)

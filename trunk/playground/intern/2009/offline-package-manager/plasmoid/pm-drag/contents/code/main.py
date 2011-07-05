#!/usr/bin/python
# -*- coding: utf-8 -*-

# Os & Comar
import os
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

class PmDragApplet(plasmascript.Applet):
    """ Our main applet derived from plasmascript.Applet """

    def __init__(self, parent, args=None):
        plasmascript.Applet.__init__(self, parent)

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

        self.applet.setAcceptDrops(True)

        self.layout = QGraphicsLinearLayout(self.applet)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.layout.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))

        self.icon = Plasma.IconWidget()
        self.icon.setIcon("package-x-generic")
        self.icon.setToolTip("Drag and Drop your Pisi packages on it ..")
        self.icon.setAcceptDrops(False)
        self.layout.addItem(self.icon)

    def constraintsEvent(self, constraints):
        if constraints & Plasma.SizeConstraint:
            self.theme.resize(self.size())

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        if str(event.mimeData().text()).endswith('.pisi'):
            os.system("/usr/kde/3.5/bin/package-manager --install %s" % event.mimeData().text())

    def mousePressEvent(self, event):
        pass

def CreateApplet(parent):
    return PmDragApplet(parent)

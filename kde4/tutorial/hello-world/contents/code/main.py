#!/usr/bin/python
# -*- coding: utf-8 -*-

# Plasma Libs
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript

# Qt Core
from PyQt4.Qt import Qt, QGraphicsLinearLayout

class HelloWorldApplet(plasmascript.Applet):
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

        # Update the size of Plasmoid
        self.constraintsEvent(Plasma.SizeConstraint)

        # We need a layout
        self.layout = QGraphicsLinearLayout(Qt.Horizontal, self.applet)
        self.setLayout(self.layout)

        # A label
        self.label = Plasma.Label(self.applet)

        # to say hello world !
        self.label.setText("Hello World !")

        # and centered
        self.label.setAlignment(Qt.AlignCenter)

        # add it to current layout
        self.layout.addItem(self.label)

        # resize the applet
        self.resize(125, 125)

    def constraintsEvent(self, constraints):
        if constraints & Plasma.SizeConstraint:
            self.theme.resize(self.size())

def CreateApplet(parent):
    return HelloWorldApplet(parent)


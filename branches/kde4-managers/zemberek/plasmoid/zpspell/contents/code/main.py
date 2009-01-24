#!/usr/bin/python
# -*- coding: utf-8 -*-

# Dbus
import dbus

# Qt Libs
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# KDE Libs
from PyKDE4.kdecore import *
from PyKDE4.kdeui import *

# Plasma Libs
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript

systemBus = dbus.SystemBus()
zpProxy = systemBus.get_object('net.zemberekserver.server.dbus', '/net/zemberekserver/server/dbus/ZemberekDbus')
zpInterface = dbus.Interface(zpProxy, 'net.zemberekserver.server.dbus.ZemberekDbusInterface')

class ZpSpellApplet(plasmascript.Applet):
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

        self.layout = QGraphicsGridLayout(self.applet)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.layout.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))

        self.line_edit = Plasma.LineEdit(self.applet)
        self.layout.addItem(self.line_edit,0,0)

        self.text_edit = Plasma.TextEdit(self.applet)
        self.layout.addItem(self.text_edit,1,0)
        self.check()

        self.connect(self.line_edit, SIGNAL("textEdited(const QString&)"), self.check)

        # Update the size of Plasmoid
        self.constraintsEvent(Plasma.SizeConstraint)

    def check(self, word=''):
        self.text_edit.setText('')
        if not word:
            word = unicode(self.line_edit.text())
        else:
            word = unicode(word)
        if len(word) == 0:
            self.text_edit.setText("<i>Start writing to line edit for spell checking..</i>")
            return
        if zpInterface.kelimeDenetle(word):
            self.text_edit.setText("<b>Looks ok !</b>")
        else:
            posibilities = zpInterface.oner(word)
            if len(posibilities) > 0:
                self.text_edit.setText("Something wrong it may be:")
            else:
                self.text_edit.setText("I have no idea what it would be..")
            for posibility in posibilities:
                self.text_edit.setText("%s<b> - %s</b>\n" % (self.text_edit.text(), str(posibility)))

    def constraintsEvent(self, constraints):
        if constraints & Plasma.SizeConstraint:
            self.theme.resize(self.size())
            #self.applet.setMinimumSize(self.mainWidget.minimumSize())

def CreateApplet(parent):
    return ZpSpellApplet(parent)

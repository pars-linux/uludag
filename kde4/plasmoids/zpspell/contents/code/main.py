#!/usr/bin/python
# -*- coding: utf-8 -*-

# Dbus & Comar
import dbus
import comar

import time

# Qt Libs
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# KDE Libs
from PyKDE4.kdecore import *
from PyKDE4.kdeui import *

# Plasma Libs
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript

# DBUS-QT
from dbus.mainloop.qt import DBusQtMainLoop
from dbus import DBusException

# Global Zemberek Interface
zpInterface = None


# it is very important to check if there is an active mainloop
# before creating a new one, it may cause to crash plasma itself
if not dbus.get_default_main_loop():
    from dbus.mainloop.qt import DBusQtMainLoop
    DBusQtMainLoop(set_as_default=True)

# Our Comar Link
link = comar.Link()
systemBus = dbus.SystemBus()

def mkZpInterface():
    global zpInterface
    try:
        zpProxy = systemBus.get_object('net.zemberekserver.server.dbus', '/net/zemberekserver/server/dbus/ZemberekDbus')
        zpInterface = dbus.Interface(zpProxy, 'net.zemberekserver.server.dbus.ZemberekDbusInterface')
    except dbus.exceptions.DBusException:
        zpInterface = None

class FailedWidget(QGraphicsWidget):
    def __init__(self, parent):
        QGraphicsWidget.__init__(self, parent)
        self.layout = QGraphicsLinearLayout(Qt.Vertical, self)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.layout.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))

        label = Plasma.Label(self)
        label.setText("Zemberek-server doesn't work..")
        self.layout.addItem(label)

        button = Plasma.PushButton(self)
        button.setText("Click to start service")
        self.layout.addItem(button)

        self.connect(button, SIGNAL("clicked()"), self.startService)

    def startService(self):
        link.System.Service['zemberek-server'].start()

class ZpSpellApplet(plasmascript.Applet):
    """ Our main applet derived from plasmascript.Applet """

    def __init__(self, parent, args=None):
        plasmascript.Applet.__init__(self, parent)

    def init(self):
        """ Const method for initializing the applet """

        # Try to connect dbus
        mkZpInterface()

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

        if not zpInterface:
            self.failWidget = FailedWidget(self.applet)
            self.layout.addItem(self.failWidget,0,0)
            link.listenSignals("System.Service", self.handler)
        else:
            self.initPlasmoid()

    def handler(self, package, signal, args):
        if package == 'zemberek_server':
            if args[1] in ['on','started','conditional_started']:
                systemBus.add_signal_receiver(self.dbusHandler, dbus_interface="org.freedesktop.DBus", member_keyword="signal")

    def dbusHandler(self, *args, **kwargs):
        if kwargs["signal"] == "NameOwnerChanged" and args[0] == "net.zemberekserver.server.dbus":
            mkZpInterface()
            self.failWidget.hide()
            self.layout.removeAt(0)
            self.initPlasmoid()

    def initPlasmoid(self):

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

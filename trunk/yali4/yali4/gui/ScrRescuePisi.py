# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import os
import dbus
import pisi
import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL, QEvent, QObject

import yali4.storage
from yali4.gui.installdata import *
from yali4.gui.GUIAdditional import DeviceItem
from yali4.gui.ScreenWidget import ScreenWidget
from yali4.gui.Ui.rescuepisiwidget import Ui_RescuePisiWidget
from yali4.gui.GUIException import GUIException
from yali4.gui.GUIAdditional import ConnectionWidget
import yali4.gui.context as ctx
import yali4.pisiiface

##
# BootLoader screen.
class Widget(QtGui.QWidget, ScreenWidget):
    title = _('Rescue Mode for Pisi History')
    desc = _('You can take back your system ...')
    icon = "iconInstall"
    help = _('''
<font size="+2">Pisi History</font>
<font size="+1"></font>
''')

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_RescuePisiWidget()
        self.ui.setupUi(self)

        self.connect(self.ui.buttonSelectConnection, SIGNAL("clicked()"), self.showConnections)

    def showConnections(self):
        connections = ConnectionWidget(self)
        connections.show()

    def fillHistoryList(self):
        ui = PisiUI()
        ctx.debugger.log("PisiUI is creating..")
        yali4.pisiiface.initialize(ui)
        history = yali4.pisiiface.getHistory()
        for hist in history:
            self.ui.historyList.addItem("%s - %s" % (hist.date, hist.type))

    def handler(self, *args):
        print args

    def shown(self):
        if not dbus.get_default_main_loop():
            from dbus.mainloop.qt import DBusQtMainLoop
            DBusQtMainLoop(set_as_default = True)
        self.fillHistoryList()

    def execute(self):
        return True

    def backCheck(self):
        ctx.mainScreen.moveInc = 2
        return True

class PisiUI(QObject, pisi.ui.UI):

    def __init__(self, *args):
        pisi.ui.UI.__init__(self)
        apply(QObject.__init__, (self,) + args)

    def notify(self, event, **keywords):
        print event

    def display_progress(self, operation, percent, info, **keywords):
        print operation, percent, info

class PisiEvent(QEvent):

    def __init__(self, _, event):
        QEvent.__init__(self, _)
        self.event = event

    def eventType(self):
        return self.event

    def setData(self,data):
        self._data = data

    def data(self):
        return self._data


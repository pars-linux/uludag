#!/usr/bin/python
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

import sys
import comar
import dbus

from PyQt4 import QtGui
from PyQt4.QtCore import *

from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

from about import aboutData
from mainwindow import MainManager

class Manager(KMainWindow):
    def __init__ (self, *args):
        KMainWindow.__init__(self)
        self.resize (640, 480)
        self.setCentralWidget(MainManager(self))

class ServiceManager(KCModule):
    def __init__(self, component_data, parent):
        KCModule.__init__(self, component_data, parent)

        DBusQtMainLoop(set_as_default = True)
        MainManager(self, standAlone = False)

def CreatePlugin(widget_parent, parent, component_data):
    return ServiceManager(component_data, parent)

if __name__ == '__main__':

    KCmdLineArgs.init(sys.argv, aboutData)
    app = KApplication()

    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default = True)

    mainWindow = Manager(None, 'history-manager')
    mainWindow.show()

    app.connect(app, SIGNAL('lastWindowClosed()'), app.quit)

    app.exec_()


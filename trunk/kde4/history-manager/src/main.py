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
from dbus.mainloop.qt import DBusQtMainLoop

from PyQt4 import QtGui
from PyQt4.QtCore import *

from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

from about import aboutData
from window import MainManager

class HistoryManager(KCModule):
    def __init__(self, component_data, parent):
        KCModule.__init__(self, component_data, parent)

        KGlobal.locale().insertCatalog("history-manager")

        DBusQtMainLoop(set_as_default=True)
        MainManager(self, standAlone=False)

class Manager(KMainWindow):
    def __init__(self, app):
        KMainWindow.__init__(self)

        KGlobal.locale().insertCatalog("history-manager")
        settings = QSettings()

        if settings.contains("pos") and settings.contains("size"):
            self.move(self.mapToGlobal(settings.value("pos").toPoint()))
            self.resize(settings.value("size").toSize())

        # self.resize(640, 480)
        self.setCentralWidget(MainManager(self, True, app))

def CreatePlugin(widget_parent, parent, component_data):
    return HistoryManager(component_data, parent)

if __name__ == '__main__':
    KCmdLineArgs.init(sys.argv, aboutData)
    app = KUniqueApplication()

    if not dbus.get_default_main_loop():
        DBusQtMainLoop(set_as_default = True)

    mainWindow = Manager(app)
    mainWindow.show()

    app.exec_()

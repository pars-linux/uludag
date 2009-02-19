#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# System
import sys

# Qt Stuff
from PyQt4 import QtGui
from PyQt4.QtCore import *

# PyKDE4 Stuff
from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

# Application Stuff
from about import aboutData

# Intefaces
from faces import MainManager

# Network Tools
import nettools

# DBus-Qt
from dbus.mainloop.qt import DBusQtMainLoop


class Manager(KMainWindow):
    def __init__ (self, *args):
        KMainWindow.__init__(self)
        self.resize(640, 480)
        self.setCentralWidget(MainManager(self))

class NetworkManager(KCModule):
    def __init__(self, component_data, parent):
        KCModule.__init__(self, component_data, parent)

        # DBus MainLoop
        DBusQtMainLoop(set_as_default=True)
        MainManager(self, standAlone=False)

def CreatePlugin(widget_parent, parent, component_data):
    return NetworkManager(component_data, parent)

if __name__ == '__main__':

    # Set Command-line arguments
    KCmdLineArgs.init(sys.argv, aboutData)

    # Create a Kapplitcation instance
    app = KApplication()

    # DBus MainLoop
    DBusQtMainLoop(set_as_default=True)

    # Create Main Widget
    mainWindow = Manager(None, 'network-manager')
    mainWindow.show()

    # Create connection for lastWindowClosed signal to quit app
    app.connect(app, SIGNAL('lastWindowClosed()'), app.quit)

    # Run the application
    app.exec_()


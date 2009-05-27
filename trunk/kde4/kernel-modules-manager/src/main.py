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

# System
import sys
import dbus

# Qt Stuff
from PyQt4 import QtGui
from PyQt4.QtCore import *

# PyKDE4 Stuff
from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

# Application Stuff
from about import aboutData

from modulemanager import ModuleManagerDlg

class Manager(KMainWindow):
    def __init__ (self, *args):
        KMainWindow.__init__(self)
        self.resize(330,505)
        self.setCentralWidget(ModuleManagerDlg(self))

if __name__ == '__main__':

    # Set Command-line arguments
    KCmdLineArgs.init(sys.argv, aboutData)

    # Create a Kapplitcation instance
    app = KApplication()

    # DBus MainLoop
    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default=True)

    # Create Main Widget
    mainWindow = Manager(None, 'kernel-modules-manager')
    mainWindow.show()

    # Create connection for lastWindowClosed signal to quit app
    app.connect(app, SIGNAL('lastWindowClosed()'), app.quit)

    # Run the application
    app.exec_()

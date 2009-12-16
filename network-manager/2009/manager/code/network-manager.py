#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2009, TUBITAK/UEKAE
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
from PyQt4.QtCore import SIGNAL

import dbus

# PyKDE4 Stuff
from PyKDE4.kdeui import KUniqueApplication
from PyKDE4.kdecore import KCmdLineArgs

def CreatePlugin(widget_parent, parent, component_data):
    from networkmanager.kcmodule import NetworkManager
    return NetworkManager(component_data, parent)

if __name__ == '__main__':

    # Network Manager
    from networkmanager.standalone import NetworkManager

    # Application Stuff
    from networkmanager.about import aboutData

    # Set Command-line arguments
    KCmdLineArgs.init(sys.argv, aboutData)

    # Create a Kapplitcation instance
    app = KUniqueApplication()

    # DBUS MainLoop
    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default = True)


    # Create Main Widget
    mainWindow = NetworkManager(app)
    mainWindow.show()

    # Create connection for lastWindowClosed signal to quit app
    app.connect(app, SIGNAL('lastWindowClosed()'), app.quit)

    # Run the application
    app.exec_()


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

# Qt Stuff
from PyQt4.QtCore import SIGNAL

# PyKDE4 Stuff
from PyKDE4.kdeui import *
from PyKDE4.kdecore import KCmdLineArgs
from PyKDE4.kdecore import KGlobal

from base import MainForm

class Pardusman(KMainWindow):
    def __init__ (self, app):
        KMainWindow.__init__(self)

        # This is very important for translations when running as kcm_module
        KGlobal.locale().insertCatalog("pardusman")

        self.resize(597, 421)
        self.setCentralWidget(MainForm(self, app))

if __name__ == '__main__':

    # Application Stuff
    from about import aboutData

    # DBUS-QT
    from dbus.mainloop.qt import DBusQtMainLoop

    # Set Command-line arguments
    KCmdLineArgs.init(sys.argv, aboutData)

    # Create a Kapplication instance
    app = KUniqueApplication()

    # DBUS MainLoop
    DBusQtMainLoop(set_as_default = True)

    # Create Main Widget
    mainWindow = Pardusman(app)
    mainWindow.show()

    # Create connection for lastWindowClosed signal to quit app
    app.connect(app, SIGNAL('lastWindowClosed()'), app.quit)

    # Run the application
    app.exec_()


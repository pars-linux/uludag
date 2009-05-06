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

# Qt
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QWidget

# PyKDE
from PyKDE4.kdeui import KApplication
from PyKDE4.kdecore import KCmdLineArgs

# About data
from about import aboutData

# Main form
from gui.main import MainWindow


def gui(args):
    # Application name
    app_name = args[0]

    # Set command-line arguments
    KCmdLineArgs.init(args, aboutData)

    # Create applicatin
    app = KApplication()

    # Show main window
    mainWindow = MainWindow(app_name)
    mainWindow.show()

    app.setTopWidget(mainWindow)

    # Close application if there's no window
    app.connect(app, SIGNAL('lastWindowClosed()'), app.quit)

    # Go go go!
    app.exec_()

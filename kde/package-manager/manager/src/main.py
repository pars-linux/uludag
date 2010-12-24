#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009-2010, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# Python Imports
import sys
import dbus
import signal
import traceback

# PyQt4 Imports
from PyQt4.QtGui import QApplication

# PyKDE4 Imports
from PyKDE4.kdeui import KUniqueApplication
from PyKDE4.kdeui import KApplication
from PyKDE4.kdecore import KCmdLineArgs
from PyKDE4.kdecore import ki18n
from PyKDE4.kdecore import KCmdLineOptions

# Package Manager Specific Imports
import config
from about import aboutData
from pmlogging import logger
from mainwindow import MainWindow
from localedata import setSystemLocale
from pmutils import handleException

# Package Manager Main App
if __name__ == '__main__':

    # Catch signals
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Create a dbus mainloop if its not exists
    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default = True)

    # Use raster to make it faster
    QApplication.setGraphicsSystem('raster')

    # Initialize Command Line arguments from sys.argv
    KCmdLineArgs.init(sys.argv, aboutData)

    # Add Command Line options
    options = KCmdLineOptions()
    options.add("show-mainwindow", ki18n("Show main window"))
    KCmdLineArgs.addCmdLineOptions(options)

    # Create a unique KDE Application
    app = KUniqueApplication(True, True)

    # Set system Locale, we may not need it anymore
    # It should set just before MainWindow call
    setSystemLocale()

    # Create MainWindow
    manager = MainWindow()

    # Check if show-mainwindow used in sys.args to show mainWindow
    args = KCmdLineArgs.parsedArgs()
    if args.isSet("show-mainwindow"):
        manager.show()

    # If system tray disabled show mainwindow at first
    if not config.PMConfig().systemTray():
        manager.show()

    # Set exception handler
    sys.excepthook = handleException

    # Run the Package Manager
    app.exec_()


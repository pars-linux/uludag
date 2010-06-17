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

# PyKDE4 Imports
from PyKDE4.kdeui import KUniqueApplication, KApplication
from PyKDE4.kdecore import KCmdLineArgs, ki18n, KCmdLineOptions
from mainwindow_kde4 import MainWindow

# Package Manager Specific Imports
from about import aboutData
from pmlogging import logger
from localedata import setSystemLocale

def handleException(exception, value, tb):
    """
    Exception Handler

    @param exception: exception object
    @param value: exception message
    @param tb: traceback log 
    """
    logger.error("".join(traceback.format_exception(exception, value, tb)))

# Package Manager Main App
if __name__ == '__main__':

    # Catch signals
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Create a dbus mainloop if its not exists
    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default = True)

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

    # Set exception handler
    sys.excepthook = handleException

    # Run the Package Manager
    app.exec_()


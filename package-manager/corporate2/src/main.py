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
from optparse import OptionParser

# PyQt4 Imports
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QApplication
from pds.quniqueapp import QUniqueApplication

# Package Manager Specific Imports
import config
import backend

from pmlogging import logger
from mainwindow import MainWindow
from localedata import setSystemLocale

from pmutils import *

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

    pid = os.fork()
    if pid:
        os._exit(0)

    app = QUniqueApplication(sys.argv, catalog='package-manager')
    setSystemLocale()

    # Set application font from system
    font = Pds.settings('font','Sans,10').split(',')
    app.setFont(QFont(font[0], int(font[1])))

    manager = MainWindow(app)
    app.setMainWindow(manager)

    if config.PMConfig().systemTray():
        app.setQuitOnLastWindowClosed(False)

    # Arrange arguments
    parser = OptionParser()
    parser.add_option("--show-mainwindow",
                      action="store_false",
                      help="Show main window.")
    parser.add_option("--add-repository",
                      help="Add repository. Needs argument.")

    opts, args = parser.parse_args()

    if not config.PMConfig().systemTray() or not opts.show_mainwindow is None:
        # Show the mainwindow if user wants
        manager.show()

    if not opts.add_repository is None:
        # Check add repo options and then open repository settings dialog
        repoAddress = checkRepoDirectory(opts.add_repository)
        if repoAddress:
            manager.show()
            manager.showPreferences.trigger()
            manager.settingsDialog.tabWidget.setCurrentIndex(2)
            manager.settingsDialog.addRepoButton.click()
            manager.settingsDialog.repositorySettings.fillRepoDialog(repoAddress)

    # Set exception handler
    sys.excepthook = handleException

    # Run the Package Manager
    app.exec_()

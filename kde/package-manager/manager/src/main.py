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

import os
import sys
import traceback
import context as ctx

from PyQt4 import QtGui
from PyQt4.QtCore import *

import dbus

from localedata import setSystemLocale
from pmlogging import logger
import config
import signal

if ctx.Pds.session == ctx.pds.Kde4:
    from PyKDE4.kdeui import KUniqueApplication, KApplication
    from PyKDE4.kdecore import KCmdLineArgs, ki18n, KCmdLineOptions
    from about import aboutData
else:
    from pds.quniqueapp import QUniqueApplication

def handleException(exception, value, tb):
    logger.error("".join(traceback.format_exception(exception, value, tb)))

if __name__ == '__main__':
    setSystemLocale()

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default = True)

    from optparse import OptionParser

    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-i", "--install-package", dest="install_package",
                      action="store_true", default=False,
                      help="packages to install")

    (options, args) = parser.parse_args()
    if options.install_package:

        from mainwindow import MainWindow
        if ctx.Pds.session == ctx.pds.Kde4:
            KCmdLineArgs.init([], aboutData)
            app = KApplication()
        else:
            app = QtGui.QApplication(sys.argv)
            font = ctx.Pds.settings('font','Dejavu Sans,10').split(',')
            app.setFont(QtGui.QFont(font[0], int(font[1])))

        setSystemLocale()
        manager = MainWindow(app, silence = True)

        manager.centralWidget().state.operationAction(args, silence = True)
        manager.centralWidget().progressDialog.show()

    else:
        if ctx.Pds.session == ctx.pds.Kde4:
            from mainwindow_kde4 import MainWindow

            KCmdLineArgs.init(sys.argv, aboutData)
            options = KCmdLineOptions()
            options.add("show-mainwindow", ki18n("Show main window"))
            KCmdLineArgs.addCmdLineOptions(options)

            app = KUniqueApplication(True, True)

            # It should set just before MainWindow call
            setSystemLocale()

            manager = MainWindow()
            args = KCmdLineArgs.parsedArgs()
            if args.isSet("show-mainwindow"):
                manager.show()

        else:
            from mainwindow import MainWindow

            pid = os.fork()
            if pid:
                os._exit(0)

            app = QUniqueApplication(sys.argv, catalog='package-manager')

            setSystemLocale()

            manager = MainWindow(app)
            app.setMainWindow(manager)

            # Set application font from system
            font = ctx.Pds.settings('font','Dejavu Sans,10').split(',')
            app.setFont(QtGui.QFont(font[0], int(font[1])))

            if config.PMConfig().systemTray():
                app.setQuitOnLastWindowClosed(False)

        if not config.PMConfig().systemTray():
            manager.show()

    sys.excepthook = handleException
    ctx._time()
    app.exec_()

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
import traceback
import context as ctx

from PyQt4 import QtGui
from PyQt4.QtCore import *

import dbus

from mainwindow import MainWindow
from localedata import setSystemLocale
from pmlogging import logger
# import config

def handleException(exception, value, tb):
    logger.error("".join(traceback.format_exception(exception, value, tb)))

if __name__ == '__main__':

    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default = True)

    if ctx.Pds.session == ctx.pds.Kde4:
        from PyKDE4.kdeui import KUniqueApplication
        from PyKDE4.kdecore import KCmdLineArgs, ki18n, KCmdLineOptions

        from about import aboutData

        KCmdLineArgs.init(sys.argv, aboutData)
        options = KCmdLineOptions()
        options.add("show-mainwindow", ki18n("Show main window"))
        KCmdLineArgs.addCmdLineOptions(options)

        app = KUniqueApplication(True, True)
        manager = MainWindow()
        args = KCmdLineArgs.parsedArgs()

        #if not config.PMConfig().systemTray():
        manager.show()
        #else:
        #    if args.isSet("show-mainwindow"):
        #        manager.show()

        sys.excepthook = handleException
        setSystemLocale()
    else:
        app = QtGui.QApplication(sys.argv)
        manager = MainWindow()
        manager.show()

    app.exec_()

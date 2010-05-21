#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009-2010 TUBITAK/UEKAE
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
    from PyKDE4.kdeui import KApplication
    from PyKDE4.kdecore import KCmdLineArgs
    from about import aboutData

def handleException(exception, value, tb):
    logger.error("".join(traceback.format_exception(exception, value, tb)))

if __name__ == '__main__':
    setSystemLocale()

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default = True)

    from optparse import OptionParser

    usage = ctx.Pds.i18n("%prog packages_to_install")
    parser = OptionParser(usage=usage)
    args = filter(lambda x: not x.startswith('-'), sys.argv[1:])
    if len(sys.argv) > 1:

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

        manager.centralWidget().state._selected_packages = args
        manager.centralWidget().state.operationAction(args, silence = True)
        manager.centralWidget().progressDialog.show()

        sys.excepthook = handleException
        ctx._time()
        app.exec_()
    else:
        parser.print_usage()


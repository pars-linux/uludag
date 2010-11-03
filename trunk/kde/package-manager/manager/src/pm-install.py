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
from PyQt4.QtGui import QDesktopWidget
from PyQt4.QtCore import *

import dbus

from localedata import setSystemLocale
from pmlogging import logger
import config
import signal

from PyKDE4.kdecore import i18n
from PyKDE4.kdecore import KCmdLineArgs
from PyKDE4.kdeui import KUniqueApplication

from mainwindow import MainWindow
from about import aboutData

def handleException(exception, value, tb):
    """
    Exception Handler

    @param exception: exception object
    @param value: exception message
    @param tb: traceback log
    """
    logger.error("".join(traceback.format_exception(exception, value, tb)))

if __name__ == '__main__':
    setSystemLocale()

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default = True)

    from optparse import OptionParser

    usage = unicode(i18n("%prog packages_to_install"))
    parser = OptionParser(usage=usage)
    args = filter(lambda x: not x.startswith('-'), sys.argv[1:])

    if len(sys.argv) > 1:

        aboutData.setAppName("pm-install")
        KCmdLineArgs.init([], aboutData)

        app = KUniqueApplication(True, True)
        setSystemLocale()

        manager = MainWindow(silence = True)
        manager.statusBar().hide()
        manager.resize(QSize(600, 90))
        manager.move(QDesktopWidget().screenGeometry(manager).center() - manager.rect().center())

        cw = manager.centralWidget()
        cw.state.state = cw.state.INSTALL
        cw.state._selected_packages = args
        cw.state.operationAction(cw.state._selected_packages, silence = True)

        sys.excepthook = handleException
        ctx._time()
        app.exec_()
    else:
        parser.print_usage()


#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import sys
import dbus

from PyQt4 import QtGui
from PyQt4 import QtCore

from PyKDE4.kdeui import KUniqueApplication
from PyKDE4.kdecore import KCmdLineArgs

from maindialog import MainDialog
from about import aboutData
from dumlogging import logger

def handleException(exception, value, tb):
    logger.error("".join(traceback.format_exception(exception, value, tb)))

if __name__ == '__main__':

    KCmdLineArgs.init(sys.argv, aboutData)

    app = KUniqueApplication(True, True)
    args = KCmdLineArgs.parsedArgs()

    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default = True)

    manager = MainDialog()
    manager.show()

    sys.excepthook = handleException

    app.exec_()

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
import dbus
import signal
import traceback
from optparse import OptionParser

# PyQt4 Imports
from PyQt4.QtCore import *
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QApplication

from pds.quniqueapp import QUniqueApplication

from pmlogging import logger
from pmwindow import UmWindow
from localedata import setSystemLocale

from pmutils import *

if __name__ == '__main__':
    # Catch signals
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Create a dbus mainloop if its not exists
    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default = True)

    # Use raster to make it faster
    QApplication.setGraphicsSystem('raster')

    app = QUniqueApplication(sys.argv, catalog='upgrade-manager')
    setSystemLocale()

    # Set application font from system
    font = Pds.settings('font','Sans,10').split(',')
    app.setFont(QFont(font[0], int(font[1])))

    window = UmWindow(app)
    window.show()

    app.exec_()

    sys.exit(0)


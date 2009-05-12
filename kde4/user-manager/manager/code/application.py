#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import sys

from PyQt4 import QtGui
from PyQt4 import QtCore

from PyKDE4.kdeui import KMainWindow, KApplication
from PyKDE4.kdecore import KCmdLineArgs

from about import aboutData
from main import MainWidget

class MainWindow(KMainWindow):
    def __init__(self, parent=None):
        KMainWindow.__init__(self, parent)
        widget = MainWidget(self)
        self.resize(widget.size())
        self.setCentralWidget(widget)

if __name__ == "__main__":

    KCmdLineArgs.init(sys.argv, aboutData)
    app = KApplication()

    from dbus.mainloop.qt import DBusQtMainLoop
    DBusQtMainLoop(set_as_default=True)

    window = MainWindow()
    window.show()

    app.exec_()

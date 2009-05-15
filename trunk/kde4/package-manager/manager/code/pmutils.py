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

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QEventLoop

def waitCursor():
    QtGui.QApplication.setOverrideCursor(QtGui.QCursor(Qt.WaitCursor))

def restoreCursor():
    QtGui.QApplication.restoreOverrideCursor()

def processEvents():
    QtGui.QApplication.processEvents()

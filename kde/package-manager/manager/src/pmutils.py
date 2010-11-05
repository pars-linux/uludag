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
import unicodedata

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QEventLoop

from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import SLOT
from PyQt4.QtCore import QThread

class PThread(QThread):
    def __init__(self, parent, action, callback, args=[], kwargs={}):
        QThread.__init__(self,parent)

        parent.connect(self, SIGNAL("finished()"), callback)

        self.action = action
        self.args = args
        self.kwargs = kwargs
        self.callback = callback
        self.data = None

    def run(self):
        try:
            self.data = self.action(*self.args, **self.kwargs)
        finally:
            self.connect(self.parent(), SIGNAL("cleanUp()"), SLOT("deleteLater()"))

    def cleanUp(self):
        self.deleteLater()

    def get(self):
        return self.data

def waitCursor():
    QtGui.QApplication.setOverrideCursor(QtGui.QCursor(Qt.WaitCursor))

def restoreCursor():
    # According to the Qt Documentation it should be called twice to reset 
    # cursor to the default if one use waitCursor twice.
    QtGui.QApplication.restoreOverrideCursor()
    QtGui.QApplication.restoreOverrideCursor()

def processEvents():
    QtGui.QApplication.processEvents()

def humanReadableSize(size, precision=".1"):
    symbols, depth = [' B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'], 0

    while size > 1000 and depth < 8:
        size = float(size / 1024)
        depth += 1

    if size == 0:
        return "0 B"

    fmt = "%%%sf %%s" % precision
    return fmt % (size, symbols[depth])

# Python regex sucks
# http://mail.python.org/pipermail/python-list/2009-January/523704.html
def letters():
    start = end = None
    result = []
    for index in xrange(sys.maxunicode + 1):
        c = unichr(index)
        if unicodedata.category(c)[0] == 'L':
            if start is None:
                start = end = c
            else:
                end = c
        elif start:
            if start == end:
                result.append(start)
            else:
                result.append(start + "-" + end)
            start = None
    return ''.join(result)

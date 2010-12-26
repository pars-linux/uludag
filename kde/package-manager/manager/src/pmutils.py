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
import urllib
import unicodedata

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QEventLoop

from PyKDE4.solid import Solid

def waitCursor():
    QtGui.QApplication.setOverrideCursor(QtGui.QCursor(Qt.WaitCursor))

def restoreCursor():
    # According to the Qt Documentation it should be called twice to reset 
    # cursor to the default if one use waitCursor twice.
    QtGui.QApplication.restoreOverrideCursor()
    QtGui.QApplication.restoreOverrideCursor()

def processEvents():
    QtGui.QApplication.processEvents()

def isSolidOnline():
    return Solid.Networking.status() == Solid.Networking.Connected

def network_available():
    try:
        urllib.urlopen('http://packages.pardus.org.tr')
    except:
        return False
    return True

def handleException(exception, value, tb):
    """
    Exception Handler

    @param exception: exception object
    @param value: exception message
    @param tb: traceback log
    """
    logger.error("".join(traceback.format_exception(exception, value, tb)))

def humanReadableSize(size, precision=".1"):
    if not size:
        return 'N/A'

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

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

# Qt Stuff
from PyQt4 import QtGui
from PyQt4.QtCore import *

DEFAULT_HEIGHT = 72
MAX_HEIGHT = DEFAULT_HEIGHT * 3
(UP, DOWN) = range(2)

class RowAnimator(object):
    def __init__(self, updater=None):
        self.height = DEFAULT_HEIGHT
        self.direction = DOWN
        self.row = None
        self.timeLine = QTimeLine(250)
        self.timeLine.setUpdateInterval(40)
        QObject.connect(self.timeLine, SIGNAL("valueChanged(qreal)"), updater)
        QObject.connect(self.timeLine, SIGNAL("finished()"), self.finished)

    def animate(self, row):
        self.setRow(row)
        self.timeLine.start()

    def reset(self, row=None):
        self.timeLine.stop()
        self.timeLine.setCurrentTime(0)
        self.row = row
        self.height = DEFAULT_HEIGHT
        self.direction = DOWN

    def finished(self):
        if self.direction == DOWN:
            self.direction = UP
            self.height = MAX_HEIGHT
        else:
            self.direction = DOWN
            self.height = DEFAULT_HEIGHT

    def size(self):
        if self.running():
            self.updateSize()
        return QSize(0, self.height)

    def setRow(self, row):
        if self.row != row:
            self.reset(row)

    def currentRow(self):
        return self.row

    def running(self):
        return self.timeLine.state() == QTimeLine.Running

    def updateSize(self):
        if self.direction == DOWN:
            self.height += 25
            if self.height > MAX_HEIGHT:
                self.height = MAX_HEIGHT
        else:
            self.height -= 25
            if self.height < DEFAULT_HEIGHT:
                self.height = DEFAULT_HEIGHT

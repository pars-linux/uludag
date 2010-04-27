#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009-2010, TUBITAK/UEKAE
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

DEFAULT_HEIGHT = 52
MAX_HEIGHT = DEFAULT_HEIGHT * 3
(UP, DOWN) = range(2)

class HoverLinkFilter(QObject):
    def __init__(self, parent):
        QObject.__init__(self)
        self.link_rect = QRect()
        self.parent = parent

    def eventFilter(self, obj, event):
        if event.type() == QEvent.HoverMove and self.parent.direction == UP:
            if self.link_rect.contains(event.pos()):
                obj.setCursor(Qt.PointingHandCursor)
            else:
                obj.unsetCursor()
            return True
        return QObject.eventFilter(self, obj, event)

class RowAnimator(object):
    def __init__(self, updater=None):
        self.height = DEFAULT_HEIGHT
        self.max_height = DEFAULT_HEIGHT * 3
        self.direction = DOWN
        self.row = None
        self.lastrow = None
        self.timeLine = QTimeLine(250)
        self.timeLine.setUpdateInterval(40)
        self.t_view = updater
        QObject.connect(self.timeLine, SIGNAL("valueChanged(qreal)"), self.size)
        QObject.connect(self.timeLine, SIGNAL("finished()"), self.finished)

        self.hoverLinkFilter = HoverLinkFilter(self)
        self.t_view.installEventFilter(self.hoverLinkFilter)

    def animate(self, row):
        self.setRow(row)
        self.timeLine.start()

    def reset(self, row=None):
        self.timeLine.stop()
        self.timeLine.setCurrentTime(0)
        self.height = DEFAULT_HEIGHT
        if self.row >= 0:
            self.t_view.setRowHeight(self.row, self.height)
        self.direction = DOWN
        self.row = row

    def finished(self):
        if self.direction == DOWN:
            self.direction = UP
            self.height = self.max_height
        else:
            self.direction = DOWN
            self.height = DEFAULT_HEIGHT
        self.t_view.setRowHeight(self.row, self.height)

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
            if self.height > self.max_height:
                self.height = self.max_height
        else:
            self.height -= 25
            if self.height < DEFAULT_HEIGHT:
                self.height = DEFAULT_HEIGHT
        self.t_view.setRowHeight(self.row, self.height)

#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pardus Desktop Services
# GUI Module ~ gui.py

# Copyright (C) 2010, TUBITAK/UEKAE
# 2010 - Gökmen Göksel <gokmen:pardus.org.tr>

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

# Qt Libraries
from PyQt4 import QtGui
from PyQt4 import QtCore

# PREDEFINED POSITIONS
# --------------------
TOPLEFT = 1
TOPCENTER = 2
TOPRIGHT = 3
MIDLEFT = 4
MIDCENTER = 5
MIDRIGHT = 6
BOTLEFT = 7
BOTCENTER = 8
BOTRIGHT = 9
# --------------------
FORWARD = QtCore.QTimeLine.Forward
BACKWARD = QtCore.QTimeLine.Backward
# --------------------
IN = 0
OUT = 1
# --------------------

# STYLE SHEET
STYLE = """
  background-color:rgba(0,0,0,120);
  color:white;
  border: 1px solid #FFF;
  border-radius: 4px;
"""


class PAbstractBox(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.sceneX = QtCore.QTimeLine()
        self.sceneY = QtCore.QTimeLine()
        self.animation = 38

    def animate(self, direction = IN, move_direction = FORWARD, start = TOPCENTER, stop = BOTCENTER):
        if not self.sceneX.state() == QtCore.QTimeLine.NotRunning:
            return

        self.sceneX.setDirection(move_direction)
        self.sceneX.setEasingCurve(QtCore.QEasingCurve(self.animation))
        self.sceneX.setDuration(2000)
        self.sceneX.setUpdateInterval(20)

        self.sceneY.setDirection(move_direction)
        self.sceneY.setEasingCurve(QtCore.QEasingCurve(self.animation))
        self.sceneY.setDuration(2000)
        self.sceneY.setUpdateInterval(20)

        p_width  = self.parent.width()
        p_height = self.parent.height()
        width  = self.width()
        height = self.height()

        range = {TOPLEFT   : [0, 0],
                 TOPCENTER : [p_width/2 - width/2, 0],
                 TOPRIGHT  : [p_width - width, 0],
                 MIDLEFT   : [0, p_height/2 - height/2],
                 MIDCENTER : [p_width/2 - width/2, p_height/2 - height/2],
                 MIDRIGHT  : [p_width - width, p_height/2 - height/2],
                 BOTLEFT   : [0, p_height - height],
                 BOTCENTER : [p_width/2 - width/2, p_height - height],
                 BOTRIGHT  : [p_width - width, p_height - height]}

        start_pos = range[start]
        stop_pos  = range[stop]

        # Poor developer's debug mechanism.
        # print start_pos, stop_pos, width, height

        if direction == IN:
            self.show()
            if start in (TOPLEFT, MIDLEFT, BOTLEFT):
                start_pos[0] -= width
            elif start in (TOPRIGHT, MIDRIGHT, BOTRIGHT):
                start_pos[0] += width
            elif start == TOPCENTER:
                start_pos[1] -= height
            elif start == BOTCENTER:
                start_pos[1] += height
        elif direction == OUT:
            if stop in (TOPLEFT, MIDLEFT, BOTLEFT):
                stop_pos[0] -= width
            elif stop in (TOPRIGHT, MIDRIGHT, BOTRIGHT):
                stop_pos[0] += width
            elif stop == TOPCENTER:
                stop_pos[1] -= height
            elif stop == BOTCENTER:
                stop_pos[1] += height

        self.move(start_pos[0], start_pos[1])

        self.sceneX.setFrameRange(start_pos[0], stop_pos[0])
        self.sceneX.frameChanged.connect(lambda x: self.move(x, self.y()))
        self.sceneX.finished.connect(lambda: self.setHidden(direction == OUT))

        self.sceneY.setFrameRange(start_pos[1], stop_pos[1])
        self.sceneY.frameChanged.connect(lambda y: self.move(self.x(), y))

        self.sceneX.start()
        self.sceneY.start()


class PInfoBox(PAbstractBox):
    def __init__(self, parent=None):
        PAbstractBox.__init__(self, parent)
        self.label = QtGui.QLabel('Hello World !', self)


class PMessageBox(PAbstractBox):
    def __init__(self, parent=None):
        PAbstractBox.__init__(self, parent)
        self.label = QtGui.QLabel(self)
        self.setStyleSheet(STYLE)
        self.padding_w = 14
        self.padding_h = 8
        self.hide()

    def showMessage(self, message, duration = 2, inPos = TOPCENTER, stopPos = MIDCENTER, outPos = BOTCENTER):
        self.setMessage(message)
        self.animate(start = inPos, stop = stopPos)
        QtCore.QTimer.singleShot((2+duration) * 1000, lambda: self.animate(start = stopPos, stop = outPos, direction = OUT))

    def setMessage(self, message):
        self.label.setText(message)
        self.label.setAlignment(QtCore.Qt.AlignVCenter)
        metric = self.label.fontMetrics()
        self.label.resize(metric.width(message) + self.padding_w, metric.height() + self.padding_h)
        self.resize(metric.width(message) + self.padding_w, metric.height() + self.padding_h)


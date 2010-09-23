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
(TOPLEFT, TOPCENTER, TOPRIGHT, \
 MIDLEFT, MIDCENTER, MIDRIGHT, \
 BOTLEFT, BOTCENTER, BOTRIGHT,
 CURRENT) = range(10)
# --------------------
FORWARD = QtCore.QTimeLine.Forward
BACKWARD = QtCore.QTimeLine.Backward
# --------------------
(IN, OUT, RESIZE) = range(3)
# --------------------
OVERLAY_OPACITY = 200

class PAbstractBox(QtGui.QWidget):
    def __init__(self, parent):
        self.overlay = QtGui.QWidget(parent)
        self.overlay.hide()
        self.__overlay_enabled = False
        QtGui.QWidget.__init__(self, parent)

        self.last_direction = IN
        self.last_move_direction = FORWARD
        self.last_start = TOPCENTER
        self.last_stop = BOTCENTER
        self.duration = 2000

        self.parent = parent
        self.parent.resizeEvent = self.resizeCallBacks
        self.sceneX = QtCore.QTimeLine()
        self.sceneY = QtCore.QTimeLine()
        self.sceneF = QtCore.QTimeLine()
        self.animation = 30
        self.call_back_functions = {IN:[], OUT:[], RESIZE:[]}

        self.registerFunction(RESIZE, lambda: '')
        self.registerFunction(OUT, lambda: self.flushCallBacks(RESIZE))
        self.registerFunction(OUT, lambda: self.registerFunction(RESIZE, lambda: ''))

    def flushCallBacks(self, direction):
        self.call_back_functions[direction] = []

    def enableOverlay(self, animated = False):
        self.overlay.resize(self.parent.size())
        self.__overlay_enabled = True
        self.sceneF.setUpdateInterval(20)
        self.registerFunction(IN,  self.sceneF.stop)
        if animated:
            self.sceneF.setFrameRange(0, 200)
            self.sceneF.frameChanged.connect(lambda x: self.overlay.setStyleSheet('background-color: rgba(0,0,0,%s)' % x))
            self.registerFunction(IN,  lambda: self.sceneF.setFrameRange(200, 0))
            self.registerFunction(OUT, lambda: self.sceneF.setFrameRange(0, 200))
        else:
            self.overlay.setStyleSheet('background-color: rgba(0, 0, 0, %s)' % OVERLAY_OPACITY)

        self.registerFunction(RESIZE, lambda: self.overlay.resize(self.parent.size()))
        self.registerFunction(RESIZE, lambda: '')

    def disableOverlay(self):
        self.__overlay_enabled = False

    def resizeCallBacks(self, event):
        QtGui.QWidget(self.parent).resizeEvent(event)
        self.runCallBacks(RESIZE)

    def animate(self, direction = IN, move_direction = FORWARD, start = TOPCENTER, stop = BOTCENTER, start_after = None, duration = 0):
        if start_after:
            start_after.finished.connect(lambda: self.__animate(direction, move_direction, start, stop, duration))
        else:
            return self.__animate(direction, move_direction, start, stop, duration)

    def __animate(self, direction, move_direction, start, stop, duration):

        self.sceneX.stop()
        self.sceneY.stop()
        self.sceneF.stop()

        duration = duration if duration > 0 else self.duration

        self.call_back_functions[RESIZE].pop()
        self.registerFunction(RESIZE, lambda: self.animate(self.last_direction,
                                                           self.last_move_direction,
                                                           CURRENT,
                                                           self.last_stop))

        self.last_stop           = stop
        self.last_start          = start
        self.last_move_direction = move_direction
        self.last_direction      = direction

        self.sceneX.setDirection(move_direction)
        self.sceneX.setEasingCurve(QtCore.QEasingCurve(self.animation))
        self.sceneX.setDuration(duration)
        self.sceneX.setUpdateInterval(20)

        self.sceneY.setDirection(move_direction)
        self.sceneY.setEasingCurve(QtCore.QEasingCurve(self.animation))
        self.sceneY.setDuration(duration)
        self.sceneY.setUpdateInterval(20)
        self.sceneF.setDuration(duration)

        p_width  = self.parent.width()
        p_height = self.parent.height()
        width  = self.width()
        height = self.height()

        limits = {TOPLEFT   : [0, 0],
                  TOPCENTER : [p_width/2 - width/2, 0],
                  TOPRIGHT  : [p_width - width, 0],
                  MIDLEFT   : [0, p_height/2 - height/2],
                  MIDCENTER : [p_width/2 - width/2, p_height/2 - height/2],
                  MIDRIGHT  : [p_width - width, p_height/2 - height/2],
                  BOTLEFT   : [0, p_height - height],
                  BOTCENTER : [p_width/2 - width/2, p_height - height],
                  BOTRIGHT  : [p_width - width, p_height - height],
                  CURRENT   : [self.x(), self.y()]}

        start_pos = limits[start]
        stop_pos  = limits[stop]

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
        self.sceneX.finished.connect(lambda: self.runCallBacks(direction))

        self.sceneY.setFrameRange(start_pos[1], stop_pos[1])
        self.sceneY.frameChanged.connect(lambda y: self.move(self.x(), y))

        if self.__overlay_enabled:
            self.overlay.show()
            self.sceneX.finished.connect(lambda: self.overlay.setHidden(direction == OUT))
        else:
            self.overlay.hide()

        if self.sceneX.state() == QtCore.QTimeLine.NotRunning:
            self.sceneX.start()
            self.sceneY.start()
            if not start == CURRENT:
                self.sceneF.start()

        return self.sceneX

    def registerFunction(self, direction, func):
        if not func in self.call_back_functions[direction]:
            self.call_back_functions[direction].append(func)

    def runCallBacks(self, direction):
        for func in self.call_back_functions[direction]:
            func()

class PWidgetbox(PAbstractBox):
    def __init__(self, parent, widget):
        PAbstractBox.__init__(self, parent)

class PInfoBox(PAbstractBox):
    def __init__(self, parent=None):
        PAbstractBox.__init__(self, parent)
        self.label = QtGui.QLabel('Hello World !', self)

class PMessageBox(PAbstractBox):

    # STYLE SHEET
    STYLE = """background-color:rgba(0,0,0,120);
               color:white;
               border: 1px solid #FFF;
               border-radius: 4px;"""

    def __init__(self, parent=None):
        PAbstractBox.__init__(self, parent)
        self.label = QtGui.QLabel(self)
        self.setStyleSheet(PMessageBox.STYLE)
        self.padding_w = 14
        self.padding_h = 8
        self.hide()

    def showMessage(self, message, duration = 2, inPos = MIDLEFT, stopPos = MIDCENTER, outPos = MIDRIGHT):
        self.setMessage(message)
        self.enableOverlay(animated = True)
        obj = self.animate(start = inPos, stop = stopPos)
        self.animate(start = stopPos, stop = outPos, direction = OUT, start_after = obj)

    def setMessage(self, message):
        self.label.setText(message)
        self.label.setAlignment(QtCore.Qt.AlignVCenter)
        metric = self.label.fontMetrics()
        self.label.resize(metric.width(message) + self.padding_w, metric.height() + self.padding_h)
        self.resize(metric.width(message) + self.padding_w, metric.height() + self.padding_h)


#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

from PyQt4 import QtCore, QtGui
from pds.gui import *

class PWidgetbox(PAbstractBox):
    def __init__(self, parent, widget):
        PAbstractBox.__init__(self, parent)
        ui = widget()
        ui.setupUi(self)
        self.enableOverlay(True)

    def showAnimated(self):
        self.animate(start = TOPCENTER, stop = TOPCENTER)

    def hideAnimated(self):
        self.animate(start = CURRENT, stop = MIDRIGHT, direction = OUT)

class PMessageBox(PAbstractBox):

    # STYLE SHEET
    STYLE = """background-color:rgba(0,0,0,120);
               color:white;
               border: 1px solid #999;
               border-radius: 4px;"""

    OUT_POS  = MIDRIGHT
    IN_POS   = MIDCENTER
    STOP_POS = MIDCENTER

    def __init__(self, parent=None):
        PAbstractBox.__init__(self, parent)
        self.label = QtGui.QLabel(self)
        self.setStyleSheet(PMessageBox.STYLE)
        self.padding_w = 22
        self.padding_h = 16
        self.animation = 1
        self.duration = 400
        self.last_msg = None
        self.enableOverlay()
        self.hide()

    def showMessage(self, message):
        self.setMessage(message)
        self.last_msg = self.animate(start = PMessageBox.IN_POS, stop = PMessageBox.STOP_POS)

    def hideMessage(self):
        self.animate(start = PMessageBox.STOP_POS,
                     stop  = PMessageBox.OUT_POS,
                     start_after = self.last_msg,
                     direction = OUT)

    def setMessage(self, message):
        self.label.setText(message)
        self.label.setAlignment(QtCore.Qt.AlignVCenter)
        metric = self.label.fontMetrics()
        self.label.resize(metric.width(message) + self.padding_w, metric.height() + self.padding_h)
        self.resize(metric.width(message) + self.padding_w, metric.height() + self.padding_h)


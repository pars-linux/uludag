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
from ui_message import Ui_MessageBox

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
    STYLE = """color:white;font-size:16pt;"""
    OUT_POS  = MIDCENTER
    IN_POS   = MIDCENTER
    STOP_POS = MIDCENTER

    def __init__(self, parent):
        PAbstractBox.__init__(self, parent)
        self.ui = Ui_MessageBox()
        self.ui.setupUi(self)
        self.animation = 1
        self.duration = 100
        self.last_msg = None
        self.setStyleSheet(PMessageBox.STYLE)
        self.registerFunction(FINISHED, QtGui.qApp.processEvents)
        self.enableOverlay()
        self.hide()

    def showMessage(self, message, icon = None):
        self.ui.label.setText(message)
        if icon:
            self.ui.icon.setPixmap(QtGui.QPixmap(icon))
            self.ui.icon.show()
        else:
            self.ui.icon.hide()
        self.last_msg = self.animate(start = PMessageBox.IN_POS, stop = PMessageBox.STOP_POS)
        QtGui.qApp.processEvents()

    def hideMessage(self):
        if self.isVisible():
            self.animate(start = PMessageBox.STOP_POS,
                         stop  = PMessageBox.OUT_POS,
                         start_after = self.last_msg,
                         direction = OUT)


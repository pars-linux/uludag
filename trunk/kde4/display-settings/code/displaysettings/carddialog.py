#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# PyQt
from PyQt4 import QtCore
from PyQt4 import QtGui

# PyKDE
from PyKDE4 import kdeui
from PyKDE4 import kdecore

# UI
from displaysettings.ui_videocard import Ui_VideoCardDialog

class VideoCardDialog(QtGui.QDialog, Ui_VideoCardDialog):

    configChanged = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

        if parent:
            self.configChanged.connect(parent.configChanged)

    def show(self):
        print "-- show"
        QtGui.QDialog.show(self)

    def accept(self):
        print "-- accept"
        self.configChanged.emit()
        QtGui.QDialog.accept(self)

    def reject(self):
        print "-- reject"
        QtGui.QDialog.reject(self)

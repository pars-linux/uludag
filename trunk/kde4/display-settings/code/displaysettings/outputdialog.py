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
from displaysettings.ui_output import Ui_OutputDialog

class OutputDialog(QtGui.QDialog, Ui_OutputDialog):

    configChanged = QtCore.pyqtSignal()

    def __init__(self, parent, iface, output):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle(kdecore.i18n("Settings for Output %1", output))

        self.iface = iface
        self.output = output
        self.configChanged.connect(parent.configChanged)

    def load(self):
        pass

    def show(self):
        QtGui.QDialog.show(self)

    def accept(self):
        QtGui.QDialog.accept(self)

    def reject(self):
        QtGui.QDialog.reject(self)

    def apply(self):
        pass

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

    depths = (16, 24, 30)
    configChanged = QtCore.pyqtSignal()

    def __init__(self, parent, iface):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.iface = iface
        self.configChanged.connect(parent.configChanged)

    def load(self):
        self.driver = self.iface.getDriver()
        self.depth = self.iface.getDepth()

    def show(self):
        drivers = self.iface.listDrivers()
        self.driverSelection.clear()
        self.driverSelection.addItems(drivers)

        if self.driver:
            self.manualDriverButton.setChecked(True)
            index = self.driverSelection.findText(self.driver)
            if index > -1:
                self.driverSelection.setCurrentIndex(index)
        else:
            self.autoDriverButton.setChecked(True)

        if self.depth:
            self.manualDepthButton.setChecked(True)
            self.depthSelection.setCurrentIndex(self.depths.index(self.depth))
        else:
            self.autoDepthButton.setChecked(True)

        QtGui.QDialog.show(self)

    def accept(self):
        oldDriver = self.driver
        oldDepth = self.depth

        if self.autoDriverButton.isChecked():
            self.driver = ""
        else:
            self.driver = str(self.driverSelection.currentText())

        if self.autoDepthButton.isChecked():
            self.depth = 0
        else:
            self.depth = self.depths[self.depthSelection.currentIndex()]

        if (oldDriver, oldDepth) != (self.driver, self.depth):
            self.configChanged.emit()

        QtGui.QDialog.accept(self)

    def reject(self):
        QtGui.QDialog.reject(self)

    def apply(self):
        self.iface.setDriver(self.driver)
        self.iface.setDepth(self.depth)

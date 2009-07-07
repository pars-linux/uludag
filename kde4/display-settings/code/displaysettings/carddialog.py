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
        self.changeList = []

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
            config = self.iface.getConfig()
            preferred = config.preferredDriver()
            if preferred:
                index = self.driverSelection.findText(preferred)
                if index > -1:
                    self.driverSelection.setCurrentIndex(index)

        if self.depth:
            self.manualDepthButton.setChecked(True)
            self.depthSelection.setCurrentIndex(self.depths.index(self.depth))
        else:
            self.autoDepthButton.setChecked(True)

        QtGui.QDialog.show(self)

    def accept(self):
        driver = "" if self.autoDriverButton.isChecked() else str(self.driverSelection.currentText())
        if driver != self.driver:
            self.changeList.append("driver")
            self.driver = driver

        depth = 0 if self.autoDepthButton.isChecked() else self.depths[self.depthSelection.currentIndex()]
        if depth != self.depth:
            self.changeList.append("depth")
            self.depth = depth

        if self.changeList:
            self.configChanged.emit()

        QtGui.QDialog.accept(self)

    def reject(self):
        QtGui.QDialog.reject(self)

    def setDriver(self, driver):
        self.changeList.append("driver")
        self.driver = driver
        self.configChanged.emit()

    def apply(self):
        if "driver" in self.changeList:
            self.iface.setDriver(self.driver)

        if "depth" in self.changeList:
            self.iface.setDepth(self.depth)

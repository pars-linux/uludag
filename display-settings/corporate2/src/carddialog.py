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

from qt import *
from kdecore import *
from kdeui import *
import kdedesigner

# UI
import ui.videocard

class VideoCardDialog(ui.videocard.VideoCardDialog):

    depths = (16, 24, 30)

    def __init__(self, parent, iface):
        ui.videocard.VideoCardDialog.__init__(self, parent)

        self.iface = iface

    def load(self):
        self.driver = self.iface.getDriver()
        self.depth = self.iface.getDepth()
        self.changeList = []

    def show(self):
        drivers = self.iface.listDrivers()
        self.driverSelection.clear()
        self.driverSelection.insertStrList(drivers)

        if self.driver:
            self.manualDriverButton.setChecked(True)
            if self.driver in drivers:
                index = drivers.index(self.driver)
                self.driverSelection.setCurrentItem(index)
        else:
            self.autoDriverButton.setChecked(True)
            config = self.iface.getConfig()
            preferred = config.preferredDriver()
            if preferred in drivers:
                index = drivers.index(preferred)
                self.driverSelection.setCurrentItem(index)

        if self.depth:
            self.manualDepthButton.setChecked(True)
            self.depthSelection.setCurrentItem(self.depths.index(self.depth))
        else:
            self.autoDepthButton.setChecked(True)

        ui.videocard.VideoCardDialog.show(self)

    def accept(self):
        driver = "" if self.autoDriverButton.isChecked() \
                        else str(self.driverSelection.currentText())

        if driver != self.driver:
            self.changeList.append("driver")
            self.driver = driver

        depth = 0 if self.autoDepthButton.isChecked() \
                        else self.depths[self.depthSelection.currentItem()]

        if depth != self.depth:
            self.changeList.append("depth")
            self.depth = depth

        if self.changeList:
            self.emit(PYSIGNAL("configChanged"), ())

        ui.videocard.VideoCardDialog.accept(self)

    def reject(self):
        ui.videocard.VideoCardDialog.reject(self)

    def setDriver(self, driver):
        self.changeList.append("driver")
        self.driver = driver
        self.emit(PYSIGNAL("configChanged"), ())

    def apply(self):
        if "driver" in self.changeList:
            self.iface.setDriver(self.driver)

        if "depth" in self.changeList:
            self.iface.setDepth(self.depth)

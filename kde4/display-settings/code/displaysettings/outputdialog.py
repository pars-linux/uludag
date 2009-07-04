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

    def __init__(self, parent, iface, outputName):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle(kdecore.i18n("Settings for Output %1", outputName))

        self.iface = iface
        self.outputName = outputName
        self.configChanged.connect(parent.configChanged)

        self.monitorType.currentIndexChanged.connect(self.slotTypeChanged)

        self.slotTypeChanged(0)

    def slotTypeChanged(self, index):
        isCustomMode = index == 2
        self.browseMonitorsButton.setDisabled(isCustomMode)
        self.hsyncMin.setEnabled(isCustomMode)
        self.hsyncMax.setEnabled(isCustomMode)
        self.vrefMin.setEnabled(isCustomMode)
        self.vrefMax.setEnabled(isCustomMode)

    def load(self):
        print "output %s load" % self.outputName

        config = self.iface.getConfig()
        output = config.outputs.get(self.outputName)
        monitor = config.monitors.get(self.outputName)

        self.ignored = output.ignored if output else False
        self.rangeSelected = monitor is not None

        if monitor:
            self.hsync = monitor.hsync
            self.vref = monitor.vref
            self.vendor = monitor.vendor
            self.model = monitor.model
        else:
            self.hsync = "28-33"
            self.vref = "43-72"
            self.vendor = "Generic"
            self.model = "Monitor 800x600"

    def show(self):
        self.ignoreOutputCheck.setChecked(self.ignored)
        self.freqBox.setChecked(self.rangeSelected)

        if self.vendor.startswith("Generic"):
            self.monitorType.setCurrentIndex(0)
        elif self.vendor.startswith("Custom"):
            self.monitorType.setCurrentIndex(2)
        else:
            self.monitorType.setCurrentIndex(1)

        QtGui.QDialog.show(self)

    def accept(self):
        changed = False

        ignored = self.ignoreOutputCheck.isChecked()
        if ignored != self.ignored:
            changed = True
            self.ignored = ignored

        if not ignored:
            rangeSelected = self.freqBox.isChecked()
            if rangeSelected != self.rangeSelected:
                changed = True
                self.rangeSelected = rangeSelected

        if changed:
            self.configChanged.emit()

        QtGui.QDialog.accept(self)

    def reject(self):
        QtGui.QDialog.reject(self)

    def apply(self):
        pass

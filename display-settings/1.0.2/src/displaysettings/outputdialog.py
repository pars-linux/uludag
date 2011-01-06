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

from displaysettings.monitorbrowser import MonitorBrowser

def splitRange(range):
    range = range.replace(" ", "")

    if "-" in range:
        return map(float, range.split("-"))
    else:
        return (float(range),)*2

class OutputDialog(QtGui.QDialog, Ui_OutputDialog):

    configChanged = QtCore.pyqtSignal()

    def __init__(self, parent, iface, outputName):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.okButton = self.buttonBox.button(QtGui.QDialogButtonBox.Ok)
        self.setWindowTitle(kdecore.i18n("Settings for Output %1", outputName))

        self.iface = iface
        self.outputName = outputName
        self.configChanged.connect(parent.configChanged)

        self.monitorType.currentIndexChanged.connect(self.slotTypeChanged)
        self.browseMonitorsButton.clicked.connect(self.slotBrowseMonitors)

        self.lastStdMonitor = None
        self.lastDBMonitor = None

        # Remove dimensions tab as it is not ready
        self.tabWidget.removeTab(1)

    def slotTypeChanged(self, index):
        notCustomMode = index != 2
        self.browseMonitorsButton.setEnabled(notCustomMode)
        self.hsyncMin.setReadOnly(notCustomMode)
        self.hsyncMax.setReadOnly(notCustomMode)
        self.vrefMin.setReadOnly(notCustomMode)
        self.vrefMax.setReadOnly(notCustomMode)

        if index == 0 and self.lastStdMonitor:
            self.vendor, model, hsync, vref = self.lastStdMonitor
            self.writeMonitorInfo(model, hsync, vref)
        elif index == 1 and self.lastDBMonitor:
            self.vendor, model, hsync, vref = self.lastDBMonitor
            self.writeMonitorInfo(model, hsync, vref)
        elif index == 2:
            self.vendor = "Custom"
            model = kdecore.i18n("Custom Monitor")
            self.monitorName.setText(model)
        else:
            self.vendor = ""
            model = kdecore.i18n("<qt><i>Click \"Choose...\" button to select a monitor</i></qt>")
            self.monitorName.setText(model)

        self.okButton.setDisabled(self.vendor == "")

    def slotBrowseMonitors(self):
        std = self.monitorType.currentIndex() == 0
        dlg = MonitorBrowser(self, std)
        if dlg.exec_() == QtGui.QDialog.Accepted:
            self.writeMonitorInfo(dlg.model, dlg.hsync, dlg.vref)
            if std:
                self.lastStdMonitor = (dlg.vendor, dlg.model, dlg.hsync, dlg.vref)
            else:
                self.lastDBMonitor = (dlg.vendor, dlg.model, dlg.hsync, dlg.vref)

            self.vendor = dlg.vendor
            self.okButton.setEnabled(True)

    def writeMonitorInfo(self, model, hsync, vref):
        self.monitorName.setText(model)

        hMin, hMax = splitRange(hsync)
        self.hsyncMin.setValue(hMin)
        self.hsyncMax.setValue(hMax)

        vMin, vMax = splitRange(vref)
        self.vrefMin.setValue(vMin)
        self.vrefMax.setValue(vMax)

    def load(self):
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
            self.hsync = "31.5-35.1"
            self.vref = "50-61"
            self.vendor = "Generic"
            self.model = "Monitor 800x600"

        self.writeMonitorInfo(self.model, self.hsync, self.vref)

        self.changeList = []

    def show(self):
        if self.vendor.startswith("Generic"):
            self.lastStdMonitor = (self.vendor, self.model, self.hsync, self.vref)
            self.monitorType.setCurrentIndex(0)
        elif self.vendor.startswith("Custom"):
            self.monitorType.setCurrentIndex(2)
        else:
            self.lastDBMonitor = (self.vendor, self.model, self.hsync, self.vref)
            self.monitorType.setCurrentIndex(1)

        self.freqBox.setChecked(self.rangeSelected)
        self.ignoreOutputCheck.setChecked(self.ignored)

        QtGui.QDialog.show(self)

    def accept(self):
        ignored = self.ignoreOutputCheck.isChecked()
        if ignored != self.ignored:
            self.changeList.append("ignored")
            self.ignored = ignored

        if not ignored:
            rangeSelected = self.freqBox.isChecked()
            if rangeSelected != self.rangeSelected:
                self.changeList.append("monitor")
                self.rangeSelected = rangeSelected

            if rangeSelected:
                hMin = self.hsyncMin.value()
                hMax = self.hsyncMax.value()
                vMin = self.vrefMin.value()
                vMax = self.vrefMax.value()
                oldhsync = splitRange(self.hsync)
                oldvref = splitRange(self.vref)

                model = str(self.monitorName.text())

                index = self.monitorType.currentIndex()
                if index == 0:
                    self.vendor = "Generic"
                elif index == 2:
                    self.vendor = "Custom"
                    model = "Custom"

                if model != self.model \
                        or (hMin, hMax) != oldhsync \
                        or (vMin, vMax) != oldvref:
                    self.changeList.append("monitor")
                    self.model = model
                    self.hsync = str(hMin) if hMin == hMax else "%s-%s" % (hMin, hMax)
                    self.vref = str(vMin) if vMin == vMax else "%s-%s" % (vMin, vMax)

        if self.changeList:
            self.configChanged.emit()

        QtGui.QDialog.accept(self)

    def reject(self):
        QtGui.QDialog.reject(self)

    def apply(self):
        if "ignored" in self.changeList:
            self.iface.setOutput(self.outputName, ignored=self.ignored)

        if "monitor" in self.changeList:
            if self.rangeSelected:
                self.iface.setMonitor(self.outputName,
                                      self.vendor,
                                      self.model,
                                      self.hsync,
                                      self.vref)
            else:
                self.iface.removeMonitor(self.outputName)

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
from displaysettings.ui_monitorbrowser import Ui_MonitorBrowser

from zorg import hwdata

class ListItem(QtGui.QListWidgetItem):
    def __init__(self, text, data, parent):
        QtGui.QListWidgetItem.__init__(self, text, parent)

        self.data = data

class MonitorBrowser(QtGui.QDialog, Ui_MonitorBrowser):
    def __init__(self, parent, generic):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

        generics, vendors = hwdata.getMonitorInfos()

        if generic:
            self.vendorsLabel.setText(kdecore.i18n("Type:"))
            self.modelsLabel.setText(kdecore.i18n("Monitors:"))

            for mtype, monitors in generics.items():
                if "CRT" in mtype:
                    mtype = "CRT"
                elif "LCD" in mtype:
                    mtype = "LCD"

                ListItem(mtype, monitors, self.vendorList)

        else:
            for vendor, monitors in vendors.items():
                ListItem(vendor, monitors, self.vendorList)

        self.vendorList.currentItemChanged.connect(self.slotVendorChanged)
        self.vendorList.setCurrentRow(0)

    def slotVendorChanged(self, current, previous):
        self.modelList.clear()
        for monitor in current.data:
            ListItem(monitor["model"], monitor, self.modelList)

        self.modelList.setCurrentRow(0)
        self.vendor = str(current.text())

    def accept(self):
        item = self.modelList.currentItem()
        self.model = item.data["model"]
        self.hsync = item.data["hsync"]
        self.vref = item.data["vref"]

        QtGui.QDialog.accept(self)

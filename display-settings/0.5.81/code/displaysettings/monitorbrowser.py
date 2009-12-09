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
from displaysettings.ui.monitorbrowser \
        import MonitorBrowser as Ui_MonitorBrowser

from zorg import hwdata

class ListItem(QListBoxText):
    def __init__(self, text, data, parent):
        QListBoxText.__init__(self, parent, text)

        self.data = data

class MonitorBrowser(Ui_MonitorBrowser):
    def __init__(self, parent, generic):
        Ui_MonitorBrowser.__init__(self, parent)

        generics, vendors = hwdata.getMonitorInfos()

        if generic:
            self.vendorsLabel.setText(i18n("Type:"))
            self.modelsLabel.setText(i18n("Monitors:"))

            for mtype, monitors in generics.items():
                if "CRT" in mtype:
                    mtype = "CRT"
                elif "LCD" in mtype:
                    mtype = "LCD"

                ListItem(mtype, monitors, self.vendorList)

        else:
            for vendor, monitors in vendors.items():
                ListItem(vendor, monitors, self.vendorList)

        self.connect(self.vendorList, \
                SIGNAL("currentChanged(QListBoxItem *)"), self.slotVendorChanged)

        self.vendorList.setSelected(0, True)

    def slotVendorChanged(self, current):
        self.modelList.clear()
        for monitor in current.data:
            ListItem(monitor["model"], monitor, self.modelList)

        self.modelList.setSelected(0, True)
        self.vendor = str(current.text())

    def accept(self):
        item = self.modelList.selectedItem()
        self.model = item.data["model"]
        self.hsync = item.data["hsync"]
        self.vref = item.data["vref"]

        QDialog.accept(self)

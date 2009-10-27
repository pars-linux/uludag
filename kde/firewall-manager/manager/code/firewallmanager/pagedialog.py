#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009 TUBITAK/UEKAE
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

# Settings item widget
from firewallmanager.settingsitem import SettingsItemWidget


class PageDialog(kdeui.KPageDialog):
    def __init__(self, parent, parameters, savedParameters):
        kdeui.KPageDialog.__init__(self, parent)

        self.setFaceType(kdeui.KPageDialog.Tabbed)
        self.setCaption(kdecore.i18n("Settings"))


        self.page_widget = PageWidget(self, parameters, savedParameters)
        self.page_item = kdeui.KPageWidgetItem(self.page_widget, kdecore.i18n("Settings"))

        self.addPage(self.page_item)

    def getValues(self):
        return self.page_widget.getValues()


class PageWidget(QtGui.QWidget):
    def __init__(self, parent, parameters=[], saved={}):
        QtGui.QWidget.__init__(self, parent)
        layout = QtGui.QVBoxLayout(self)
        self.widgets = {}
        for name, label, type_, options in parameters:
            widget = SettingsItemWidget(self, name, type_)
            widget.setTitle(label)
            widget.setOptions(options)
            if name in saved:
                widget.setValue(saved[name])
            self.widgets[name] = widget
            layout.addWidget(widget)

        self.item = QtGui.QSpacerItem(10, 10, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        layout.addSpacerItem(self.item)

    def getValues(self):
        values = {}
        for name, widget in self.widgets.iteritems():
            values[name] = widget.getValue()
        return values


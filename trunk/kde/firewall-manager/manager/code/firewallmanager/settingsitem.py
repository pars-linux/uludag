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
#from PyKDE4.kdeui import KIcon

# UI
from firewallmanager.ui_settingsitem import Ui_SettingsItemWidget


class SettingsItemWidget(QtGui.QWidget, Ui_SettingsItemWidget):
    def __init__(self, parent, name, type_):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.name = name
        self.type = type_

        self.lineItem.hide()
        self.comboItems.hide()
        self.listItems.hide()

        if type_ == "combo":
            self.comboItems.show()
        elif type_ == "editlist":
            self.listItems.show()
        elif type_ == "text":
            self.lineItem.show()

    def setTitle(self, title):
        self.labelTitle.setText(unicode(title))

    def setOptions(self, options):
        for key, value in options.iteritems():
            if key == "choose" and self.type == "combo":
                for item in value.split("\n"):
                    name, label = item.split("\t")
                    self.comboItems.addItem(label, QtCore.QVariant(name))
            elif key == "format" and self.type in ["editlist", "text"]:
                editor = self.listItems.lineEdit()
                validator = QtGui.QRegExpValidator(QtCore.QRegExp(value), self)
                editor.setValidator(validator)

    def setValue(self, value):
        value = unicode(value)
        if self.type == "combo":
            index = self.comboItems.findData(QtCore.QVariant(value))
            if index == -1:
                return
            self.comboItems.setCurrentIndex(index)
        elif self.type == "editlist":
            for item in value.split():
                self.listItems.insertItem(unicode(item))
        elif self.type == "text":
            self.lineItem.setText(unicode(value))

    def getValue(self):
        if self.type == "combo":
            index = self.comboItems.currentIndex()
            return unicode(self.comboItems.itemData(index).toString())
        elif self.type == "editlist":
            items = []
            for index in range(self.listItems.count()):
                items.append(unicode(self.listItems.text(index)))
            return " ".join(items)
        elif self.type == "text":
            return unicode(self.lineItem.text())

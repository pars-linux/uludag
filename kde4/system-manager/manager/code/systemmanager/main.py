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
from systemmanager.ui_main import Ui_MainWidget

# Backend
from systemmanager.backend import Interface

# Config
#from systemmanager.config import

class MainWidget(QtGui.QWidget, Ui_MainWidget):
    def __init__(self, parent, embed=False):
        QtGui.QWidget.__init__(self, parent)

        if embed:
            self.setupUi(parent)
        else:
            self.setupUi(self)

        # Backend
        self.iface = Interface()
        self.iface.listenSignals(self.signalHandler)

        # Fail if no packages provide backend
        self.checkBackend()

        # Set icons
        self.pixmapLanguage.setPixmap(kdeui.KIcon("applications-education-language").pixmap(48, 48))
        self.pixmapTime.setPixmap(kdeui.KIcon("chronometer").pixmap(48, 48))
        self.pixmapPackage.setPixmap(kdeui.KIcon("applications-other").pixmap(48, 48))
        self.pixmapConsole.setPixmap(kdeui.KIcon("utilities-terminal").pixmap(48, 48))

        # Initialize
        self.buildLists()
        self.setItems()

    def checkBackend(self):
        """
            Check if there are packages that provide required backend.
        """
        if not len(self.iface.getPackages()):
            kdeui.KMessageBox.error(self, kdecore.i18n("There are no packages that provide backend for this application.\nPlease be sure that packages are installed and configured correctly."))
            return False
        return True

    def signalHandler(self, package, signal, args):
        pass

    def buildLists(self):
        # Languages
        self.comboLanguage.clear()
        for code, label in self.iface.listLanguages():
            self.comboLanguage.addItem(label, QtCore.QVariant(code))
        # Locales
        self.comboLocale.clear()
        for code, label in self.iface.listLocales():
            self.comboLocale.addItem(label, QtCore.QVariant(code))
        # Keyboard maps
        self.comboKeyboard.clear()
        for code, label in self.iface.listKeymaps():
            self.comboKeyboard.addItem(label, QtCore.QVariant(code))
        # Time zones
        self.comboTimeZone.clear()
        # Services
        self.comboHeadStart.clear()
        self.comboHeadStart.addItem(kdecore.i18n("None"), QtCore.QVariant(""))
        for package, label in self.iface.listServices():
            self.comboHeadStart.addItem(label, QtCore.QVariant(package))

    def setItems(self):
        # Language
        language = QtCore.QVariant(self.iface.getLanguage())
        index = self.comboLanguage.findData(language)
        if index != -1:
            self.comboLanguage.setCurrentIndex(index)
        # Locale
        locale = QtCore.QVariant(self.iface.getLocale())
        index = self.comboLocale.findData(locale)
        if index != -1:
            self.comboLocale.setCurrentIndex(index)
        # Keyboard map
        keymap = QtCore.QVariant(self.iface.getKeymap())
        index = self.comboKeyboard.findData(keymap)
        if index != -1:
            self.comboKeyboard.setCurrentIndex(index)
        # Time zone
        pass
        # Clock
        is_utc, adjust = self.iface.getClock()
        if is_utc:
            self.checkUTC.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkUTC.setCheckState(QtCore.Qt.Unchecked)
        if adjust:
            self.checkClockAdjust.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkClockAdjust.setCheckState(QtCore.Qt.QtUnchecked)
        # Head start
        service = QtCore.QVariant(self.iface.getHeadStart())
        index = self.comboHeadStart.findData(service)
        if index != -1:
            self.comboHeadStart.setCurrentIndex(index)
        # Console
        self.spinTTY.setValue(self.iface.getTTYs())

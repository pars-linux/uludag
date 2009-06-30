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

        # Actions
        self.connect(self.buttonBox, QtCore.SIGNAL("clicked(QAbstractButton*)"), self.slotButtonsClicked)

        # Initialize
        self.buildLists()

    def slotButtonsClicked(self, button):
        if self.buttonBox.buttonRole(button) == QtGui.QDialogButtonBox.ApplyRole:
            self.saveItems()
        elif self.buttonBox.buttonRole(button) == QtGui.QDialogButtonBox.ResetRole:
            self.buildLists()

    def checkBackend(self):
        """
            Check if there are packages that provide required backend.
        """
        if not len(self.iface.getPackages()):
            kdeui.KMessageBox.error(self, kdecore.i18n("There are no packages that provide backend for this application.\nPlease make sure that packages are installed and configured correctly."))
            return False
        return True

    def signalHandler(self, package, signal, args):
        pass

    def buildLists(self):
        # All languages
        self.comboLanguage.clear()
        for code, label in self.iface.listLanguages():
            self.comboLanguage.addItem(label, QtCore.QVariant(code))
        # Selected language
        language = QtCore.QVariant(self.iface.getLanguage())
        index = self.comboLanguage.findData(language)
        if index != -1:
            self.comboLanguage.setCurrentIndex(index)
        # All Keymaps
        self.comboKeyboard.clear()
        for code, label in self.iface.listKeymaps():
            self.comboKeyboard.addItem(label, QtCore.QVariant(code))
        # Selected keymap
        keymap = QtCore.QVariant(self.iface.getKeymap())
        index = self.comboKeyboard.findData(keymap)
        if index != -1:
            self.comboKeyboard.setCurrentIndex(index)
        # All services
        self.comboHeadStart.clear()
        self.comboHeadStart.addItem(kdecore.i18n("None"), QtCore.QVariant(""))
        for package, label in self.iface.listServices():
            self.comboHeadStart.addItem("%s (%s)" % (label, package), QtCore.QVariant(package))
        # Head start
        service = QtCore.QVariant(self.iface.getHeadStart())
        index = self.comboHeadStart.findData(service)
        if index != -1:
            self.comboHeadStart.setCurrentIndex(index)
        # Console
        self.spinTTY.setValue(self.iface.getTTYs())
        # Clock
        is_utc, adjust = self.iface.getClock()
        if is_utc:
            self.checkUTC.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkUTC.setCheckState(QtCore.Qt.Unchecked)
        if adjust:
            self.checkClockAdjust.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkClockAdjust.setCheckState(QtCore.Qt.Unchecked)

    def saveItems(self):
        # Language
        language = self.comboLanguage.itemData(self.comboLanguage.currentIndex())
        language = str(language.toString())
        self.iface.setLanguage(language)
        # Keymap
        keymap = self.comboKeyboard.itemData(self.comboKeyboard.currentIndex())
        keymap = str(keymap.toString())
        self.iface.setKeymap(keymap)
        # Head start
        package = self.comboHeadStart.itemData(self.comboHeadStart.currentIndex())
        package = str(package.toString())
        self.iface.setHeadStart(package)
        # Console
        self.iface.setTTYs(self.spinTTY.value())
        # Clock
        is_utc = self.checkUTC.checkState() == QtCore.Qt.Checked
        adjust = self.checkClockAdjust.checkState() == QtCore.Qt.Checked
        self.iface.setClock(is_utc, adjust)

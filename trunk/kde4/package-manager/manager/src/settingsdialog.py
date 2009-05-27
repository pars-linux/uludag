#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file

from PyQt4 import QtGui

from PyKDE4.kdecore import i18n
from PyKDE4.kdeui import *

from ui_settingsdialog import Ui_SettingsDialog

class SettingsDialog(QtGui.QDialog, Ui_SettingsDialog):
    def __init__(self, state, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.state = state
        self.setupUi(self)
        self.initialize()
        self.connectSignals()

    def initialize(self):
        self.moveUpButton.setIcon(KIcon("arrow-up"))
        self.moveDownButton.setIcon(KIcon("arrow-down"))
        self.addRepoButton.setIcon(KIcon("list-add"))
        self.removeRepoButton.setIcon(KIcon("list-remove"))

    def connectSignals(self):
        self.connect(self.buttonOk, SIGNAL("clicked()"), self.saveSettings)

    def saveSettings(self):
        pass

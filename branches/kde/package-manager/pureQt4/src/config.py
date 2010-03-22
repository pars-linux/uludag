#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file

from PyQt4.Qt import QVariant, QSettings

general = 'General'
defaults = {"SystemTray":False,
            "UpdateCheck":False,
            "InstallUpdatesAutomatically":False,
            "UpdateCheckInterval":60,
            }

class Config:
    def __init__(self, organization, product):
        self.config = QSettings(organization, product)

    def setValue(self, group, option, value):
        self.config.beginGroup(group)
        self.config.setValue(option, QVariant(value))
        self.config.endGroup(group)
        self.config.sync()

    def getBoolValue(self, group, option):
        self.config.beginGroup(group)
        default = self._initValue(option, False)
        return self.config.value(option, QVariant(default)).toBool()

    def getNumValue(self, group, option):
        self.config.beginGroup(group)
        default = self._initValue(option, 0)
        return self.config.value(option, QVariant(default)).toInt()[0]

    def _initValue(self, option, value):
        if defaults.has_key(option):
            return defaults[option]
        return value

class PMConfig(Config):
    def __init__(self):
        Config.__init__(self, "Pardus", "Package-Manager")

    def showOnlyGuiApp(self):
        return self.getBoolValue(general, "ShowOnlyGuiApp")

    def updateCheck(self):
        return self.getBoolValue(general, "UpdateCheck")

    def installUpdatesAutomatically(self):
        return self.getBoolValue(general, "InstallUpdatesAutomatically")

    def updateCheckInterval(self):
        return self.getNumValue(general, "UpdateCheckInterval")

    def systemTray(self):
        return self.getBoolValue(general, "SystemTray")

    def setSystemTray(self, enabled):
        self.setValue(general, "SystemTray", enabled)

    def setUpdateCheck(self, enabled):
        self.setValue(general, "UpdateCheck", enabled)

    def setInstallUpdatesAutomatically(self, enabled):
        self.setValue(general, "InstallUpdatesAutomatically", enabled)

    def setUpdateCheckInterval(self, value):
        self.setValue(general, "UpdateCheckInterval", value)

    def setShowOnlyGuiApp(self, enabled):
        self.setValue(general, "ShowOnlyGuiApp", enabled)

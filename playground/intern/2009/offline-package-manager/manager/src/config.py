#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file

from PyKDE4.kdecore import KConfig

(general) = ("General")

defaults = {"SystemTray":False,
            "UpdateCheck":False,
            "InstallUpdatesAutomatically":False,
            "UpdateCheckInterval":60,
            }

class Config:
    def __init__(self, config):
        self.config = KConfig(config)
        self.group = None

    def setValue(self, group, option, value):
        self.group = self.config.group(group)
        self.group.writeEntry(option, str(value))
        self.config.sync()

    def getBoolValue(self, group, option):
        default = self._initValue(group, option, False)
        return self.group.readEntry(option, str(default)) == "True"

    def getNumValue(self, group, option):
        default = self._initValue(group, option, 0)
        return int(self.group.readEntry(option, str(default)))

    def _initValue(self, group, option, value):
        self.group = self.config.group(group)

        if defaults.has_key(option):
            return defaults[option]
        else:
            return value

class PMConfig(Config):
    def __init__(self):
        Config.__init__(self, "package-managerrc")

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

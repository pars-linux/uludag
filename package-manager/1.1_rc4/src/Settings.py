#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file

(general) = ("General")

defaults = {"SystemTray":True,
            "UpdateCheck":True,
            "UpdateCheckInterval":60
            }

class Settings:
    def __init__(self, config):
        self.config = config

    def setValue(self, group, option, value):
        self.config.setGroup(group)
        self.config.writeEntry(option, value)
        self.config.sync()

    def getBoolValue(self, group, option):
        default = self._initValue(group, option, False)
        return self.config.readBoolEntry(option, default)

    def getNumValue(self, group, option):
        default = self._initValue(group, option, 0)
        return self.config.readNumEntry(option, default)

    def _initValue(self, group, option, value):
        self.config.setGroup(group)

        if defaults.has_key(option):
            return defaults[option]
        else:
            return value

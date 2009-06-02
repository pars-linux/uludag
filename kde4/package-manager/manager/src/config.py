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

(general) = ("General")

defaults = {"SystemTray":False,
            "UpdateCheck":False,
            "UpdateCheckInterval":60,
            }

class Config:
    def __init__(self, config):
        self.config = config
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

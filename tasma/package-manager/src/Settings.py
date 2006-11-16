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

class Settings:
    def __init__(self, config):
        self.config = config

    def setValue(self, group, option, value):
        self.config.setGroup(group)
        self.config.writeEntry(option, value)
        self.config.sync()

    def getBoolValue(self, group, option):
        self.config.setGroup(group)
        return self.config.readBoolEntry(option, False)

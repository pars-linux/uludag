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

# Comar
import comar

# DBus
import dbus

class Interface:
    def __init__(self):
        self.link = comar.Link()
        self.link.setLocale()
        self.package = self.getMainPackage()

    def getPackages(self):
        """
            List of packages that provide Disk.Manager model
        """
        return list(self.link.User.Manager)

    def getMainPackage(self):
        """
            Package that's selected by system.
            For now, it's hardcoded. This value should be given by COMAR.
        """
        packages = self.getPackages()
        if not len(packages):
            return None
        return "mudur"

    def deviceList(self, func=None):
        if func:
            self.link.Disk.Manager[self.package].getDevices(async=func)
        else:
            return self.link.Disk.Manager[self.package].getDevices()

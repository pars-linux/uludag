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

# Comar
import comar
import zorg.config
from zorg.utils import idsQuery

from displaysettings.device import Output
from displaysettings.nv import Interface as NVInterface
from displaysettings.randr import Interface as RRInterface

class Interface:
    def __init__(self):
        self.link = comar.Link()
        self.link.setLocale()
        self.link.useAgent()
        self.package = self.getMainPackage()

        self.ext = NVInterface()
        print "NVCTRL" if self.ext.ready else "RANDR", "extension will be used to get hardware info."
        if not self.ext.ready:
            self.ext = RRInterface()

        self.readConfig()
        self.cardVendor, self.cardModel = idsQuery(self._info.vendor_id,
                                                   self._info.product_id)

    def readConfig(self):
        self._bus = self.link.Xorg.Display["zorg"].activeDeviceID()
        self._info = zorg.config.getDeviceInfo(self._bus)

        if not self._info:
            # XXX
            print "corrupted config"
            return

        self.monitors = self._info.monitors

    def listenSignals(self, func):
        self.link.listenSignals("X.Y", func)

    def getPackages(self):
        """
            List of packages that provide Xorg.Display model
        """
        return list(self.link.Xorg.Display)

    def getMainPackage(self):
        """
            Display Settings tool is heavily zorg dependent.
        """
        return "zorg"

    def getConfig(self):
        return self._info

    def listDrivers(self):
        return map(str, self.link.Xorg.Display["zorg"].listDrivers())

    def getDriver(self):
        return self._info.driver if self._info.driver else ""

    def setDriver(self, driver):
        if driver == self.getDriver():
            return

        self.link.Xorg.Display["zorg"].setDriver(driver)

    def getDepth(self):
        return self._info.depth

    def setDepth(self, depth):
        if depth == self.getDepth():
            return

        self.link.Xorg.Display["zorg"].setDepth(depth)

    def getOutputs(self):
        return self.ext.getOutputs()

    def sync(self):
        self.link.Xorg.Display["zorg"].syncConfigs()
        self.readConfig()

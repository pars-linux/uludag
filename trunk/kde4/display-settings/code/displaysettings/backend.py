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

MODES = [
    "2048x1536",
    "1920x1440",
    "1920x1200",
    "1680x1050",
    "1600x1200",
    "1600x1024",
    "1440x900",
    "1400x1050",
    "1366x768",
    "1360x1024",
    "1360x768",
    "1280x1024",
    "1280x960",
    "1280x800",
    "1280x768",
    "1280x720", # 720p
    "1152x864",
    "1152x768",
    "1024x768",
    "1024x600",
    "800x600",
    "640x480"
]

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
        outputs = self.ext.getOutputs()
        if outputs:
            return outputs
        else:
            return [Output("default")]

    def setOutput(self, name, enabled=None, ignored=None):
        output = self._info.outputs.get(name)
        if output:
            if enabled is None:
                enabled = output.enabled

            if ignored is None:
                ignored = output.ignored
        else:
            if enabled is None:
                enabled = True

            if ignored is None:
                ignored = True

        self.link.Xorg.Display["zorg"].setOutput(name, enabled, ignored)

    def setMonitor(self, outputName, vendor, model, hsync, vref):
        self.link.Xorg.Display["zorg"].setMonitor(outputName, vendor, model, \
                                                    hsync, vref)

    def removeMonitor(self, outputName):
        self.link.Xorg.Display["zorg"].setMonitor(outputName, "", "", "", "")

    def getModes(self, outputName):
        return MODES

    def setMode(self, outputName, mode, rate):
        self.link.Xorg.Display["zorg"].setMode(outputName, mode, rate)

    def getRates(self, outputName, mode):
        return ["60"]

    def setRotation(self, outputName, rotation):
        self.link.Xorg.Display["zorg"].setOrientation(outputName, rotation, "")

    def setSimpleLayout(self, left, right, cloned):
        self.link.Xorg.Display["zorg"].setPosition(left, "", "")

        if right:
            pos = "" if cloned else "RightOf"
            arg = "" if cloned else left
            self.link.Xorg.Display["zorg"].setPosition(right, pos, arg)

    def sync(self):
        self.link.Xorg.Display["zorg"].syncConfigs()
        self.readConfig()

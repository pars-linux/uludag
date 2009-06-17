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

import displaysettings.nv
import displaysettings.randr

class Interface:
    def __init__(self):
        self.link = comar.Link()
        self.link.setLocale()
        self.link.useAgent()
        self.package = self.getMainPackage()

        self.ext = displaysettings.nv.Interface()
        if not self.ext.ready:
            self.ext = displaysettings.randr.Interface()

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


class Output:
    Connected = 0
    Disconnected = 1
    Unknown = 2

    def __init__(self, name):
        self.name = name
        self.connection = self.Disconnected

    def __repr__(self):
        return "<Output %s>" % self.name

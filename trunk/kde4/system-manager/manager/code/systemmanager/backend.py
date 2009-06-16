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


class Interface:
    def __init__(self):
        self.link = comar.Link()
        self.link.setLocale()
        self.link.useAgent()
        self.package = self.getMainPackage()

    def listenSignals(self, func):
        self.link.listenSignals("X.Y", func)

    def getPackages(self):
        """
            List of packages that provide System.Settings model
        """
        return list(self.link.System.Settings)

    def getMainPackage(self):
        """
            System Manager is heavily mudur dependent.
        """
        return "mudur"

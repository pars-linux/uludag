#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import comar
import pisi

class Iface:
    """
        Package Manager operations abstraction layer
    """

    def __init__(self):
        # Connect to COMAR
        self.link = comar.Link()
        self.pdb  = pisi.db.packagedb.PackageDB()

    def getPackageList(self):
        return pisi.api.list_available()

    def getPackage(self, name):
        return self.pdb.get_package(name)

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

class Iface:
    """
        Package Manager operations abstraction layer
    """

    (SYSTEM, REPO) = range(2)

    def __init__(self, source=REPO):
        """ Interface initialization """
        self.source = source

    def setSource(self, source):
        """ set the package list info source """
        pass

    def getPackageList(self):
        """ returns the package list """
        pass

    def getUpdates(self):
        """ returns the upgradable package list """
        pass

    def getGroups(self):
        """ returns all the group names """
        pass

    def getGroupPackages(self, name):
        """ returns the package list of the given group """
        pass

    def getGroupComponents(self, name):
        """ returns the component list of the given group """
        pass

    def getPackage(self, name):
        """ returns the package info """
        pass

    def getDepends(self, packages):
        """ returns the packages that the given packages depends """
        pass

    def getRequires(self, packages):
        """ returns the packages that the given packages required by """
        pass

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
# Please read the COPYING file.

from sets import Set as set
import PisiIface

(install_state, remove_state, upgrade_state) = range(3)

class Basket:
    def __init__(self):
        self.state = None
        self.packagesSize = 0
        self.extraPackagesSize = 0
        self.packages = []
        self.extraPackages = []

    def add(self, package):
        self.packages.append(str(package))

    def remove(self, package):
        self.packages.remove(str(package))

    def dump(self, packages):
        self.packages.extend(map(lambda x:str(x), packages))

    def empty(self):
        self.packages = []
        self.extraPackages = []
        self.packagesSize = 0
        self.extraPackagesSize = 0

    def setState(self, state):
        self.state = state

    def update(self):
        self.packagesSize = 0
        self.extraPackagesSize = 0

        pkgs = self.packages
        if not pkgs:
            self.extraPackages = []
            return
        
        if self.state == remove_state:
            self.extraPackages = PisiIface.getRequires(pkgs)
        else:
            self.extraPackages = PisiIface.getDepends(pkgs)

        for package in pkgs:
            self.packagesSize += self.getPackageSize(self.getPackage(package))

        for package in self.extraPackages:
            self.extraPackagesSize += self.getPackageSize(self.getPackage(package))

    def getBasketSize(self):
        return self.extraPackagesSize + self.packagesSize

    def getPackageSize(self, package):
        if self.state == remove_state:
            return package.installedSize
        else:
            return package.packageSize

    def getPackage(self, package):
        return PisiIface.getPackage(package)

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

import groups
import pisi

class Iface:

    (SYSTEM, REPO) = range(2)

    def __init__(self, source=REPO):
        self.source = source

        # init databases
        self.pdb  = pisi.db.packagedb.PackageDB()
        self.cdb  = pisi.db.componentdb.ComponentDB()
        self.idb  = pisi.db.installdb.InstallDB()

    def setSource(self, source):
        self.source = source

    def getPackageList(self):
        if self.source == self.REPO:
            return pisi.api.list_available()
        else:
            return pisi.api.list_installed()

    def getUpdates(self):
        return pisi.api.list_upgradable()

    def getGroups(self):
        _groups = []
        for group in groups.getGroups():
            _groups.append(groups.groups[group])
        return _groups

    def getGroupPackages(self, name):
        components = groups.getGroupComponents(name)
        packages = []
        for component in components:
            packages.extend(self.cdb.get_union_packages(component))
        return packages

    def getGroupComponents(self, name):
        return groups.getGroupComponents(name)

    def getPackage(self, name):
        if self.source == self.REPO:
            return self.pdb.get_package(name)
        else:
            return self.idb.get_package(name)

    def getDepends(self, packages):
        if not self.idb.has_package(packages[0]):
            deps = set(pisi.api.get_install_order(packages))
        else:
            deps = set(pisi.api.get_upgrade_order(packages))
        return list(set(deps) - set(packages))

    def getRequires(self, packages):
        revDeps = set(pisi.api.get_remove_order(packages))
        return list(set(revDeps) - set(packages))

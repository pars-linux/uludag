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

import pisi
from kdecore import i18n
import Icons

class Package:
    def __init__(self, name, summary, description, version, icon_path, size, homepage, repo):
        self.name = name
        self.summary = summary
        self.description = description
        self.version = version
        self.icon_path = icon_path
        self.size = self._sizer(size)
        self.homepage = homepage
        self.repo = repo

    def _sizer(self, size):
        if size:
            tpl = pisi.util.human_readable_size(size)
            return "%.0f %s" % (tpl[0], tpl[1])
        else:
            return i18n("N\A")

    def __str__(self):
        return self.name

    def lower(self):
        return self.name.lower()

class PackageCache:
    def __init__(self):
        self.packages = {}

    def clearCache(self):
        self.packages.clear()

    def isEmpty(self):
        return not self.packages

    def populateCache(self, packages, inInstalled = False):
        for pkg_name in packages:
            if inInstalled:
                try:
                    package, repo = pisi.db.packagedb.PackageDB().get_package_repo(pkg_name)
                except:
                    package = pisi.db.installdb.InstallDB().get_package(pkg_name)
                    repo = i18n("N\A")
                size = package.installedSize
            else:
                package, repo = pisi.db.packagedb.PackageDB().get_package_repo(pkg_name)
                size = package.packageSize

            if package.source:
                homepage = package.source.homepage
            else:
                homepage = i18n("N\A")

            self.packages[package.name] = (Package(package.name,
                                          package.summary,
                                          package.description,
                                          package.version,
                                          Icons.getIconPath(package.icon),
                                          size,
                                          homepage,
                                          repo))

    def searchInPackages(self, terms):
        def search(package, term):
            term = unicode(term).lower()
            if term in unicode(package.name).lower() or \
               term in unicode(package.summary).lower() or \
               term in unicode(package.description).lower():
                return True

        found = []
        for pkg in self.packages.values():
            if terms == filter(lambda x:search(pkg, x), terms):
                found.append(pkg.name)

        return found

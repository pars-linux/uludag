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

class Package:
    def __init__(self, name, summary, description):
        self.name = name
        self.summary = summary
        self.description = description

class PackageCache:
    def __init__(self):
        self.packages = []

    def clearCache(self):
        self.packages = []

    def isEmpty(self):
        return not self.packages

    def populateCache(self, packages, repo=None):
        for pkg_name in packages:
            package = pisi.context.packagedb.get_package(pkg_name, repo)
            self.packages.append(Package(package.name, package.summary, package.description))

    def searchInPackages(self, terms):
        def search(package, term):
            term = unicode(term).lower()
            if term in unicode(package.name).lower() or \
               term in unicode(package.summary).lower() or \
               term in unicode(package.description).lower():
                return True

        found = []
        for pkg in self.packages:
            if terms == filter(lambda x:search(pkg, x), terms):
                found.append(pkg.name)

        return found

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

import PisiIface

class PackageCache:
    def __init__(self):
        pass

    def clearCache(self):
        pass

    def isEmpty(self):
        pass

    def populateCache(self, packages, inInstalled = False):
        for pkg_name in packages:
            if inInstalled:
                packageInstalled = PisiIface.get_installed_package(pkg_name)
                try:
                    packageInRepo, repoOfPackage = PisiIface.get_repo_and_package(pkg_name)
                    # if package is in both packagedb and installdb, then think that if they are same. If not, this means package is installed manually
                    if packageInRepo.version != packageInstalled.version or \
                            packageInRepo.release != packageInstalled.release or \
                            packageInRepo.build != packageInstalled.build:
                        package = packageInstalled
                        repo = i18n("N\A")
                    else:
                        package = packageInRepo
                        repo = repoOfPackage
                except:
                    # this means PackageDB exception, so package is installed manually
                    repo = i18n("N\A")

                size = package.installedSize
            else:
                package, repo = PisiIface.get_repo_and_package(pkg_name)
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

    def get_package(self, package):
        return self.packages[package]

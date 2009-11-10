#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

class PackageCollection:
    def __init__(self, uniqueTag, icon, title, description, packageSelection):
        self.uniqueTag = uniqueTag
        self.icon = icon
        self.title = title
        self.description = description
        self.packageSelection = packageSelection


class PackageSelection:
    def __init__(self, repoURI, selectedComponents=[], selectedPackages=[], allPackages=[]):
        self.repoURI = repoURI
        self.selectedComponents = selectedComponents
        self.selectedPackages = selectedPackages
        self.allPackages = allPackages

    def addSelectedComponent(self, component):
        self.selectedComponents.append(component)

    def addSelectedPackage(self, package):
        self.selectedPackages.append(package)

    def addPackage(self, package):
        self.allPackages.append(package)

class LanguageSelection:
    def __init__(self, defaultLanguage, languages=[]):
        self.defaultLanguage = defaultLanguage
        self.languages = languages

    def addLanguage(language):
        self.languages.append(language)


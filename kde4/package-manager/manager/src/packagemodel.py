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

# Qt Stuff
from PyQt4 import QtGui
from PyQt4.QtCore import *

# PyKDE4 Stuff
from PyKDE4.kdeui import *

import string
import backend

(SummaryRole, DescriptionRole, VersionRole, GroupRole) = (Qt.UserRole, Qt.UserRole+1, Qt.UserRole+2, Qt.UserRole+3)

class PackageModel(QAbstractTableModel):

    def __init__(self, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.iface = backend.pm.Iface()
        self.resetCachedInfos()
        self.cached_package = None
        self.packages = []

    def rowCount(self, index=QModelIndex()):
        return len(self.packages)

    def columnCount(self, index=QModelIndex()):
        return 2

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()

        if role == Qt.DisplayRole:
            return QVariant(self.packages[index.row()])
	elif role == Qt.CheckStateRole and index.column() == 0:
            return QVariant(self.package_selections[index.row()])
        elif role == Qt.DecorationRole:
            return QVariant(":/data/package.png")

        package = self.package(index)
        if role == SummaryRole:
            return QVariant(unicode(package.summary))
        elif role == DescriptionRole:
            return QVariant(unicode(package.description))
        elif role == VersionRole:
            return QVariant(unicode(package.version))
        elif role == GroupRole:
            # TODO
            return QVariant()
        else:
            return QVariant()

    def setData(self, index, value, role):
        if role == Qt.CheckStateRole and index.column() == 0:
            self.package_selections[index.row()] = value
            self.resetCachedInfos()
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index)
            return True
        else:
            return False

    def flags(self, index):
        if index.isValid() and index.column() == 0:
            return Qt.ItemIsEnabled | Qt.ItemIsUserCheckable | QAbstractTableModel.flags(self, index)
        else:
            return Qt.ItemIsEnabled

    def setPackages(self, packages):
        self.cached_package = None
        self.packages = packages
        self.package_selections = [Qt.Unchecked] * len(self.packages)
        self.packages.sort(key=string.lower)
        self.reset()

    def package(self, index):
        if self.cached_package and self.cached_package.name == self.packages[index.row()]:
            return self.cached_package
        else:
            self.cached_package = self.iface.getPackage(self.packages[index.row()])
            return self.cached_package

    # FIXME: There should really be a better way to get this from proxy. Proxy's selectedIndexes only
    # returns the selected but filtered packages.
    def selectedPackages(self):
        if not self.cached_selected:
            for i, pkg in enumerate(self.packages):
                if self.package_selections[i] == Qt.Checked:
                    self.cached_selected.append(pkg)
        return self.cached_selected

    def extraPackages(self):
        if not self.cached_extras:
            self.cached_extras = self.iface.getExtras(self.selectedPackages())
        return self.cached_extras

    def __packagesSize(self, packages):
        size = 0
        for name in packages:
            size += self.iface.getPackageSize(name)
        return size

    def selectedPackagesSize(self):
        if not self.cached_selected_size < 0:
            self.cached_selected_size = self.__packagesSize(self.selectedPackages())
        return self.cached_selected_size

    def extraPackagesSize(self):
        if not self.cached_extras_size < 0:
            self.cached_extras_size = self.__packagesSize(self.extraPackages())
        return self.cached_extras_size

    def resetCachedInfos(self):
        self.cached_selected = []
        self.cached_extras = []
        self.cached_selected_size = 0
        self.cached_extras_size = 0

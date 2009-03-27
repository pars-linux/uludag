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
        self.cached_package = None
        self.packages = self.iface.getPackageList()
        self.package_selections = [Qt.Unchecked] * len(self.packages)
        self.packages.sort(key=string.lower)

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
            return QVariant("icons/package.png")

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
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index)
            return True
        else:
            return False

    def flags(self, index):
        if index.isValid() and index.column() == 0:
            return Qt.ItemIsEnabled | Qt.ItemIsUserCheckable | QAbstractTableModel.flags(self, index)
        else:
            return Qt.ItemIsEnabled

    def package(self, index):
        if self.cached_package and self.cached_package.name == self.packages[index.row()]:
            return self.cached_package
        else:
            self.cached_package = self.iface.getPackage(self.packages[index.row()])
            return self.cached_package

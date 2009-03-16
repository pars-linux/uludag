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
import pmtools

(SummaryRole, DescriptionRole, VersionRole) = (Qt.UserRole, Qt.UserRole+1, Qt.UserRole+2)

class PackageModel(QAbstractTableModel):

    def __init__(self, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.iface = pmtools.Iface()
        self.packages = self.iface.getPackageList()
        self.package_selections = [Qt.Unchecked] * len(self.packages)
        self.packages.sort(key=string.lower)
        self.icon = QtGui.QIcon(QtGui.QPixmap("icons/package.png"))

    def rowCount(self, index=QModelIndex()):
        return len(self.packages)

    def columnCount(self, index=QModelIndex()):
        return 2

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()

        package = self.iface.getPackage(self.packages[index.row()])

        if role == Qt.DisplayRole:
            return package.name
        elif role == Qt.DecorationRole:
            return self.icon
        elif role == SummaryRole:
            return unicode(package.summary)
        elif role == DescriptionRole:
            return unicode(package.description)
        elif role == VersionRole:
            return unicode(package.version)
	elif role == Qt.CheckStateRole and index.column() == 0:
            return QVariant(self.package_selections[index.row()])
        else:
            return QVariant()

    def setData(self, index, value, role):
        if role == Qt.CheckStateRole and index.column() == 0:
            self.package_selections[index.row()] = value
            return True
        else:
            return False

    def flags(self, index):
        if index.isValid() and index.column() == 0:
            return Qt.ItemIsEnabled | Qt.ItemIsUserCheckable | QAbstractTableModel.flags(self, index)
        else:
            return QAbstractTableModel.flags(self, index)

    def package(self, index):
        return self.packages[index.row()]

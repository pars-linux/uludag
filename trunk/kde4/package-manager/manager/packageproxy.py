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
from PyKDE4.kdecore import *

class PackageProxy(QtGui.QSortFilterProxyModel):

    def __init__(self, parent=None):
        QtGui.QSortFilterProxyModel.__init__(self, parent)
        self.__sourceModel = None
        self.__modelCache = {}

    def setSourceModel(self, model):
        QtGui.QSortFilterProxyModel.setSourceModel(self, model)
        self.__sourceModel = model

    def data(self, index, role):
        sourceIndex = self.mapToSource(index)
        if role != Qt.CheckStateRole and self.__modelCache.has_key(sourceIndex.row()) and self.__modelCache[sourceIndex.row()].has_key(role):
            v = self.__modelCache[sourceIndex.row()][role]
        else:
            v = self.__sourceModel.data(self.mapToSource(index), role)
            if not self.__modelCache.has_key(sourceIndex.row()):
                self.__modelCache[sourceIndex.row()] = {}
            if not self.__modelCache[sourceIndex.row()].has_key(role):
                self.__modelCache[sourceIndex.row()][role] = v
        return v

    def setData(self, index, value, role):
        return self.__sourceModel.setData(self.mapToSource(index), value, role)

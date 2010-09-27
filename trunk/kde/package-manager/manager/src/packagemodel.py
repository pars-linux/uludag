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

import string
import backend
from pmutils import humanReadableSize
from pmlogging import logger

from PyKDE4.kdeui import KIconLoader
from context import _time

from statemanager import StateManager

(SummaryRole, DescriptionRole, VersionRole, GroupRole, \
    RepositoryRole, HomepageRole, SizeRole, TypeRole, \
    ComponentRole, InstalledVersionRole, InstalledRole) = \
range(Qt.UserRole, Qt.UserRole + 11)

_variant = QVariant()
_unknown_icons = []

class SearchThread(QThread):
    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.iface = parent.iface
        self.last_result = []

    def __del__(self):
        self.wait()

    def search(self, packages, criteria):
        self.packages = packages
        self.criteria = criteria
        self.start()

    def run(self):
        self.last_result = list(set(self.iface.search(self.criteria, self.packages)).intersection(self.packages))
        print self.last_result

class PackageModel(QAbstractTableModel):

    def __init__(self, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.iface = backend.pm.Iface()
        self._flags = Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsUserCheckable
        self.resetCachedInfos()
        self.cached_package = None
        self.packages = []
        self.state = parent.state

        # Search Thread Obj
        # FIXME TRY-EXCEPT
        self.searchThread = SearchThread(self)
        try:
            self.searchThread.finished.connect(lambda: parent.state.setCachedPackages(self.searchThread.last_result))
            self.searchThread.finished.connect(parent.initializeGroupList)
        except:
            pass

    def rowCount(self, index=QModelIndex()):
        return len(self.packages)

    def columnCount(self, index=QModelIndex()):
        if self._flags & Qt.ItemIsUserCheckable:
            return 2
        return 1

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return _variant

        if role == Qt.DisplayRole:
            return QVariant(self.packages[index.row()])
        elif role == Qt.CheckStateRole and index.column() == 0:
            return QVariant(self.package_selections[index.row()])

        if role >= Qt.UserRole:
            try:
                package = self.package(index)
            except Exception, e:
                logger.warning(e)
                return _variant

        if role == SummaryRole:
            return QVariant(unicode(package.summary))
        elif role == DescriptionRole:
            return QVariant(unicode(package.description))
        elif role == TypeRole:
            return QVariant(unicode(package._type))
        elif role == SizeRole:
            return QVariant(unicode(humanReadableSize(self.iface.getPackageSize(package.name))))
        elif role == VersionRole:
            return QVariant(unicode(package.version))
        elif role == InstalledVersionRole:
            if self.state.inUpgrade():
                return QVariant(unicode(self.iface.getInstalledVersion(package.name)))
            return _variant
        elif role == RepositoryRole:
            if not self.state.inRemove():
                return QVariant(unicode(self.iface.getPackageRepository(package.name)))
            return _variant
        elif role == HomepageRole:
            return QVariant(unicode(package.source.homepage))
        elif role == InstalledRole:
            return QVariant(unicode(package.installed))
        elif role == ComponentRole:
            return QVariant(unicode(package.partOf))
        elif role == Qt.DecorationRole:
            package = self.package(index)
            if package.icon:
                return QVariant(package.icon)
        return _variant

    def setData(self, index, value, role):
        if role == Qt.CheckStateRole and index.column() == 0:
            self.package_selections[index.row()] = value
            self.resetCachedInfos()
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index)
            return True
        else:
            return False

    def setCheckable(self, checkable):
        if checkable:
            self._flags |= Qt.ItemIsUserCheckable
        else:
            self._flags &= ~Qt.ItemIsUserCheckable

    def flags(self, index):
        if not index.isValid():
            return 0
        return self._flags

    def setPackages(self, packages):
        self.beginResetModel()
        self.cached_package = None
        self.packages = packages
        self.packages.sort(key=string.lower)
        self.package_selections = [Qt.Unchecked] * len(self.packages)
        self.endResetModel()

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
            self.cached_extras = self.iface.getExtras(self.selectedPackages(), self.state.getState())
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
        self.cached_package = None

    def selectPackages(self, packages):
        self.resetCachedInfos()
        for package in packages:
            self.package_selections[self.packages.index(package)] = Qt.Checked

    def reverseSelection(self, packages):
        self.resetCachedInfos()
        for package in packages:
            index = self.packages.index(package)
            self.package_selections[index] = Qt.Unchecked

    def search(self, text):
        # FIXME When instant search available from Pisi Api, we will use it.
        # packages = []
        # for word in text:
        #     packages += filter(lambda x: word in x, self.packages)
        # packages = list(set(packages))
        return list(set(self.iface.search(text, self.packages)).intersection(self.packages))
        # self.searchThread.search(self.packages, text)
        # return packages

    def downloadSize(self):
        try:
            return self.iface.calculate_download_size(self.selectedPackages() + self.extraPackages())
        except:
            return None


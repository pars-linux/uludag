#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file

from PyQt4 import QtGui
from PyQt4.QtCore import *

from packageproxy import PackageProxy
from packagemodel import PackageModel, GroupRole
from packagedelegate import PackageDelegate

from pmutils import *

from ui_basketdialog import Ui_BasketDialog

class BasketDialog(QtGui.QDialog, Ui_BasketDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.connect(self.packageList.model(), SIGNAL("dataChanged(QModelIndex,QModelIndex)"), self.filterExtras)
        self.model = None

    def setModel(self, model):
        self.model = model
        self.initPackageList()
        self.initExtraList()

    def __initList(self, packageList):
        packageList.setModel(PackageProxy(self))
        packageList.model().setSourceModel(self.model)
        packageList.setItemDelegate(PackageDelegate(self))
        packageList.setColumnWidth(0, 32)
        packageList.setAlternatingRowColors(True)
        packageList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        packageList.model().setFilterRole(GroupRole)

    def __updateList(self, packageList, packages):
        packageList.model().setFilterPackages(packages)
        packageList.model().reset()

    def initExtraList(self):
        self.__initList(self.extraList)
        self.__updateList(self.extraList, self.model.extraPackages())

    def initPackageList(self):
        self.__initList(self.packageList)
        self.__updateList(self.packageList, self.model.selectedPackages())

    def filterExtras(self):
        waitCursor()
        self.__updateList(self.extraList, self.model.extraPackages())
        restoreCursor()

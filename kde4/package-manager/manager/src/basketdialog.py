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
        self.model = None

    def setModel(self, model):
        self.model = model
        self.initPackageList()
        self.initExtraList()

    def initPackageList(self):
        self.packageList.setModel(PackageProxy(self))
        self.packageList.model().setSourceModel(self.model)
        self.packageList.setItemDelegate(PackageDelegate(self))
        self.packageList.setColumnWidth(0, 32)
        self.packageList.setAlternatingRowColors(True)
        self.packageList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.packageList.model().setFilterRole(GroupRole)
        packages = self.model.selectedPackages()
        self.packageList.model().setFilterPackages(packages)
        self.packageList.model().reset()
        self.connect(self.packageList.model(), SIGNAL("dataChanged(QModelIndex,QModelIndex)"), self.filterExtras)

    def filterExtras(self):
        waitCursor()
        packages = self.model.extraPackages()
        self.extraList.model().setFilterPackages(packages)
        self.extraList.model().reset()
        restoreCursor()

    def initExtraList(self):
        self.extraList.setModel(PackageProxy(self))
        self.extraList.model().setSourceModel(self.model)
        self.extraList.setItemDelegate(PackageDelegate(self))
        self.extraList.setColumnWidth(0, 32)
        self.extraList.setAlternatingRowColors(True)
        self.extraList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.extraList.model().setFilterRole(GroupRole)
        self.filterExtras()

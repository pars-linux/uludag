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
    def __init__(self, state):
        QtGui.QDialog.__init__(self, None)
        self.setupUi(self)
        self.state = state
        self.initPackageList()
        self.initExtraList()
        self.connect(self.packageList.model(), SIGNAL("dataChanged(QModelIndex,QModelIndex)"), self.filterExtras)
        self.connect(self.packageList.model(), SIGNAL("dataChanged(QModelIndex,QModelIndex)"), self.updateTotal)
        self.connect(self.actionButton, SIGNAL("clicked()"), self.action)

    def __initList(self, packageList):
        packageList.setModel(PackageProxy(self))
        packageList.setItemDelegate(PackageDelegate(self))
        packageList.setAlternatingRowColors(True)
        packageList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        packageList.model().setFilterRole(GroupRole)

    def __updateList(self, packageList, packages):
        packageList.model().setFilterPackages(packages)
        packageList.setColumnWidth(0, 32)

    def setModel(self, model):
        self.model = model
        self.packageList.model().setSourceModel(model)

    def initExtraList(self):
        self.__initList(self.extraList)
        self.extraList.model().setSourceModel(PackageModel(self))

    def initPackageList(self):
        self.__initList(self.packageList)
        self.__updateList(self.packageList, [])

    def filterExtras(self):
        waitCursor()
        extraPackages = self.model.extraPackages()
        self.extraList.model().sourceModel().setPackages(extraPackages)
        self.__updateList(self.extraList, extraPackages)
        self.extraList.setVisible(bool(extraPackages))
        self.extrasLabel.setVisible(bool(extraPackages))
        restoreCursor()

    def updateTotal(self):
        selectedSize, extraSize = self.model.selectedPackagesSize(), self.model.extraPackagesSize()
        self.totalSize.setText("<b>%s</b>" % humanReadableSize(selectedSize + extraSize))

    def setActionButton(self):
        self.actionButton.setText(self.state.getActionName())
        self.actionButton.setIcon(self.state.getActionIcon())

    def setBasketLabel(self):
        self.infoLabel.setText(self.state.getBasketInfo())
        self.extrasLabel.setText(self.state.getBasketExtrasInfo())

    def action(self):
        self.state.operationAction(self.model.selectedPackages())
        self.close()

    def show(self):
        waitCursor()
        self.__updateList(self.packageList, self.model.selectedPackages())
        self.filterExtras()
        self.updateTotal()
        self.setActionButton()
        self.setBasketLabel()
        restoreCursor()
        QtGui.QDialog.show(self)

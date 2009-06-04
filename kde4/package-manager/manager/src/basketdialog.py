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
    def __init__(self, state, model):
        QtGui.QDialog.__init__(self, None)
        self.setupUi(self)
        self.state = state
        self.model = model
        self.initPackageList()
        self.initExtraList()
        self.setActionButton()
        self.connect(self.packageList.model(), SIGNAL("dataChanged(QModelIndex,QModelIndex)"), self.filterExtras)
        self.connect(self.actionButton, SIGNAL("clicked()"), self.action)

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

    def initExtraList(self):
        self.__initList(self.extraList)
        self.filterExtras()

    def initPackageList(self):
        self.__initList(self.packageList)
        self.__updateList(self.packageList, self.model.selectedPackages())

    def filterExtras(self):
        waitCursor()
        extraPackages = self.model.extraPackages()
        if extraPackages:
            self.extraList.show()
            self.extrasLabel.show()
            self.__updateList(self.extraList, extraPackages)
        else:
            self.extraList.hide()
            self.extrasLabel.hide()
        restoreCursor()

    def setActionButton(self):
        self.actionButton.setText(self.state.getActionName())
        self.actionButton.setIcon(self.state.getActionIcon())

    def refresh(self):
        self.__updateList(self.packageList, self.model.selectedPackages())
        self.__updateList(self.extraList, self.model.extraPackages())

    def action(self):
        self.state.operationAction(self.model.selectedPackages())
        self.close()

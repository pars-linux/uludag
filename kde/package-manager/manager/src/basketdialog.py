#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file

from PyQt4 import QtGui
from PyQt4.QtCore import *

from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

from packagemodel import GroupRole
from packageproxy import PackageProxy
from packagemodel import PackageModel
from packagedelegate import PackageDelegate

from pds.gui import *
from pmutils import *

from ui_basketdialog import Ui_BasketDialog

class BasketDialog(PAbstractBox, Ui_BasketDialog):
    def __init__(self, state, parent):
        PAbstractBox.__init__(self, parent)
        self.state = state
        self.setupUi(self)
        self.parent = parent
        # PDS Settings
        self._animation = 1
        self._duration = 400
        self.last_msg = None
        self.enableOverlay()
        self._disable_parent_in_shown = True
        self.registerFunction(IN, lambda: parent.statusBar().hide())
        self.registerFunction(FINISHED, lambda: parent.statusBar().setVisible(not self.isVisible()))

        self.initPackageList()
        self.initExtraList()

        self.actionButton.clicked.connect(self.action)
        self.cancelButton.clicked.connect(self._hide)


    def _show(self):
        waitCursor()
        self.showHideDownloadInfo()
        self.__updateList(self.packageList, self.model.selectedPackages())
        try:
            self.filterExtras()
        except Exception, e:
            messageBox = QtGui.QMessageBox(i18n("Pisi Error"), unicode(e),
                    QtGui.QMessageBox.Critical, QtGui.QMessageBox.Ok, 0, 0)
            QTimer.singleShot(0, restoreCursor)
            messageBox.exec_()
            return
        self.updateTotal()
        self.setActionButton()
        self.setBasketLabel()
        self.connectModelSignals()
        QTimer.singleShot(0, restoreCursor)
        self.animate(start = BOTCENTER, stop = MIDCENTER)#, dont_animate = True)

    def _hide(self):
        self.disconnectModelSignals()
        self.animate(start = MIDCENTER, stop = BOTCENTER, direction = OUT)#, dont_animate = True)

    def connectModelSignals(self):
        self.connect(self.packageList.model(),
                SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                self.filterExtras)

        self.connect(self.packageList.model(),
                SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                self.updateTotal)

    def disconnectModelSignals(self):
        self.disconnect(self.packageList.model(),
                SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                self.filterExtras)

        self.disconnect(self.packageList.model(),
                SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                self.updateTotal)

    def __initList(self, packageList):
        packageList.setModel(PackageProxy(self))
        packageList.setItemDelegate(PackageDelegate(self))
        packageList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        packageList.model().setFilterRole(GroupRole)
        packageList.itemDelegate().setAnimatable(False)

    def __updateList(self, packageList, packages):
        packageList.model().reset()
        packageList.model().setFilterPackages(packages)
        packageList.setColumnWidth(0, 32)

    def setModel(self, model):
        self.model = model
        self.packageList.model().setSourceModel(model)

    def initExtraList(self):
        self.__initList(self.extraList)
        self.extraList.hideSelectAll()
        self.extraList.model().setSourceModel(PackageModel(self))
        self.extraList.model().sourceModel().setCheckable(False)

    def initPackageList(self):
        self.__initList(self.packageList)
        self.packageList.hideSelectAll()
        self.__updateList(self.packageList, [])

    def filterExtras(self):
        waitCursor()
        extraPackages = self.model.extraPackages()
        self.extraList.setPackages(extraPackages)
        self.__updateList(self.extraList, extraPackages)
        self.extraList.setVisible(bool(extraPackages))
        self.extrasLabel.setVisible(bool(extraPackages))
        restoreCursor()

    def updateTotal(self):
        selectedSize, extraSize = self.model.selectedPackagesSize(), \
                                  self.model.extraPackagesSize()
        self.totalSize.setText("<b>%s</b>" % humanReadableSize(
                                        selectedSize + extraSize))
        downloadSize = self.model.downloadSize()
        if not downloadSize:
            downloadSize = selectedSize + extraSize
        self.downloadSize.setText("<b>%s</b>" % humanReadableSize(
                                        downloadSize))

    def setActionButton(self):
        self.actionButton.setText(self.state.getActionName())
        self.actionButton.setIcon(self.state.getActionIcon())

    def setBasketLabel(self):
        self.infoLabel.setText(self.state.getBasketInfo())
        self.extrasLabel.setText(self.state.getBasketExtrasInfo())

    def setActionEnabled(self, enabled):
        self.actionButton.setEnabled(enabled)

    def askForActions(self, packages, reason, title):
        text = reason + '<br>'
        for package in packages:
            text += '<br> - <b>%s</b>' % package
        text += '<br><br>' + i18n("Do you want to continue ?")
        return QtGui.QMessageBox.question(self, title,
                text, QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

    def action(self):

        if self.state.inUpgrade():
            answer = QtGui.QMessageBox.Yes
            actions = self.state.checkUpdateActions(
                self.model.selectedPackages() + self.model.extraPackages())
            if actions[0]:
                answer = self.askForActions(actions[0],
                       i18n("You must <b>restart</b> your system for the "
                            "updates in the following package(s) to take "
                            "effect:"), i18n("Update Requirements"))
            if not answer == QtGui.QMessageBox.Yes:
                return
            if actions[1]:
                answer = self.askForActions(actions[1],
                    i18n("You must restart following system services for "
                         "the updated package(s) to take effect:"),
                    i18n("Update Requirements"))
            if not answer == QtGui.QMessageBox.Yes:
                return

        if self.state.inRemove():
            answer = QtGui.QMessageBox.Yes
            actions = self.state.checkRemoveActions(
                self.model.selectedPackages() + self.model.extraPackages())
            if actions:
                answer = self.askForActions(actions,
                       i18n("Selected packages are considered critical "
                            "for the system. Removing them may cause your "
                            "system to be unusable."),
                       i18n("Warning"))
            if not answer == QtGui.QMessageBox.Yes:
                return

        reinstall = False
        if self.state.inInstall():
            answer = QtGui.QMessageBox.Yes
            actions = self.state.checkInstallActions(
                self.model.selectedPackages() + self.model.extraPackages())
            if actions:
                answer = self.askForActions(actions,
                       i18n("Selected packages are already installed "
                            "If you continue, packages will be reinstalled"),
                       i18n("Already Installed Packages"))
            if not answer == QtGui.QMessageBox.Yes:
                return
            if actions:
                reinstall = True

        self.state.operationAction(self.model.selectedPackages(), reinstall = reinstall)

    def showHideDownloadInfo(self):
        if self.state.state == self.state.REMOVE:
            self.downloadSize.hide()
            self.downloadSizeLabel.hide()
        else:
            self.downloadSize.show()
            self.downloadSizeLabel.show()



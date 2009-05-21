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

from PyQt4 import QtGui
from PyQt4.QtCore import *

from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

from ui_mainwindow import Ui_MainWindow

from mainwidget import MainWidget
from statemanager import StateManager

class MainWindow(KMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        KMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.setCentralWidget(MainWidget(self))
        self.connect(self.centralWidget(), SIGNAL("selectionChanged(QModelIndexList)"), self.updateStatusBar)
        self.statusBar().showMessage(i18n("Currently your basket is empty."))
        self.initializeActions()

    def initializeActions(self):
        self.toolBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        showInstallAction = KToggleAction(KIcon("list-add"), i18n("Show New Packages"), self.toolBar)
        self.connect(showInstallAction, SIGNAL("triggered()"), lambda:self.centralWidget().switchState(StateManager.INSTALL))
        self.connect(showInstallAction, SIGNAL("triggered()"), self.centralWidget().initialize)
        showRemoveAction = KToggleAction(KIcon("list-remove"), i18n("Show Installed Packages"), self.toolBar)
        self.connect(showRemoveAction, SIGNAL("triggered()"), lambda:self.centralWidget().switchState(StateManager.REMOVE))
        self.connect(showRemoveAction, SIGNAL("triggered()"), self.centralWidget().initialize)
        showUpgradeAction = KToggleAction(KIcon("view-refresh"), i18n("Show Upgradable Packages"), self.toolBar)
        self.connect(showUpgradeAction, SIGNAL("triggered()"), lambda:self.centralWidget().switchState(StateManager.UPGRADE))

        actionGroup = QtGui.QActionGroup(self.toolBar)
        for action in [showInstallAction, showRemoveAction, showUpgradeAction]:
            actionGroup.addAction(action)
            self.toolBar.addAction(action)
            self.menu_File.addAction(action)

        showInstallAction.setChecked(True)

    def updateStatusBar(self, indexes):
        pass

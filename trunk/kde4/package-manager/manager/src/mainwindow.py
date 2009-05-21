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

class MainWindow(KXmlGuiWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        KXmlGuiWindow.__init__(self, parent)
        self.setupUi(self)
        self.setCentralWidget(MainWidget(self))
        self.connect(self.centralWidget(), SIGNAL("selectionChanged(QModelIndexList)"), self.updateStatusBar)
        self.statusBar().showMessage(i18n("Currently your basket is empty."))
        self.initializeActions()

    def initializeActions(self):
        KStandardAction.quit(KApplication.kApplication().quit, self.actionCollection())
        actionGroup = QtGui.QActionGroup(self)

        showInstallAction = KToggleAction(KIcon("list-add"), i18n("Show New Packages"), self)
        actionGroup.addAction(showInstallAction)
        self.actionCollection().addAction("showInstallAction", showInstallAction)
        self.connect(showInstallAction, SIGNAL("triggered()"), lambda:self.centralWidget().switchState(StateManager.INSTALL))
        self.connect(showInstallAction, SIGNAL("triggered()"), self.centralWidget().initialize)

        showRemoveAction = KToggleAction(KIcon("list-remove"), i18n("Show Installed Packages"), self)
        actionGroup.addAction(showRemoveAction)
        self.actionCollection().addAction("showRemoveAction", showRemoveAction)
        self.connect(showRemoveAction, SIGNAL("triggered()"), lambda:self.centralWidget().switchState(StateManager.REMOVE))
        self.connect(showRemoveAction, SIGNAL("triggered()"), self.centralWidget().initialize)

        showUpgradeAction = KToggleAction(KIcon("view-refresh"), i18n("Show Upgradable Packages"), self)
        actionGroup.addAction(showUpgradeAction)
        self.actionCollection().addAction("showUpgradeAction", showUpgradeAction)
        self.connect(showUpgradeAction, SIGNAL("triggered()"), lambda:self.centralWidget().switchState(StateManager.UPGRADE))

        self.setupGUI(KXmlGuiWindow.Default, "data/packagemanagerui.rc")

        self.toolBar().setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        showInstallAction.setChecked(True)

    def updateStatusBar(self, indexes):
        pass

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
from settingsdialog import SettingsDialog
from tray import Tray

class MainWindow(KXmlGuiWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        KXmlGuiWindow.__init__(self, parent)
        self.setupUi(self)
        self.setCentralWidget(MainWidget(self))
        self.settingsDialog = SettingsDialog(self)
        self.initializeActions()
        self.initializeStatusBar()
        self.initializeTray()
        self.connectMainSignals()

    def connectMainSignals(self):
        self.connect(self.settingsDialog, SIGNAL("settingsChanged()"), self.centralWidget().initialize)

    def initializeTray(self):
        self.tray = Tray(self)
        self.tray.show()

    def initializeStatusBar(self):
        self.statusLabel = QtGui.QLabel(i18n("Currently your basket is empty."), self.statusBar())
        self.statusLabel.setAlignment(Qt.AlignCenter)
        self.statusBar().addWidget(self.statusLabel)
        self.statusBar().setSizeGripEnabled(True)
        self.wheelMovie = QtGui.QMovie(self)
        self.statusLabel.setText(i18n("Currently your basket is empty."))
        self.wheelMovie.setFileName(":/data/wheel.mng")
        self.connect(self.centralWidget(), SIGNAL("selectionStatusChanged(QString)"), self.updateStatusBar)
        self.connect(self.centralWidget(), SIGNAL("updatingStatus()"), self.statusWaiting)

    def initializeActions(self):
        self.toolBar().setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        KStandardAction.quit(KApplication.kApplication().quit, self.actionCollection())
        KStandardAction.preferences(self.settingsDialog.show, self.actionCollection())

        self.initializeOperationActions()
        self.setupGUI(KXmlGuiWindow.Default, "data/packagemanagerui.rc")

    def initializeOperationActions(self):
        actionGroup = QtGui.QActionGroup(self)

        showInstallAction = KToggleAction(KIcon("list-add"), i18n("Show Installable Packages"), self)
        showInstallAction.setChecked(True)
        self.actionCollection().addAction("showInstallAction", showInstallAction)
        self.connect(showInstallAction, SIGNAL("triggered()"), lambda:self.centralWidget().switchState(StateManager.INSTALL))
        self.connect(showInstallAction, SIGNAL("triggered()"), self.centralWidget().initialize)
        actionGroup.addAction(showInstallAction)

        showRemoveAction = KToggleAction(KIcon("list-remove"), i18n("Show Installed Packages"), self)
        self.actionCollection().addAction("showRemoveAction", showRemoveAction)
        self.connect(showRemoveAction, SIGNAL("triggered()"), lambda:self.centralWidget().switchState(StateManager.REMOVE))
        self.connect(showRemoveAction, SIGNAL("triggered()"), self.centralWidget().initialize)
        actionGroup.addAction(showRemoveAction)

        showUpgradeAction = KToggleAction(KIcon("view-refresh"), i18n("Show Upgradable Packages"), self)
        self.actionCollection().addAction("showUpgradeAction", showUpgradeAction)
        self.connect(showUpgradeAction, SIGNAL("triggered()"), lambda:self.centralWidget().switchState(StateManager.UPGRADE))
        actionGroup.addAction(showUpgradeAction)

    def statusWaiting(self):
        self.statusLabel.setMovie(self.wheelMovie)
        self.wheelMovie.start()

    def updateStatusBar(self, text):
        self.wheelMovie.stop()
        self.statusLabel.setText(text)

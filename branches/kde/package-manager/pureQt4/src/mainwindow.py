#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2010, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import SIGNAL

from ui_mainwindow import Ui_MainWindow

from mainwidget import MainWidget
from statemanager import StateManager
from settingsdialog import SettingsDialog
from tray import Tray

import helpdialog
import backend
import config

from context import *

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, app = None):
        QtGui.QMainWindow.__init__(self, None)
        self.setupUi(self)
        self.app = app
        self.iface = backend.pm.Iface()
        self.setWindowIcon(QtGui.QIcon(":/data/package-manager.png"))
        self.setCentralWidget(MainWidget(self))
        self.settingsDialog = SettingsDialog(self)
        self.initializeActions()
        self.initializeStatusBar()
        self.initializeTray()
        self.connectMainSignals()

    def connectMainSignals(self):
        self.connect(self.settingsDialog, SIGNAL("packagesChanged()"), self.centralWidget().initialize)
        self.connect(self.settingsDialog, SIGNAL("traySettingChanged()"), self.tray.settingsChanged)
        self.connect(self.centralWidget().state, SIGNAL("repositoriesChanged()"), self.tray.populateRepositoryMenu)
        self.connect(self.app, SIGNAL("aboutToQuit()"), self.slotQuit)

    def initializeTray(self):
        self.tray = Tray(self, self.iface)
        self.connect(self.centralWidget().operation, SIGNAL("finished(QString)"), self.trayAction)
        self.connect(self.tray, SIGNAL("showUpdatesSelected()"), self.trayShowUpdates)

    def trayShowUpdates(self):
        self.showUpgradeAction.setChecked(True)
        self.centralWidget().switchState(StateManager.UPGRADE, action=False)
        self.centralWidget().initialize()
        self.show()
        self.raise_()

    def trayAction(self, operation):
        if not self.isVisible() and operation in ["System.Manager.updateRepository", "System.Manager.updateAllRepositories"]:
            self.tray.showPopup()
        if self.tray.isVisible() and operation in ["System.Manager.updatePackage",
                                                   "System.Manager.installPackage",
                                                   "System.Manager.removePackage"]:
            self.tray.updateTrayUnread()

    def initializeStatusBar(self):
        self.statusLabel = QtGui.QLabel(i18n("Currently your basket is empty."), self.statusBar())
        self.statusLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.statusBar().addWidget(self.statusLabel)
        self.statusBar().setSizeGripEnabled(True)
        self.wheelMovie = QtGui.QMovie(self)
        self.statusLabel.setText(i18n("Currently your basket is empty."))
        self.wheelMovie.setFileName(":/data/wheel.mng")
        self.connect(self.centralWidget(), SIGNAL("selectionStatusChanged(QString)"), self.updateStatusBar)
        self.connect(self.centralWidget(), SIGNAL("updatingStatus()"), self.statusWaiting)

    def initializeActions(self):
        self.toolBar = QtGui.QToolBar(self)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.initializeOperationActions()

    def initializeOperationActions(self):
        actionGroup = QtGui.QActionGroup(self)

        self.menubar = QtGui.QMenuBar(self)

        self.menuFile = QtGui.QMenu(i18n('File'), self.menubar)
        self.menuOptions = QtGui.QMenu(i18n('Settings'), self.menubar)
        self.menuHelp = QtGui.QMenu(i18n('Help'), self.menubar)

        self.quitAppAction = QtGui.QAction(KIcon(('exit', 'application-exit')), i18n("Quit"), self)
        self.quitAppAction.setShortcut(QtGui.QKeySequence('Ctrl+q'))
        self.quitAppAction.triggered.connect(self.slotQuit)

        self.helpAppAction = QtGui.QAction(KIcon(('help', 'help-contents')), i18n("Help"), self)
        self.helpAppAction.setShortcut(QtGui.QKeySequence('F1'))
        self.helpAppAction.triggered.connect(self.showHelp)
        self.menuHelp.addAction(self.helpAppAction)

        self.setMenuBar(self.menubar)

        # Action Show Installable Packages
        self.showInstallAction = QtGui.QAction(KIcon("list-add"),
                          i18n("Show Installable Packages"), self)
        self.showInstallAction.setCheckable(True)
        self.showInstallAction.setChecked(True)
        self.showInstallAction.triggered.connect(lambda:self.centralWidget().switchState(StateManager.INSTALL))
        self.showInstallAction.triggered.connect(self.centralWidget().initialize)
        actionGroup.addAction(self.showInstallAction)
        self.toolBar.addAction(self.showInstallAction)
        self.menuFile.addAction(self.showInstallAction)

        # Action Show Installed Packages
        self.showRemoveAction = QtGui.QAction(KIcon("list-remove"),
                          i18n("Show Installed Packages"), self)
        self.showRemoveAction.setCheckable(True)
        self.showRemoveAction.triggered.connect(lambda:self.centralWidget().switchState(StateManager.REMOVE))
        self.showRemoveAction.triggered.connect(self.centralWidget().initialize)
        actionGroup.addAction(self.showRemoveAction)
        self.toolBar.addAction(self.showRemoveAction)
        self.menuFile.addAction(self.showRemoveAction)

        # Action Show Upgradable Packages
        self.showUpgradeAction = QtGui.QAction(KIcon("view-refresh"),
                          i18n("Show Upgradable Packages"), self)
        self.showUpgradeAction.setCheckable(True)
        self.showUpgradeAction.triggered.connect(lambda:self.centralWidget().switchState(StateManager.UPGRADE))
        self.showUpgradeAction.triggered.connect(self.centralWidget().initialize)
        actionGroup.addAction(self.showUpgradeAction)
        self.toolBar.addAction(self.showUpgradeAction)
        self.menuFile.addAction(self.showUpgradeAction)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.quitAppAction)

        self.showSettingsAction = QtGui.QAction(KIcon("preferences-system"),
                          i18n("Package Manager Settings"), self)
        self.showSettingsAction.triggered.connect(self.showSettingsDialog)
        self.menuOptions.addAction(self.showSettingsAction)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

    def showSettingsDialog(self):
        self.settingsDialog.show()

    def statusWaiting(self):
        self.statusLabel.setMovie(self.wheelMovie)
        self.wheelMovie.start()

    def updateStatusBar(self, text):
        self.wheelMovie.stop()
        self.statusLabel.setText(text)

    def queryClose(self):
        if config.PMConfig().systemTray():
            self.hide()
            return False
        return True

    def showHelp(self):
        helpDialog = helpdialog.HelpDialog(self, helpdialog.MAINAPP)
        helpDialog.show()

    def queryExit(self):
        if not self.iface.operationInProgress():
            if self.tray.notification:
                self.tray.notification.close()
            return True
        return False

    def slotQuit(self):
        if self.iface.operationInProgress():
            return
        QtCore.QCoreApplication.quit()


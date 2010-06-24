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
from PyKDE4.kio import KFileDialog, KFile  # to open an open dialog for importing index action

from ui_mainwindow import Ui_MainWindow

from mainwidget import MainWidget
from statemanager import StateManager
from settingsdialog import SettingsDialog
from offlinemanager import OfflineManager
from sessionmanager import SessionManager
from tray import Tray

import backend
import config

class MainWindow(KXmlGuiWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        KXmlGuiWindow.__init__(self, parent)
        self.setupUi(self)
        self.setWindowIcon(KIcon(":/data/package-manager.png"))
        self.setCentralWidget(MainWidget(self))
        self.settingsDialog = SettingsDialog(self)
        self.initializeActions()
        self.initializeStatusBar()
        self.initializeTray()
        self.connectMainSignals()
        
        self.offlinemanager = OfflineManager()
        self.connectOfflineSignals()

    def connectMainSignals(self):
        self.connect(self, SIGNAL("packagesChanged()"), self.centralWidget().initialize)
        self.connect(self.settingsDialog, SIGNAL("packagesChanged()"), self.centralWidget().initialize)
        self.connect(self.settingsDialog, SIGNAL("traySettingChanged()"), self.tray.settingsChanged)
        self.connect(self.centralWidget().state, SIGNAL("repositoriesChanged()"), self.tray.populateRepositoryMenu)
        self.connect(KApplication.kApplication(), SIGNAL("shutDown()"), self.slotQuit)

    def connectOfflineSignals(self):
        self.connect(self, SIGNAL("importIndex(str)"), self.offlinemanager.importIndex)
        self.connect(self, SIGNAL("exportIndex(str)"), self.offlinemanager.exportIndex)
        self.connect(self, SIGNAL("openSession(str)"), self.offlinemanager.openSession)
        self.connect(self, SIGNAL("saveSession(str)"), self.offlinemanager.saveSession)

    def initializeTray(self):
        self.tray = Tray(self)
        self.connect(self.centralWidget().operation, SIGNAL("finished(QString)"), self.trayShow)
        self.connect(self.tray, SIGNAL("showUpdatesSelected()"), self.trayShowUpdates)

    def trayShowUpdates(self):
        self.showUpgradeAction.setChecked(True)
        self.centralWidget().switchState(StateManager.UPGRADE, action=False)
        self.centralWidget().initialize()
        KApplication.kApplication().updateUserTimestamp()
        self.show()
        self.raise_()

    def trayShow(self, operation):
        if not self.isVisible() and operation in ["System.Manager.updateRepository", "System.Manager.updateAllRepositories"]:
            self.tray.showPopup()

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

        self.showInstallAction = KToggleAction(KIcon("list-add"), i18n("Show Installable Packages"), self)
        self.showInstallAction.setChecked(True)
        self.actionCollection().addAction("showInstallAction", self.showInstallAction)
        self.connect(self.showInstallAction, SIGNAL("triggered()"), lambda:self.centralWidget().switchState(StateManager.INSTALL))
        self.connect(self.showInstallAction, SIGNAL("triggered()"), self.centralWidget().initialize)
        actionGroup.addAction(self.showInstallAction)

        self.showRemoveAction = KToggleAction(KIcon("list-remove"), i18n("Show Installed Packages"), self)
        self.actionCollection().addAction("showRemoveAction", self.showRemoveAction)
        self.connect(self.showRemoveAction, SIGNAL("triggered()"), lambda:self.centralWidget().switchState(StateManager.REMOVE))
        self.connect(self.showRemoveAction, SIGNAL("triggered()"), self.centralWidget().initialize)
        actionGroup.addAction(self.showRemoveAction)

        self.showUpgradeAction = KToggleAction(KIcon("view-refresh"), i18n("Show Upgradable Packages"), self)
        self.actionCollection().addAction("showUpgradeAction", self.showUpgradeAction)
        self.connect(self.showUpgradeAction, SIGNAL("triggered()"), lambda:self.centralWidget().switchState(StateManager.UPGRADE))
        actionGroup.addAction(self.showUpgradeAction)

        self.importIndexAction = KToggleAction(KIcon("list-add"), i18n("Import Index"), self)
        self.actionCollection().addAction("importIndexAction", self.importIndexAction)
        self.connect(self.importIndexAction, SIGNAL("triggered()"), self.importIndex)

        self.exportIndexAction = KToggleAction(KIcon("list-remove"), i18n("Export Index"), self)
        self.actionCollection().addAction("exportIndexAction", self.exportIndexAction)
        self.connect(self.exportIndexAction, SIGNAL("triggered()"), self.exportIndex)

        self.openSessionAction = KToggleAction(KIcon("list-add"), i18n("Open Session"), self)
        self.actionCollection().addAction("openSessionAction", self.openSessionAction)
        self.connect(self.openSessionAction, SIGNAL("triggered()"), self.openSession)

        self.saveSessionAction = KToggleAction(KIcon("list-remove"), i18n("Save Session"), self)
        self.actionCollection().addAction("saveSessionAction", self.saveSessionAction)
        self.connect(self.saveSessionAction, SIGNAL("triggered()"), self.saveSession)

    def statusWaiting(self):
        self.statusLabel.setMovie(self.wheelMovie)
        self.wheelMovie.start()

    def updateStatusBar(self, text):
        self.wheelMovie.stop()
        self.statusLabel.setText(text)

    def queryClose(self):
        if config.PMConfig().systemTray() and not KApplication.kApplication().sessionSaving():
            self.hide()
            return False
        return True

    def queryExit(self):
        if not backend.pm.Iface().operationInProgress():
            if self.tray.notification:
                self.tray.notification.close()
            return True
        return False

    def slotQuit(self):
        if backend.pm.Iface().operationInProgress():
            return

    def switchSession(self, session):
        self.centralWidget().switchSession(session)
        self.showInstallAction.setChecked(True)

    def importIndex(self):
        filename = str(KFileDialog.getOpenFileName(KUrl("pisi-installed"), "*.xml", self, i18n("Import index file")))

        if filename:
            self.switchSession(SessionManager.OFFLINE)
            self.emit(SIGNAL("importIndex(str)"), filename)
            self.emit(SIGNAL("packagesChanged()"))

    def exportIndex(self):
        filename = str(KFileDialog.getSaveFileName(KUrl("pisi-installed"), "*.xml", self, i18n("Export index file")))

        if filename:
            self.emit(SIGNAL("exportIndex(str)"), filename)

    def openSession(self):
        filename = str(KFileDialog.getOpenFileName(KUrl("pisi-archive"), "*.offline", self, i18n("Open offline session")))

        if filename:
            self.emit(SIGNAL("openSession(str)"), filename)

    def saveSession(self):
        filename = str(KFileDialog.getSaveFileName(KUrl("pisi-archive"), "*.offline", self, i18n("Save offline session")))

        if filename:
            self.emit(SIGNAL("saveSession(str)"), filename)
            self.switchSession(SessionManager.NORMAL)

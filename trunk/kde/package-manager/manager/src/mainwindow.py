#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009-2010, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

from PyQt4 import QtGui
from PyQt4.QtGui import QLabel
from PyQt4.QtCore import *

from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

from ui_mainwindow import Ui_MainWindow

from mainwidget import MainWidget
from statemanager import StateManager
from settingsdialog import SettingsDialog
from tray import Tray

import backend
import config
import context
from context import _time

class MainWindow(KXmlGuiWindow, Ui_MainWindow):
    def __init__(self, app = None):
        KXmlGuiWindow.__init__(self, None)
        self.setupUi(self)

        self.app = app
        self.iface = backend.pm.Iface()

        self.setWindowIcon(KIcon(":/data/package-manager.png"))

        self.setCentralWidget(MainWidget(self))
        self.sw = self.centralWidget()

        self.settingsDialog = SettingsDialog(self)

        self.initializeActions()
        self.initializeStatusBar()
        self.initializeTray()
        self.connectMainSignals()

    def connectMainSignals(self):
        self.connect(self.settingsDialog, SIGNAL("packagesChanged()"), self.sw.initialize)
        self.connect(self.settingsDialog, SIGNAL("packageViewChanged()"), self.sw.updateSettings)
        self.connect(self.settingsDialog, SIGNAL("traySettingChanged()"), self.tray.settingsChanged)
        self.connect(self.sw.state, SIGNAL("repositoriesChanged()"), self.tray.populateRepositoryMenu)
        self.connect(self.sw, SIGNAL("repositoriesUpdated()"), self.tray.updateTrayUnread)
        self.connect(KApplication.kApplication(), SIGNAL("shutDown()"), self.slotQuit)

    def initializeTray(self):
        self.tray = Tray(self, self.iface)
        self.connect(self.sw.operation, SIGNAL("finished(QString)"), self.trayAction)
        self.connect(self.sw.operation, SIGNAL("finished(QString)"), self.tray.stop)
        self.connect(self.sw.operation, SIGNAL("operationCancelled()"), self.tray.stop)
        self.connect(self.sw.operation, SIGNAL("started(QString)"), self.tray.animate)
        self.connect(self.tray, SIGNAL("showUpdatesSelected()"), self.trayShowUpdates)

    def trayShowUpdates(self):
        self.showUpgradeAction.setChecked(True)

        self.sw.switchState(StateManager.UPGRADE, action=False)
        self.sw.initialize()

        KApplication.kApplication().updateUserTimestamp()

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
        sb = self.statusBar()
        sb.addPermanentWidget(self.sw.actions, 1)

        self.wheelMovie = QtGui.QMovie(self)
        self.updateStatusBar('')
        self.wheelMovie.setFileName(":/data/wheel.mng")

        self.connect(self.sw, SIGNAL("selectionStatusChanged(QString)"), self.updateStatusBar)
        self.connect(self.sw, SIGNAL("updatingStatus()"), self.statusWaiting)

    def initializeActions(self):
        self.toolBar().setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        KStandardAction.quit(KApplication.kApplication().quit, self.actionCollection())
        KStandardAction.preferences(self.settingsDialog.show, self.actionCollection())
        self.initializeOperationActions()
        self.setupGUI(KXmlGuiWindow.Default, "/usr/share/package-manager/data/packagemanagerui.rc")

    def initializeOperationActions(self):
        actionGroup = QtGui.QActionGroup(self)

        self.showInstallAction = KToggleAction(KIcon("list-add"), i18n("Show Installable Packages"), self)
        self.actionCollection().addAction("showInstallAction", self.showInstallAction)
        self.connect(self.showInstallAction, SIGNAL("triggered()"), lambda:self.sw.switchState(StateManager.INSTALL))
        self.sw.stateCombo.addItem(KIcon("view-refresh"), i18n("Show Installable Packages"))
        actionGroup.addAction(self.showInstallAction)

        self.showRemoveAction = KToggleAction(KIcon("list-remove"), i18n("Show Installed Packages"), self)
        self.actionCollection().addAction("showRemoveAction", self.showRemoveAction)
        self.connect(self.showRemoveAction, SIGNAL("triggered()"), lambda:self.sw.switchState(StateManager.REMOVE))
        self.sw.stateCombo.addItem(KIcon("list-remove"), i18n("Show Installed Packages"))
        actionGroup.addAction(self.showRemoveAction)

        self.showUpgradeAction = KToggleAction(KIcon("view-refresh"), i18n("Show Upgradable Packages"), self)
        self.actionCollection().addAction("showUpgradeAction", self.showUpgradeAction)
        self.connect(self.showUpgradeAction, SIGNAL("triggered()"), lambda:self.sw.switchState(StateManager.UPGRADE))
        self.sw.stateCombo.addItem(KIcon("list-add"), i18n("Show Upgradable Packages"))
        actionGroup.addAction(self.showUpgradeAction)

        self.showInstallAction.setChecked(True)

    def statusWaiting(self):
        self.sw.busyIndicator.setMovie(self.wheelMovie)
        self.sw.statusLabel.setText(i18n('Busy ...'))
        self.statusBar().show()
        self.wheelMovie.start()

    def updateStatusBar(self, text):
        self.wheelMovie.stop()
        self.sw.statusLabel.setText(text)
        if text == '':
            self.statusBar().hide()
        else:
            self.statusBar().show()

    def queryClose(self):
        if config.PMConfig().systemTray() and not KApplication.kApplication().sessionSaving():
            self.hide()
            return False
        return True

    def queryExit(self):
        if not self.iface.operationInProgress():
            if self.tray:
                del self.tray.notification
            return True
        return False

    def slotQuit(self):
        if self.iface.operationInProgress():
            return

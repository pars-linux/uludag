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
from tray import Tray
from backend.pisi.operations import Operations

import backend
import config

import pisi

class MainWindow(KXmlGuiWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        KXmlGuiWindow.__init__(self, parent)
        self.setupUi(self)
        self.iface = backend.pm.Iface()
        self.setWindowIcon(KIcon(":/data/package-manager.png"))
        self.setCentralWidget(MainWidget(self))
        self.settingsDialog = SettingsDialog(self)
        self.offlineOperations = Operations()
        self.initializeActions()
        self.initializeStatusBar()
        self.initializeTray()
        self.connectMainSignals()

    def connectMainSignals(self):
        self.connect(self.settingsDialog, SIGNAL("packagesChanged()"), self.centralWidget().initialize)
        self.connect(self.settingsDialog, SIGNAL("traySettingChanged()"), self.tray.settingsChanged)
        self.connect(self.centralWidget().state, SIGNAL("repositoriesChanged()"), self.tray.populateRepositoryMenu)
        self.connect(KApplication.kApplication(), SIGNAL("shutDown()"), self.slotQuit)

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

        self.importIndexAction = KToggleAction(KIcon("list-add"), "Import Index", self)
        self.actionCollection().addAction("importIndexAction", self.importIndexAction)
        #self.connect(self.importIndexAction, SIGNAL("triggered()"), lambda:self.centralWidget().switchState(StateManager.OFFLINE))
        self.connect(self.importIndexAction, SIGNAL("triggered()"), self.importIndex)
        #actionGroup.addAction(self.importIndexAction)

        self.exportIndexAction = KToggleAction(KIcon("list-remove"), "Export Index", self)
        self.actionCollection().addAction("exportIndexAction", self.exportIndexAction)
        #self.connect(self.exportIndexAction, SIGNAL("triggered()"), lambda:self.centralWidget().switchState(StateManager.INSTALL))
        self.connect(self.exportIndexAction, SIGNAL("triggered()"), self.importIndex)
        #actionGroup.addAction(self.exportIndexAction)

        self.importOfflineJobsAction = KToggleAction(KIcon("list-add"), "Import Offline Jobs", self)
        self.actionCollection().addAction("importOfflineJobsAction", self.importOfflineJobsAction)
        self.connect(self.importOfflineJobsAction, SIGNAL("trigged()"), self.importOfflineJobs)

        self.closeOfflineModeAction = KToggleAction(KIcon("list-remove"), "Close Offline Mode", self)
        self.actionCollection().addAction("closeOfflineModeAction", self.closeOfflineModeAction)
        self.connect(self.closeOfflineModeAction, SIGNAL("triggered()"), self.closeOfflineModer)

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
        if not self.iface.operationInProgress():
            if self.tray.notification:
                self.tray.notification.close()
            return True
        return False

    def slotQuit(self):
        if self.iface.operationInProgress():
            return

    def importIndex(self):
        print "Hello world"
        filename = KFileDialog.getOpenFileName(KUrl("."), "*.xml", self, i18n("Select project file"))
        if filename:
            print filename

    def exportIndex(self):
        idb = pisi.db.installdb.InstallDB()
        idb.list_installed()
        for name in idb.list_installed():
            pkg = idb.get_package(name)
            pkg
        index = pisi.index.Index()
        for name in idb.list_installed():
            index.packages.append(idb.get_package(name))
        #for name in idb.list_installed():
        #    index.add_package(idb.get_package(name))
        index.add_components("/home/volkan/components.xml")
        index.add_groups("/home/volkan/groups.xml")
        index.add_distro("/home/volkan/distribution.xml")
        index.write("/home/volkan/pisi-installed.xml.bz2", sha1sum=True, compress=pisi.file.File.bz2, sign=None)

    def importOfflineJobs(self):
        print "Offline jobs are running..."
        filename = KFileDialog.getOpenFileName(KUrl("pisi_files"), "*.tar", self, i18n("Select project file"))
        print filename

    def closeOfflineModer(self):
        filename = KFileDialog.getSaveFileName(KUrl("pisi_files"), "*.tar", self, i18n("Select project file"))
        self.offlineOperations.closeOfflineMode(filename)

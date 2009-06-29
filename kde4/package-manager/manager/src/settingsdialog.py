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

from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

from ui_settingsdialog import Ui_SettingsDialog

import config
import helpdialog
import repodialog
import backend

class SettingsTab(QObject):
    def __init__(self, settings):
        self.settings = settings
        self.config = config.PMConfig()
        self.iface = backend.pm.Iface()
        self.setupUi()
        self.connectSignals()
        self.changed = False

    def markChanged(self):
        self.changed = True

    def setupUi(self):
        pass

    def connectSignals(self):
        pass

    def save(self):
        pass

class GeneralSettings(SettingsTab):
    def setupUi(self):
        self.settings.moveUpButton.setIcon(KIcon("arrow-up"))
        self.settings.moveDownButton.setIcon(KIcon("arrow-down"))
        self.settings.addRepoButton.setIcon(KIcon("list-add"))
        self.settings.removeRepoButton.setIcon(KIcon("list-remove"))

        self.settings.onlyGuiApp.setChecked(self.config.showOnlyGuiApp())
        self.settings.intervalCheck.setChecked(self.config.updateCheck())
        self.settings.intervalSpin.setValue(self.config.updateCheckInterval())
        self.settings.systemTray.setChecked(self.config.systemTray())
        self.__getBandwidthSettings()

    def __getBandwidthSettings(self):
        config = self.iface.getConfig()
        bandwidth_limit = config.get("general", "bandwidth_limit")
        bandwidth_limit = int(bandwidth_limit) if bandwidth_limit else 0

        if bandwidth_limit != 0:
            self.settings.useBandwidthLimit.setChecked(True)

        self.settings.bandwidthSpin.setValue(bandwidth_limit)

    def connectSignals(self):
        self.connect(self.settings.onlyGuiApp, SIGNAL("toggled(bool)"), self.markChanged)
        self.connect(self.settings.intervalCheck, SIGNAL("toggled(bool)"), self.markChanged)
        self.connect(self.settings.useBandwidthLimit, SIGNAL("toggled(bool)"), self.markChanged)
        self.connect(self.settings.intervalSpin, SIGNAL("valueChanged(int)"), self.markChanged)
        self.connect(self.settings.systemTray, SIGNAL("toggled(bool)"), self.markChanged)
        self.connect(self.settings.bandwidthSpin, SIGNAL("valueChanged(int)"), self.markChanged)

    def save(self):
        self.config.setShowOnlyGuiApp(self.settings.onlyGuiApp.isChecked())
        self.config.setSystemTray(self.settings.systemTray.isChecked())
        self.config.setUpdateCheck(self.settings.intervalCheck.isChecked())
        self.config.setUpdateCheckInterval(self.settings.intervalSpin.value())

        if self.settings.useBandwidthLimit.isChecked():
            self.iface.setConfig("general", "bandwidth_limit", str(self.settings.bandwidthSpin.value()))
        else:
            self.iface.setConfig("general", "bandwidth_limit", "0")

class CacheSettings(SettingsTab):
    def setupUi(self):
        self.__getCacheSettings()

    def __getCacheSettings(self):
        config = self.iface.getConfig()

        cache = config.get("general", "package_cache")
        cache_limit = config.get("general", "package_cache_limit")
        cache_limit = int(cache_limit) if cache_limit else 0

        # If pisi.conf does not have it yet, default is use package cache
        if not cache or cache == "True":
            enableCache = True
        else:
            enableCache = False

        self.cacheEnabled = enableCache
        self.cacheSize = cache_limit
        self.settings.useCacheCheck.setChecked(enableCache)
        self.settings.useCacheSpin.setValue(cache_limit)

    def connectSignals(self):
        self.connect(self.settings.clearCacheButton, SIGNAL("clicked()"), self.clearCache)
        self.connect(self.settings.useCacheCheck, SIGNAL("toggled(bool)"), self.markChanged)
        self.connect(self.settings.useCacheSpin, SIGNAL("valueChanged(int)"), self.markChanged)

    def clearCache(self):
        if KMessageBox.Yes == KMessageBox.warningYesNo(self.settings,
                                                       i18n("All the cached packages will be deleted. Are you sure? "),
                                                       i18n("Warning"),
                                                       KGuiItem(i18n("Delete"), "trash-empty"),
                                                       KStandardGuiItem.cancel()
                                                       ):
            self.iface.clearCache(0)

    def save(self):
        self.iface.setCacheLimit(self.settings.useCacheCheck.isChecked(), self.settings.useCacheSpin.value())

class RepositorySettings(SettingsTab):
    def setupUi(self):
        self.settings.repoListView.horizontalHeader().setStretchLastSection(True)
        self.settings.repoListView.verticalHeader().hide()
        self.settings.repoListView.setColumnWidth(0, 32)
        self.__getRepositories()

    def connectSignals(self):
        self.connect(self.settings.addRepoButton, SIGNAL("clicked()"), self.addRepository)
        self.connect(self.settings.removeRepoButton, SIGNAL("clicked()"), self.removeRepository)
        self.connect(self.settings.moveUpButton, SIGNAL("clicked()"), self.moveUp)
        self.connect(self.settings.moveDownButton, SIGNAL("clicked()"), self.moveDown)
        self.connect(self.settings.repoListView, SIGNAL("itemChanged(QTableWidgetItem*)"), self.markChanged)

    def __getRepositories(self):
        repositories = self.iface.getRepositories()
        for name, address in repositories:
            self.__insertRow(name, address)

    def __insertRow(self, repoName, repoAddress):
        currentRow = self.settings.repoListView.rowCount()
        self.settings.repoListView.insertRow(currentRow)
        checkbox = QtGui.QCheckBox(self.settings.repoListView)
        self.connect(checkbox, SIGNAL("toggled(bool)"), self.markChanged)
        self.settings.repoListView.setCellWidget(currentRow, 0, checkbox)
        self.settings.repoListView.cellWidget(currentRow, 0).setChecked(self.iface.isRepoActive(repoName))

        repoNameItem = QtGui.QTableWidgetItem()
        repoNameItem.setText(repoName)
        repoNameItem.setTextAlignment(Qt.AlignCenter)
        self.settings.repoListView.setItem(currentRow, 1, repoNameItem)

        repoAddressItem = QtGui.QTableWidgetItem()
        repoAddressItem.setText(repoAddress)
        repoAddressItem.setTextAlignment(Qt.AlignCenter)
        self.settings.repoListView.setItem(currentRow, 2, repoAddressItem)

    def addRepository(self):
        self.repoDialog = repodialog.RepoDialog()
        self.connect(self.repoDialog.buttonBox, SIGNAL("accepted()"), self.__addRepository)
        self.repoDialog.show()

    def __addRepository(self):
        repoName = self.repoDialog.repoName.text()
        repoAddress = self.repoDialog.repoAddress.currentText()
        if not repoAddress.endsWith("xml") and not repoAddress.endsWith("xml.bz2"):
            KMessageBox.error(self,i18n('<qt>Repository address should end with xml or xml.bz2 suffix.<p>Please try again.</qt>'), i18n("Pisi Error"))
            return
        self.__insertRow(repoName, repoAddress)
        self.markChanged()

    def removeRepository(self):
        self.settings.repoListView.removeRow(self.settings.repoListView.currentRow())
        self.markChanged()

    def __setRow(self, row, rowItems):
        for col in range(self.settings.repoListView.columnCount()):
            self.settings.repoListView.setItem(row, col, rowItems[col])

    def __takeRow(self, row):
        rowItems = []
        for col in range(self.settings.repoListView.columnCount()):
            rowItems.append(self.settings.repoListView.takeItem(row, col))
        return rowItems

    def __move(self, up):
        srcRow = self.settings.repoListView.currentRow()
        dstRow = srcRow - 1 if up else srcRow + 1
        if dstRow < 0 or dstRow >= self.settings.repoListView.rowCount():
            return

        srcRowChecked = self.settings.repoListView.cellWidget(srcRow, 0).checkState()
        dstRowChecked = self.settings.repoListView.cellWidget(dstRow, 0).checkState()
        srcItems = self.__takeRow(srcRow)
        destItems = self.__takeRow(dstRow)

        self.__setRow(srcRow, destItems)
        self.__setRow(dstRow, srcItems)
        self.settings.repoListView.cellWidget(srcRow, 0).setCheckState(dstRowChecked)
        self.settings.repoListView.cellWidget(dstRow, 0).setCheckState(srcRowChecked)

        self.settings.repoListView.setCurrentItem(srcItems[1])
        self.markChanged()

    def moveUp(self):
        self.__move(True)

    def moveDown(self):
        self.__move(False)

    def getRepo(self, row):
        active = self.settings.repoListView.cellWidget(row, 0).checkState() == Qt.Checked
        name  = self.settings.repoListView.item(row, 1).text()
        address  = self.settings.repoListView.item(row, 2).text()
        return (str(name), str(address), active)

    def save(self):
        repos = []
        activities = {}
        for row in range(self.settings.repoListView.rowCount()):
            name, address, active = self.getRepo(row)
            repos.append((name, address))
            activities[name]=active
        self.iface.setRepositories(repos)
        self.iface.setRepoActivities(activities)

class ProxySettings(SettingsTab):
    def setupUi(self):
        self.settings.noProxyButton.setChecked(True)
        self.__getProxySettings()

    def __getProxySettings(self):
        config = self.iface.getConfig()
        httpProxy = httpProxyPort = ftpProxy = ftpProxyPort = httpsProxy = httpsProxyPort = None

        http = config.get("general", "http_proxy")
        if http and http != "None":
            httpProxy, httpProxyPort = http[7:].split(":")
            self.settings.httpProxy.setText(httpProxy)
            self.settings.httpProxyPort.setValue(int(httpProxyPort))

        https = config.get("general", "https_proxy")
        if https and https != "None":
            httpsProxy, httpsProxyPort = https[8:].split(":")
            self.settings.httpsProxy.setText(httpsProxy)
            self.settings.httpsProxyPort.setValue(int(httpsProxyPort))

        ftp = config.get("general", "ftp_proxy")
        if ftp and ftp != "None":
            ftpProxy, ftpProxyPort = ftp[6:].split(":")
            self.settings.ftpProxy.setText(ftpProxy)
            self.settings.ftpProxyPort.setValue(int(ftpProxyPort))

        if httpProxy or ftpProxy or httpsProxy:
            self.settings.useProxyButton.setChecked(True)
            if (httpProxy == httpsProxy == ftpProxy) and (httpProxyPort == httpsProxyPort == ftpProxyPort):
                self.settings.useHttpForAll.setChecked(True)

    def connectSignals(self):
        self.connect(self.settings.useHttpForAll, SIGNAL("toggled(bool)"), self.useHttpToggled)
        self.connect(self.settings.httpProxy, SIGNAL("textChanged(const QString&)"), self.markChanged)
        self.connect(self.settings.httpProxyPort, SIGNAL("valueChanged(int)"), self.markChanged)
        self.connect(self.settings.httpsProxy, SIGNAL("textChanged(const QString&)"), self.markChanged)
        self.connect(self.settings.httpsProxyPort, SIGNAL("valueChanged(int)"), self.markChanged)
        self.connect(self.settings.ftpProxy, SIGNAL("textChanged(const QString&)"), self.markChanged)
        self.connect(self.settings.ftpProxyPort, SIGNAL("valueChanged(int)"), self.markChanged)
        self.connect(self.settings.noProxyButton, SIGNAL("toggled(bool)"), self.markChanged)

    def useHttpToggled(self, enabled):
        if enabled:
            self.settings.httpsProxy.setText(self.settings.httpProxy.text())
            self.settings.httpsProxyPort.setValue(self.settings.httpProxyPort.value())
            self.settings.ftpProxy.setText(self.settings.httpProxy.text())
            self.settings.ftpProxyPort.setValue(self.settings.httpProxyPort.value())

            for control in [self.settings.httpsProxy, self.settings.httpsProxyPort, self.settings.ftpProxy, self.settings.ftpProxyPort]:
                control.setEnabled(False)

            self.connect(self.settings.httpProxy, SIGNAL("textChanged(const QString&)"), self.settings.httpsProxy, SLOT("setText(const QString&)"))
            self.connect(self.settings.httpProxy, SIGNAL("textChanged(const QString&)"), self.settings.ftpProxy, SLOT("setText(const QString&)"))
            self.connect(self.settings.httpProxyPort, SIGNAL("valueChanged(int)"), self.settings.httpsProxyPort, SLOT("setValue(int)"))
            self.connect(self.settings.httpProxyPort, SIGNAL("valueChanged(int)"), self.settings.ftpProxyPort, SLOT("setValue(int)"))
        else:
            self.disconnect(self.settings.httpProxy, SIGNAL("textChanged(const QString&)"), self.settings.httpsProxy, SLOT("setText(const QString&)"))
            self.disconnect(self.settings.httpProxy, SIGNAL("textChanged(const QString&)"), self.settings.ftpProxy, SLOT("setText(const QString&)"))
            self.disconnect(self.settings.httpProxyPort, SIGNAL("valueChanged(int)"), self.settings.httpsProxyPort, SLOT("setValue(int)"))
            self.disconnect(self.settings.httpProxyPort, SIGNAL("valueChanged(int)"), self.settings.ftpProxyPort, SLOT("setValue(int)"))

            for control in [self.settings.httpsProxy, self.settings.httpsProxyPort, self.settings.ftpProxy, self.settings.ftpProxyPort]:
                control.setEnabled(True)

            self.settings.httpsProxy.setText("")
            self.settings.httpsProxyPort.setValue(0)
            self.settings.ftpProxy.setText("")
            self.settings.ftpProxyPort.setValue(0)

    def save(self):
        httpProxy, httpProxyPort = self.settings.httpProxy.text(), self.settings.httpProxyPort.value()
        httpsProxy, httpsProxyPort = self.settings.httpsProxy.text(), self.settings.httpsProxyPort.value()
        ftpProxy, ftpProxyPort = self.settings.ftpProxy.text(), self.settings.ftpProxyPort.value()

        if self.settings.noProxyButton.isChecked():
            httpProxy = httpsProxy = ftpProxy = None

        if httpProxy:
            self.iface.setConfig("general", "http_proxy", "http://%s:%s" % (httpProxy, httpProxyPort))
        else:
            self.iface.setConfig("general", "http_proxy", "None")

        if httpsProxy:
            self.iface.setConfig("general", "https_proxy", "https://%s:%s" % (httpsProxy, httpsProxyPort))
        else:
            self.iface.setConfig("general", "https_proxy", "None")

        if ftpProxy:
            self.iface.setConfig("general", "ftp_proxy", "ftp://%s:%s" % (ftpProxy, ftpProxyPort))
        else:
            self.iface.setConfig("general", "ftp_proxy", "None")

class SettingsDialog(QtGui.QDialog, Ui_SettingsDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.connectSignals()

        self.generalSettings = GeneralSettings(self)
        self.cacheSettings = CacheSettings(self)
        self.repositorySettings = RepositorySettings(self)
        self.proxySettings = ProxySettings(self)

    def connectSignals(self):
        self.connect(self.buttonOk, SIGNAL("clicked()"), self.saveSettings)
        self.connect(self.buttonHelp, SIGNAL("clicked()"), self.showHelp)

    def saveSettings(self):
        changed = False
        for settings in [self.generalSettings, self.cacheSettings, self.repositorySettings, self.proxySettings]:
            if settings.changed:
                changed = True
                settings.save()
        
        if changed:
            self.emit(SIGNAL("settingsChanged()"))

    def showHelp(self):
        helpDialog = helpdialog.HelpDialog(self, helpdialog.PREFERENCES)
        helpDialog.show()

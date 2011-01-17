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

import re

from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QTableWidgetItem
from PyQt4.QtGui import QCheckBox
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QDesktopServices
from PyQt4.QtCore import *

from PyKDE4.kdecore import i18n
from PyKDE4.kdeui import KIcon
from os import path

from ui_settingsdialog import Ui_SettingsDialog

import config
import helpdialog
import repodialog
import pmutils
import backend

class SettingsTab(QObject):
    def __init__(self, settings):
        QObject.__init__(self)
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

    def initialize(self):
        pass

class GeneralSettings(SettingsTab):
    def setupUi(self):
        self.settings.moveUpButton.setIcon(KIcon("arrow-up"))
        self.settings.moveDownButton.setIcon(KIcon("arrow-down"))
        self.settings.addRepoButton.setIcon(KIcon("list-add"))
        self.settings.removeRepoButton.setIcon(KIcon("list-remove"))
        self.initialize()

    def initialize(self):
        self.settings.onlyGuiApp.setChecked(self.config.showOnlyGuiApp())
        self.settings.showComponents.setChecked(self.config.showComponents())
        self.settings.showIsA.setChecked(self.config.showIsA())
        self.settings.intervalCheck.setChecked(self.config.updateCheck())
        self.settings.installUpdates.setChecked(self.config.installUpdatesAutomatically())
        self.settings.intervalSpin.setValue(self.config.updateCheckInterval())
        self.settings.systemTray.setChecked(self.config.systemTray())
        self.settings.hideIfNoUpdate.setChecked(self.config.hideTrayIfThereIsNoUpdate())
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
        self.connect(self.settings.showComponents, SIGNAL("toggled(bool)"), self.markChanged)
        self.connect(self.settings.showIsA, SIGNAL("toggled(bool)"), self.markChanged)
        self.connect(self.settings.intervalCheck, SIGNAL("toggled(bool)"), self.markChanged)
        self.connect(self.settings.installUpdates, SIGNAL("toggled(bool)"), self.markChanged)
        self.connect(self.settings.useBandwidthLimit, SIGNAL("toggled(bool)"), self.markChanged)
        self.connect(self.settings.intervalSpin, SIGNAL("valueChanged(int)"), self.markChanged)
        self.connect(self.settings.systemTray, SIGNAL("toggled(bool)"), self.markChanged)
        self.connect(self.settings.hideIfNoUpdate, SIGNAL("toggled(bool)"), self.markChanged)
        self.connect(self.settings.bandwidthSpin, SIGNAL("valueChanged(int)"), self.markChanged)

    def save(self):
        if not self.settings.onlyGuiApp.isChecked() == self.config.showOnlyGuiApp():
            self.config.setShowOnlyGuiApp(self.settings.onlyGuiApp.isChecked())
            self.settings.emit(SIGNAL("packagesChanged()"))

        if not self.settings.showComponents.isChecked() == self.config.showComponents():
            self.config.setShowComponents(self.settings.showComponents.isChecked())
            self.settings.emit(SIGNAL("packageViewChanged()"))

        if not self.settings.showIsA.isChecked() == self.config.showIsA():
            self.config.setShowIsA(self.settings.showIsA.isChecked())
            self.settings.emit(SIGNAL("packageViewChanged()"))

        if not self.settings.systemTray.isChecked() == self.config.systemTray() or \
           not self.settings.intervalSpin.value() == self.config.updateCheckInterval() or \
           not self.settings.intervalCheck.isChecked() == self.config.updateCheck() or \
           not self.settings.hideIfNoUpdate.isChecked() == self.config.hideTrayIfThereIsNoUpdate():
            self.config.setSystemTray(self.settings.systemTray.isChecked())
            self.config.setUpdateCheck(self.settings.intervalCheck.isChecked())
            self.config.setUpdateCheckInterval(self.settings.intervalSpin.value())
            self.config.setHideTrayIfThereIsNoUpdate(self.settings.hideIfNoUpdate.isChecked())
            self.settings.emit(SIGNAL("traySettingChanged()"))

        self.config.setInstallUpdatesAutomatically(self.settings.installUpdates.isChecked())

        if self.settings.useBandwidthLimit.isChecked():
            self.iface.setConfig("general", "bandwidth_limit", str(self.settings.bandwidthSpin.value()))
        else:
            self.iface.setConfig("general", "bandwidth_limit", "0")

class CacheSettings(SettingsTab):
    def setupUi(self):
        self.initialize()

    def initialize(self):
        config = self.iface.getConfig()

        cache = config.get("general", "package_cache")
        cache_limit = config.get("general", "package_cache_limit")
        cache_limit = int(cache_limit) if cache_limit else 0
        cache_dir = config.get("directories", "cached_packages_dir")
        cache_dir = str(cache_dir) if cache_dir else '/var/cache/pisi/packages'

        # If pisi.conf does not have it yet, default is use package cache
        if not cache or cache == "True":
            enableCache = True
        else:
            enableCache = False

        self.cacheEnabled = enableCache
        self.cacheSize = cache_limit
        self.settings.cacheGroup.setEnabled(self.cacheEnabled)
        self.settings.useCacheCheck.setChecked(enableCache)
        self.settings.useCacheSpin.setValue(cache_limit)
        self.settings.cacheDirPath.setText(cache_dir)

    def connectSignals(self):
        self.connect(self.settings.clearCacheButton, SIGNAL("clicked()"), self.clearCache)
        self.connect(self.settings.selectCacheDir, SIGNAL("clicked()"), self.selectCacheDir)
        self.connect(self.settings.useCacheCheck, SIGNAL("toggled(bool)"), self.markChanged)
        self.connect(self.settings.useCacheSpin, SIGNAL("valueChanged(int)"), self.markChanged)
        self.settings.openCacheDir.clicked.connect(self.openCacheDir)

    def openCacheDir(self):
        cache_dir = unicode(self.settings.cacheDirPath.text())
        if path.exists(cache_dir):
            QDesktopServices.openUrl(QUrl("file://%s" % cache_dir, QUrl.TolerantMode))

    def selectCacheDir(self):
        selected_dir = QFileDialog.getExistingDirectory(self.settings, i18n("Open Directory"), "/",
                                                        QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if not selected_dir == '':
            if not selected_dir == self.settings.cacheDirPath.text():
                self.settings.cacheDirPath.setText(selected_dir)
                self.markChanged()

    def clearCache(self):
        if QMessageBox.Yes == QMessageBox.warning(self.settings,
                                                  i18n("Warning"),
                                                  i18n("All the cached packages will be deleted. Are you sure? "),
                                                  QMessageBox.Yes | QMessageBox.No):
            self.iface.clearCache(0)

    def save(self):
        self.iface.setCacheLimit(self.settings.useCacheCheck.isChecked(), self.settings.useCacheSpin.value())
        self.iface.setConfig("directories", "cached_packages_dir", unicode(self.settings.cacheDirPath.text()))

class RepositorySettings(SettingsTab):
    def setupUi(self):
        self.settings.repoListView.horizontalHeader().setStretchLastSection(True)
        self.settings.repoListView.verticalHeader().hide()
        self.settings.repoListView.setColumnWidth(0, 32)
        self.initialize()

    def connectSignals(self):
        self.connect(self.settings.addRepoButton, SIGNAL("clicked()"), self.addRepository)
        self.connect(self.settings.removeRepoButton, SIGNAL("clicked()"), self.removeRepository)
        self.connect(self.settings.moveUpButton, SIGNAL("clicked()"), self.moveUp)
        self.connect(self.settings.moveDownButton, SIGNAL("clicked()"), self.moveDown)
        self.connect(self.settings.repoListView, SIGNAL("itemChanged(QTableWidgetItem*)"), self.markChanged)

    def initialize(self):
        self.repositories = self.iface.getRepositories()
        self.__clear()
        for name, address in self.repositories:
            self.__insertRow(unicode(name), address)

    def __clear(self):
        while self.settings.repoListView.rowCount():
            self.settings.repoListView.removeRow(0)

    def __insertRow(self, repoName, repoAddress):
        currentRow = self.settings.repoListView.rowCount()
        self.settings.repoListView.insertRow(currentRow)
        checkbox = QCheckBox(self.settings.repoListView)
        self.connect(checkbox, SIGNAL("toggled(bool)"), self.markChanged)
        self.settings.repoListView.setCellWidget(currentRow, 0, checkbox)
        self.settings.repoListView.cellWidget(currentRow, 0).setChecked(self.iface.isRepoActive(repoName))

        repoNameItem = QTableWidgetItem()
        repoNameItem.setText(repoName)
        repoNameItem.setTextAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.settings.repoListView.setItem(currentRow, 1, repoNameItem)

        repoAddressItem = QTableWidgetItem()
        repoAddressItem.setText(repoAddress)
        repoAddressItem.setTextAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.settings.repoListView.setItem(currentRow, 2, repoAddressItem)

    def addRepository(self):
        self.repoDialog = repodialog.RepoDialog()
        self.connect(self.repoDialog.buttonBox, SIGNAL("accepted()"), self.__addRepository)
        self.repoDialog.show()

    def __addRepository(self):
        repoName = self.repoDialog.repoName.text()
        repoAddress = self.repoDialog.repoAddress.currentText()
        if not re.match("^[0-9%s\-\\_\\.\s]*$" % str(pmutils.letters()), str(repoName)) or str(repoName) == '':
            QMessageBox.warning(self.settings,
                                i18n("Pisi Error"),
                                i18n("Not a valid repository name"))
            return
        if not repoAddress.endsWith("xml") and not repoAddress.endsWith("xml.bz2") and not repoAddress.endsWith('xz'):
            QMessageBox.warning(self.settings,
                                i18n("Pisi Error"),
                                i18n('<qt>Repository address should end with xml or xml.bz2 or xz suffix.<p>Please try again.</qt>'))
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
        self.iface.updateRepositories()

class ProxySettings(SettingsTab):
    def setupUi(self):
        self.initialize()

    def initialize(self):
        self.settings.noProxyButton.setChecked(True)
        config = self.iface.getConfig()
        httpProxy = httpProxyPort = ftpProxy = ftpProxyPort = httpsProxy = httpsProxyPort = None

        http = config.get("general", "http_proxy")
        if http and http != "None":
            httpProxy, httpProxyPort = http[7:].rsplit(":", 1)
            self.settings.httpProxy.setText(httpProxy)
            self.settings.httpProxyPort.setValue(int(httpProxyPort))

        https = config.get("general", "https_proxy")
        if https and https != "None":
            httpsProxy, httpsProxyPort = https[8:].rsplit(":", 1)
            self.settings.httpsProxy.setText(httpsProxy)
            self.settings.httpsProxyPort.setValue(int(httpsProxyPort))

        ftp = config.get("general", "ftp_proxy")
        if ftp and ftp != "None":
            ftpProxy, ftpProxyPort = ftp[6:].rsplit(":", 1)
            self.settings.ftpProxy.setText(ftpProxy)
            self.settings.ftpProxyPort.setValue(int(ftpProxyPort))

        if self.config.useKdeProxy():
            self.settings.useKdeButton.setChecked(True)
        elif httpProxy or ftpProxy or httpsProxy:
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
        self.connect(self.settings.useKdeButton, SIGNAL("toggled(bool)"), self.markChanged)
        self.connect(self.settings.useKdeButton, SIGNAL("toggled(bool)"), self.getSettingsFromKde)

    def useHttpToggled(self, enabled):
        controls = (self.settings.httpsProxy, self.settings.httpsProxyPort, self.settings.ftpProxy, self.settings.ftpProxyPort)
        if enabled:
            self.settings.httpsProxy.setText(self.settings.httpProxy.text())
            self.settings.httpsProxyPort.setValue(self.settings.httpProxyPort.value())
            self.settings.ftpProxy.setText(self.settings.httpProxy.text())
            self.settings.ftpProxyPort.setValue(self.settings.httpProxyPort.value())

            for control in controls:
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

            for control in controls:
                control.setEnabled(True)

            self.clear(all=False)

    def clear(self, all=True):
        if all:
            self.settings.httpProxy.setText("")
            self.settings.httpProxyPort.setValue(0)
        self.settings.httpsProxy.setText("")
        self.settings.httpsProxyPort.setValue(0)
        self.settings.ftpProxy.setText("")
        self.settings.ftpProxyPort.setValue(0)

    def getSettingsFromKde(self, toggled):
        if toggled:
            cf = path.join(Pds.config_path, 'share/config/kioslaverc')
            config = Pds.parse(cf, force=True)
            proxyType = config.value('Proxy Settings/ProxyType').toString()
            if proxyType:
                if int(proxyType) > 0:
                    http = str(config.value('Proxy Settings/httpProxy').toString()).rsplit(':', 1)
                    self.settings.httpsProxy.setText(http[0])
                    self.settings.httpsProxyPort.setValue(int(http[1]))

                    https = str(config.value('Proxy Settings/httpsProxy').toString()).rsplit(':', 1)
                    self.settings.httpProxy.setText(https[0])
                    self.settings.httpProxyPort.setValue(int(https[1]))

                    ftp = str(config.value('Proxy Settings/ftpProxy').toString()).rsplit(':', 1)
                    self.settings.ftpProxy.setText(ftp[0])
                    self.settings.ftpProxyPort.setValue(int(ftp[1]))
            else:
                self.clear()

    def save(self):
        httpProxy, httpProxyPort = self.settings.httpProxy.text().split('://')[-1], self.settings.httpProxyPort.value()
        httpsProxy, httpsProxyPort = self.settings.httpsProxy.text().split('://')[-1], self.settings.httpsProxyPort.value()
        ftpProxy, ftpProxyPort = self.settings.ftpProxy.text().split('://')[-1], self.settings.ftpProxyPort.value()

        if self.settings.noProxyButton.isChecked():
            httpProxy = httpsProxy = ftpProxy = None

        self.config.setUseKdeProxy(self.settings.useKdeButton.isChecked())

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

class SettingsDialog(QDialog, Ui_SettingsDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.connectSignals()

        self.generalSettings = GeneralSettings(self)
        self.cacheSettings = CacheSettings(self)
        self.repositorySettings = RepositorySettings(self)
        self.proxySettings = ProxySettings(self)

        self.parent = parent

    def connectSignals(self):
        self.connect(self.buttonOk, SIGNAL("clicked()"), self.saveSettings)
        self.connect(self.buttonCancel, SIGNAL("clicked()"), self.cancelSettings)
        self.connect(self.buttonHelp, SIGNAL("clicked()"), self.showHelp)

    def cancelSettings(self):
        for tab in (self.generalSettings, self.cacheSettings, \
                self.repositorySettings, self.proxySettings):
            tab.initialize()
        self.reject()

    def saveSettings(self):
        for settings in [self.generalSettings, self.cacheSettings, self.repositorySettings, self.proxySettings]:
            try:
                if settings.changed:
                    settings.save()
            except Exception, e:
                self.parent.cw.exceptionCaught(str(e))
            settings.changed = False
        self.config = config.PMConfig()

    def showHelp(self):
        helpDialog = helpdialog.HelpDialog(self, helpdialog.PREFERENCES)
        helpDialog.show()


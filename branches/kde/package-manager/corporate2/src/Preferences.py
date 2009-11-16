# -*- coding: utf-8 -*-
#
# Copyright (C) 2005,2006 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

# KDE/Qt imports
from kdecore import i18n, KIcon
from kdeui import *
from qt import *

# Local imports
import HelpDialog
import PreferencesDialog
import RepoDialog
import Settings
import Icons

import PisiIface

class Preferences(PreferencesDialog.PreferencesDialog):
    def __init__(self, parent=None):
        PreferencesDialog.PreferencesDialog.__init__(self, parent)

        #add icons to buttons
        self.addButton.setIconSet(Icons.loadIconSet("add", KIcon.Small))
        self.editButton.setIconSet(Icons.loadIconSet("configure", KIcon.Small))
        self.removeButton.setIconSet(Icons.loadIconSet("remove", KIcon.Small))
        self.moveUpButton.setIconSet(Icons.loadIconSet("up", KIcon.Small))
        self.moveDownButton.setIconSet(Icons.loadIconSet("down", KIcon.Small))
        self.buttonOk.setIconSet(Icons.loadIconSet("ok", KIcon.Small))
        self.buttonCancel.setIconSet(Icons.loadIconSet("cancel", KIcon.Small))
        self.buttonHelp.setIconSet(Icons.loadIconSet("help1", KIcon.Small))

        self.parent = parent
        self.connect(self.addButton, SIGNAL("clicked()"), self.addNewRepo)
        self.connect(self.editButton, SIGNAL("clicked()"), self.editRepo)
        self.connect(self.removeButton, SIGNAL("clicked()"), self.removeRepo)
        self.connect(self.repoListView, SIGNAL("selectionChanged()"), self.updateButtons)
        self.connect(self.moveUpButton, SIGNAL("clicked()"), self.moveUp)
        self.connect(self.moveDownButton, SIGNAL("clicked()"), self.moveDown)
        self.connect(self.buttonOk, SIGNAL("clicked()"), self.saveSettings)
        self.connect(self.intervalCheck, SIGNAL("toggled(bool)"), self.enableCheckInterval)
        self.connect(self.useCacheCheck, SIGNAL("toggled(bool)"), self.enableUseCache)
        self.connect(self.clearCacheButton, SIGNAL("clicked()"), self.clearAllCached)
        self.connect(self.buttonHelp, SIGNAL("clicked()"), self.showHelp)
        self.connect(self.useHttpForAll, SIGNAL("toggled(bool)"), self.useHttpToggled)
        self.connect(self.useBandwidthLimit, SIGNAL("toggled(bool)"), self.bandwidthSettingChanged)
        self.connect(self.bandwidthValue, SIGNAL("valueChanged(int)"), self.bandwidthSettingChanged)

        self.connect(self.httpProxy, SIGNAL("textChanged(const QString&)"), self.proxyDataChanged)
        self.connect(self.httpProxyPort, SIGNAL("valueChanged(int)"), self.proxyDataChanged)
        self.connect(self.httpsProxy, SIGNAL("textChanged(const QString&)"), self.proxyDataChanged)
        self.connect(self.httpsProxyPort, SIGNAL("valueChanged(int)"), self.proxyDataChanged)
        self.connect(self.ftpProxy, SIGNAL("textChanged(const QString&)"), self.proxyDataChanged)
        self.connect(self.ftpProxyPort, SIGNAL("valueChanged(int)"), self.proxyDataChanged)
        self.connect(self.noProxyButton, SIGNAL("toggled(bool)"), self.proxyDataChanged)

        self.editButton.setEnabled(False)
        self.removeButton.setEnabled(False)

        self.repoListView.setSorting(-1)
        self.updateListView()
        self.updateButtons()

        self.onlyGuiApp.setChecked(self.parent.settings.getBoolValue(Settings.general, "ShowOnlyGuiApp"))
        self.intervalCheck.setChecked(self.parent.settings.getBoolValue(Settings.general, "UpdateCheck"))
        self.intervalSpin.setValue(self.parent.settings.getNumValue(Settings.general, "UpdateCheckInterval"))
        self.systemTray.setChecked(self.parent.settings.getBoolValue(Settings.general, "SystemTray"))
        self.noProxyButton.setChecked(True)
        self.getProxySettings()
        self.getCacheSettings()
        self.getBandwidthSetting()

        # This is to not call setRepositories unnecessarily
        self.reposChanged = False
        self.bandwidthChanged = False
        self.proxyChanged = False

    def bandwidthSettingChanged(self, data):
        self.bandwidthChanged = True

    def proxyDataChanged(self, data):
        self.proxyChanged = True

    def useHttpToggled(self, enabled):
        if enabled:
            self.httpsProxy.setText(self.httpProxy.text())
            self.httpsProxyPort.setValue(self.httpProxyPort.value())
            self.ftpProxy.setText(self.httpProxy.text())
            self.ftpProxyPort.setValue(self.httpProxyPort.value())

            for control in [self.httpsProxy, self.httpsProxyPort, self.ftpProxy, self.ftpProxyPort]:
                control.setEnabled(False)

            self.connect(self.httpProxy, SIGNAL("textChanged(const QString&)"), self.httpsProxy, SLOT("setText(const QString&)"))
            self.connect(self.httpProxy, SIGNAL("textChanged(const QString&)"), self.ftpProxy, SLOT("setText(const QString&)"))
            self.connect(self.httpProxyPort, SIGNAL("valueChanged(int)"), self.httpsProxyPort, SLOT("setValue(int)"))
            self.connect(self.httpProxyPort, SIGNAL("valueChanged(int)"), self.ftpProxyPort, SLOT("setValue(int)"))
        else:
            self.disconnect(self.httpProxy, SIGNAL("textChanged(const QString&)"), self.httpsProxy, SLOT("setText(const QString&)"))
            self.disconnect(self.httpProxy, SIGNAL("textChanged(const QString&)"), self.ftpProxy, SLOT("setText(const QString&)"))
            self.disconnect(self.httpProxyPort, SIGNAL("valueChanged(int)"), self.httpsProxyPort, SLOT("setValue(int)"))
            self.disconnect(self.httpProxyPort, SIGNAL("valueChanged(int)"), self.ftpProxyPort, SLOT("setValue(int)"))

            for control in [self.httpsProxy, self.httpsProxyPort, self.ftpProxy, self.ftpProxyPort]:
                control.setEnabled(True)

            self.httpsProxy.setText("")
            self.httpsProxyPort.setValue(0)
            self.ftpProxy.setText("")
            self.ftpProxyPort.setValue(0)

    def setCacheSettings(self, useCache, cacheLimit):
        self.parent.command.setCache(useCache, cacheLimit)

    def setBandwidth(self, limit):
        self.parent.command.setConfig("general", "bandwidth_limit", str(limit))

    def updateProxySettings(self):
        httpProxy, httpProxyPort = self.httpProxy.text(), self.httpProxyPort.value()
        httpsProxy, httpsProxyPort = self.httpsProxy.text(), self.httpsProxyPort.value()
        ftpProxy, ftpProxyPort = self.ftpProxy.text(), self.ftpProxyPort.value()

        if self.noProxyButton.isChecked():
            httpProxy = httpsProxy = ftpProxy = None

        if httpProxy:
            self.parent.command.setConfig("general", "http_proxy", "http://%s:%s" % (httpProxy, httpProxyPort))
        else:
            self.parent.command.setConfig("general", "http_proxy", "None")

        if httpsProxy:
            self.parent.command.setConfig("general", "https_proxy", "https://%s:%s" % (httpsProxy, httpsProxyPort))
        else:
            self.parent.command.setConfig("general", "https_proxy", "None")

        if ftpProxy:
            self.parent.command.setConfig("general", "ftp_proxy", "ftp://%s:%s" % (ftpProxy, ftpProxyPort))
        else:
            self.parent.command.setConfig("general", "ftp_proxy", "None")

    def getProxySettings(self):
        config = PisiIface.read_config("/etc/pisi/pisi.conf")
        httpProxy = httpProxyPort = ftpProxy = ftpProxyPort = httpsProxy = httpsProxyPort = None

        http = config.get("general", "http_proxy")
        if http and http != "None":
            httpProxy, httpProxyPort = http[7:].split(":")
            self.httpProxy.setText(httpProxy)
            self.httpProxyPort.setValue(int(httpProxyPort))

        https = config.get("general", "https_proxy")
        if https and https != "None":
            httpsProxy, httpsProxyPort = https[8:].split(":")
            self.httpsProxy.setText(httpsProxy)
            self.httpsProxyPort.setValue(int(httpsProxyPort))

        ftp = config.get("general", "ftp_proxy")
        if ftp and ftp != "None":
            ftpProxy, ftpProxyPort = ftp[6:].split(":")
            self.ftpProxy.setText(ftpProxy)
            self.ftpProxyPort.setValue(int(ftpProxyPort))

        if httpProxy or ftpProxy or httpsProxy:
            self.useProxyButton.setChecked(True)
            if (httpProxy == httpsProxy == ftpProxy) and (httpProxyPort == httpsProxyPort == ftpProxyPort):
                self.useHttpForAll.setChecked(True)

    def getBandwidthSetting(self):
        config = PisiIface.read_config("/etc/pisi/pisi.conf")
        bandwidth_limit = config.get("general", "bandwidth_limit")

        if bandwidth_limit:
           bandwidth_limit = int(bandwidth_limit)
        else:
            bandwidth_limit = 0

        if bandwidth_limit != 0:
            self.useBandwidthLimit.setChecked(True)
        self.bandwidthValue.setValue(bandwidth_limit)

    # Cache settings are system wide and taken from pisi.conf
    def getCacheSettings(self):
        config = PisiIface.read_config("/etc/pisi/pisi.conf")

        cache = config.get("general", "package_cache")
        cache_limit = config.get("general", "package_cache_limit")

        if cache_limit:
            cache_limit = int(cache_limit)
        else:
            cache_limit = 0

        # If pisi.conf does not have it yet, default is use package cache
        if not cache or cache == "True":
            enableCache = True
        else:
            enableCache = False

        self.cacheEnabled = enableCache
        self.cacheSize = cache_limit
        self.useCacheCheck.setChecked(enableCache)
        self.useCacheSize.setValue(cache_limit)

    def updateButtons(self):
        if self.repoListView.childCount() > 1:
            moreThanOne = True
        else:
            moreThanOne = False

        if self.repoListView.currentItem() and self.repoListView.currentItem().isSelected():
            self.editButton.setEnabled(True)
            self.removeButton.setEnabled(moreThanOne)
            self.moveUpButton.setEnabled(moreThanOne)
            self.moveDownButton.setEnabled(moreThanOne)

        else:
            self.editButton.setEnabled(False)
            self.removeButton.setEnabled(False)
            self.moveUpButton.setEnabled(False)
            self.moveDownButton.setEnabled(False)

    def updateAllRepos(self):
        self.parent.command.updateAllRepos()

    def addNewRepo(self):
        self.repo = RepoDialog.RepoDialog(self)
        self.repo.setCaption(i18n("Add New Repository"))
        self.repo.setModal(True)
        self.connect(self.repo.okButton, SIGNAL("clicked()"), self.processNewRepo)
        self.repo.show()

    def editRepo(self):
        self.repo = RepoDialog.RepoDialog(self)
        self.repo.setCaption(i18n("Edit Repository"))
        self.oldRepoName = self.repoListView.currentItem().text(0)
        self.oldRepoAddress = self.repoListView.currentItem().text(1)
        self.repo.repoName.setText(self.oldRepoName)
        self.repo.repoAddress.insertItem(self.oldRepoAddress, 0)
        self.repo.repoAddress.setCurrentItem(0)
        self.repo.setModal(True)
        self.connect(self.repo.okButton, SIGNAL("clicked()"), self.updateRepoSettings)
        self.repo.show()

    def removeRepo(self):
        repoItem = self.repoListView.currentItem()
        self.repoListView.takeItem(repoItem)
        self.reposChanged = True

    def moveUp(self):
        item = self.repoListView.currentItem()
        parent = item.itemAbove()

        if not parent:
            return

        if parent.itemAbove():
            item.moveItem(parent.itemAbove())
        else:
            self.repoListView.takeItem(item)
            self.repoListView.insertItem(item)
            self.repoListView.setSelected(item, True)

        self.reposChanged = True

    def moveDown(self):
        item = self.repoListView.currentItem()
        sibling = item.itemBelow()

        if not sibling:
            return

        item.moveItem(sibling)
        self.reposChanged = True

    def processNewRepo(self):
        repoName = unicode(self.repo.repoName.text())
        repoAddress = str(self.repo.repoAddress.currentText())

        if not repoAddress.endswith("xml") and not repoAddress.endswith("xml.bz2"):
            KMessageBox.error(self,i18n('<qt>Repository address should end with xml or xml.bz2 suffix.<p>Please try again.</qt>'), i18n("Pisi Error"))
            return

        item = QListViewItem(self.repoListView, self.repoListView.currentItem())
        item.setText(0, unicode(repoName))
        item.setText(1, repoAddress)
        self.repoListView.insertItem(item)

        self.reposChanged = True
        self.repo.close()

    def updateRepoSettings(self):
        newRepoName = unicode(self.repo.repoName.text())
        newRepoAddress = str(self.repo.repoAddress.currentText())

        if not newRepoAddress.endswith("xml") and not newRepoAddress.endswith("xml.bz2"):
            KMessageBox.error(self,i18n('<qt>Repository address should end with xml or xml.bz2 suffix.<p>Please try again.</qt>'), i18n("Pisi Error"))
            return

        self.repoListView.currentItem().setText(0,newRepoName)
        self.repoListView.currentItem().setText(1,newRepoAddress)

        if self.oldRepoAddress != newRepoAddress or self.oldRepoName != newRepoName:
            self.reposChanged = True

        self.repo.close()

    def saveSettings(self):
        self.parent.settings.setValue(Settings.general, "ShowOnlyGuiApp", self.onlyGuiApp.isChecked())
        self.parent.settings.setValue(Settings.general, "SystemTray", self.systemTray.isChecked())
        self.parent.settings.setValue(Settings.general, "UpdateCheck", self.intervalCheck.isChecked())
        self.parent.settings.setValue(Settings.general, "UpdateCheckInterval", self.intervalSpin.value())

        # set cache if changed
        if self.cacheEnabled != self.useCacheCheck.isChecked() or self.cacheSize != self.useCacheSize.value():
            self.setCacheSettings(self.useCacheCheck.isChecked(), self.useCacheSize.value())

        #set bandwidth if changed
        if self.bandwidthChanged:
            if self.useBandwidthLimit.isChecked():
                self.setBandwidth(self.bandwidthValue.value())
            else:
                # zero for no bandwidth limit
                self.setBandwidth(0)

        if self.intervalCheck.isChecked():
            self.parent.parent.tray.updateInterval(self.intervalSpin.value())
        else:
            self.parent.parent.tray.updateInterval(0)

        if self.proxyChanged:
            self.updateProxySettings()

        if self.reposChanged:
            repoList = []
            item = self.repoListView.firstChild()
            while item:
                repoList.append((unicode(item.text(0)), str(item.text(1))))
                item = item.nextSibling()

            self.reposChanged = False
            self.parent.command.setRepositories(repoList)
            self.parent.progressDialog.setCurrentOperation(i18n("<b>Applying Repository Changes</b>"))
            self.parent.progressDialog.show()
            return

        self.parent.refreshState()

    def updateListView(self):
        self.repoList = self.parent.command.getRepoList()
        self.repoListView.clear()

        index = len(self.repoList)-1
        while index >= 0:
            repoName = self.repoList[index]
            item = QListViewItem(self.repoListView,None)
            item.setText(0, unicode(self.repoList[index]))
            item.setText(1, self.parent.command.getRepoUri(str(repoName)))
            index -= 1

    def enableCheckInterval(self, state):
        self.intervalLabel.setEnabled(state)
        self.intervalSpin.setEnabled(state)

    def enableUseCache(self, state):
        self.useCacheLabel.setEnabled(state)
        self.useCacheSize.setEnabled(state)
        self.useCacheInfo.setEnabled(state)

    def showHelp(self):
        helpwin = HelpDialog.HelpDialog(self, HelpDialog.PREFERENCES)
        helpwin.show()

    def clearAllCached(self):
        if KMessageBox.Yes == KMessageBox.warningYesNo(self, 
                                                       i18n("All the cached packages will be deleted. Are you sure? "),
                                                       i18n("Warning"),
                                                       KGuiItem(i18n("Delete"), "trashcan_empty"),
                                                       KStdGuiItem.cancel()
                                                       ):
            self.parent.command.clearCache(0)

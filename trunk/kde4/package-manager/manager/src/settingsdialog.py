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

import helpdialog
import backend

class SettingsTab(QObject):
    def __init__(self, settings):
        self.settings = settings
        self.iface = backend.pm.Iface()
        self.changed = False
        self.setupUi()
        self.connectSignals()

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

class CacheSettings(SettingsTab):
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
        pass

class ProxySettings(SettingsTab):
    def setupUi(self):
        self.settings.noProxyButton.setChecked(True)

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
        for settings in [self.generalSettings, self.cacheSettings, self.repositorySettings, self.proxySettings]:
            if settings.changed:
                settings.save()

    def showHelp(self):
        helpDialog = helpdialog.HelpDialog(self, helpdialog.PREFERENCES)
        helpDialog.show()

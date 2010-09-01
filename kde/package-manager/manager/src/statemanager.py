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

from PyQt4.QtCore import QObject, SIGNAL
from PyQt4.QtGui import QMessageBox

from PyKDE4.kdeui import KIcon
from PyKDE4.kdecore import i18n

from pmlogging import logger
import config
import backend

class StateManager(QObject):

    (ALL, INSTALL, REMOVE, UPGRADE) = range(4)

    def __init__(self, parent=None):
        QObject.__init__(self)
        self.state = self.ALL
        self.silence = False
        self._group_cache = {}
        self.iface = backend.pm.Iface()

    def reset(self):
        self.cached_packages = None
        self._typeCaches = {}
        self._typeFilter = 'normal'
        self.initializePackageLists()

    def initializePackageLists(self):
        self.__installed_packages = self.iface.getInstalledPackages()
        self.__new_packages = self.iface.getNewPackages()
        self.__groups = self.iface.getGroups()
        self.__all_packages = self.__installed_packages + self.__new_packages

    def setState(self, state):
        self.state = state
        self.reset()
        self.emit(SIGNAL("repositoriesChanged()"))

    def getState(self):
        return self.state

    def packages(self):
        if self.cached_packages == None:
            if self.state == self.UPGRADE:
                self.cached_packages = self.iface.getUpdates()
                self._typeCaches = {}
            else:
                if self.state == self.REMOVE:
                    self.cached_packages = self.__installed_packages
                elif self.state == self.INSTALL:
                    self.cached_packages = self.__new_packages
                else:
                    self.cached_packages = self.__all_packages
                if self.onlyGuiInState():
                    self.cached_packages = set(self.cached_packages).intersection(self.iface.getIsaPackages("app:gui"))
        if not self._typeFilter == 'normal' and self.state == self.UPGRADE:
            if not self._typeCaches.has_key(self._typeFilter):
                self._typeCaches[self._typeFilter] = self.iface.filterUpdates(self.cached_packages, self._typeFilter)
            return self._typeCaches[self._typeFilter]
        return list(self.cached_packages)

    def onlyGuiInState(self):
        return config.PMConfig().showOnlyGuiApp()

    def getActionCurrent(self, action):
        return {"System.Manager.installPackage":i18n("Installing Package(s)"),
                "System.Manager.removePackage":i18n("Removing Package(s)"),
                "System.Manager.updatePackage":i18n("Upgrading Package(s)"),
                "System.Manager.setRepositories":i18n("Applying Repository Changes"),
                "System.Manager.updateRepository":i18n("Updating Repository"),
                "System.Manager.updateAllRepositories":i18n("Updating Repository(s)")}[str(action)]

    def getActionName(self):
        return {self.INSTALL:i18n("Install Package(s)"),
                self.REMOVE :i18n("Remove Package(s)"),
                self.UPGRADE:i18n("Upgrade Package(s)"),
                self.ALL    :i18n("Modify Package(s)")}[self.state]

    def toBe(self):
        return {self.INSTALL:i18n("installed"),
                self.REMOVE :i18n("removed"),
                self.UPGRADE:i18n("upgraded"),
                self.ALL    :i18n("modified")}[self.state]

    def getActionIcon(self):
        return {self.INSTALL:KIcon("list-add"),
                self.REMOVE :KIcon("list-remove"),
                self.UPGRADE:KIcon("view-refresh"),
                self.ALL    :KIcon("list-add")}[self.state]

    def getSummaryInfo(self, total):
        return {self.INSTALL:i18n("%1 new package(s) have been installed succesfully.", total),
                self.REMOVE :i18n("%1 package(s) have been removed succesfully.", total),
                self.UPGRADE:i18n("%1 package(s) have been upgraded succesfully.", total),
                self.ALL    :i18n("%1 package(s) have been modified succesfully.", total)}[self.state]

    def getBasketInfo(self):
        return {self.INSTALL:i18n("You have selected the following package(s) to install:"),
                self.REMOVE :i18n("You have selected the following package(s) to removal:"),
                self.UPGRADE:i18n("You have selected the following package(s) to upgrade:"),
                self.ALL    :i18n("You have selected the following package(s) to modify:")}[self.state]

    def getBasketExtrasInfo(self):
        return {self.INSTALL:i18n("Extra dependencies of the selected package(s) that are also going to be installed:"),
                self.REMOVE :i18n("Reverse dependencies of the selected package(s) that are also going to be removed:"),
                self.UPGRADE:i18n("Extra dependencies of the selected package(s) that are also going to be upgraded:"),
                self.ALL    :i18n("Extra dependencies of the selected package(s) that are also going to be modified:")}[self.state]

    def groups(self):
        return self.__groups

    def groupPackages(self, name):
        if name == "all":
            print len(self.packages())
            return self.packages()
        else:
            if self._group_cache.has_key(name):
                group_packages = self._group_cache[name]
            else:
                group_packages = self.iface.getGroupPackages(name)
                self._group_cache[name] = group_packages
            return list(set(self.packages()).intersection(group_packages))

    def chainAction(self, operation):
        chains = { "System.Manager.setRepositories":lambda:self.emit(SIGNAL("repositoriesChanged()")) }
        if chains.has_key(operation):
            chains[operation]()

    def stateAction(self):
        return {self.INSTALL:lambda:None,
                self.REMOVE :lambda:None,
                self.ALL    :lambda:None,
                self.UPGRADE:self.iface.updateRepositories}[self.state]()

    def statusText(self, packages, packagesSize, extraPackages, extraPackagesSize):
        if not packages:
            return i18n('')

        text = i18n("Currently there are <b>%1</b> selected package(s) of total <b>%2</b> of size ", packages, packagesSize)
        if extraPackages:
            if self.state == self.REMOVE:
                text += i18n("with <b>%1</b> reverse dependencies of total <b>%2</b> of size ", extraPackages, extraPackagesSize)
            else:
                text += i18n("with <b>%1</b> extra dependencies of total <b>%2</b> of size ", extraPackages, extraPackagesSize)
        text += i18n("in your basket.")

        return text

    def operationAction(self, packages, silence = False):
        if not silence:
            if self.state is not self.REMOVE and not self.conflictCheckPasses(packages):
                return
        return {self.ALL    :self.iface.modifyPackages,
                self.INSTALL:self.iface.installPackages,
                self.REMOVE :self.iface.removePackages,
                self.UPGRADE:self.iface.upgradePackages}[self.state](packages)

    def setActionHandler(self, handler):
        self.iface.setHandler(handler)

    def setExceptionHandler(self, handler):
        self.iface.setExceptionHandler(handler)

    def conflictCheckPasses(self, packages):
        (C, D, pkg_conflicts) = self.iface.getConflicts(packages, self.state)

        conflicts_within = list(D)
        if conflicts_within:
            text = i18n("Selected packages [%1] are in conflict with each other. These packages can not be installed together.", ", ".join(conflicts_within))
            QMessageBox.critical(None, i18n("Conflict Error"), text, QMessageBox.Ok)
            return False

        if pkg_conflicts:
            text = i18n("The following packages conflicts:\n")
            for pkg in pkg_conflicts.keys():
                text += i18n("%1 conflicts with: [%2]\n", pkg, ", ".join(pkg_conflicts[pkg]))
            text += i18n("\nRemove the conflicting packages from the system?")
            return QMessageBox.warning(None, i18n("Conflict Error"), text, QMessageBox.Yes, QMessageBox.No) == QMessageBox.Yes

        return True

    def checkUpdateActions(self, packages):
        return self.iface.checkUpdateActions(packages)

    def inInstall(self):
        return self.state == self.INSTALL

    def inRemove(self):
        return self.state == self.REMOVE

    def inUpgrade(self):
        return self.state == self.UPGRADE


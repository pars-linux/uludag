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

from PyQt4.QtCore import QObject, SIGNAL

from PyKDE4.kdecore import i18n
from PyKDE4.kdeui import KIcon

import backend

class StateManager(QObject):

    (INSTALL, REMOVE, UPGRADE) = range(3)

    def __init__(self, parent=None):
        QObject.__init__(self)
        self.parent = parent
        self.state = self.INSTALL
        self.iface = backend.pm.Iface()
        self.iface.setHandler(self.__actionHandler)
        self.cached_packages = None

    def setState(self, state):
        self.state = state
        self.cached_packages = None
        if self.state == self.REMOVE:
            self.iface.setSource(self.iface.SYSTEM)
        else:
            self.iface.setSource(self.iface.REPO)

    def getState(self):
        return self.state

    def packages(self):
        if self.cached_packages == None:
            if self.state == self.UPGRADE:
                self.cached_packages = self.iface.getUpdates()
            else:
                self.cached_packages = self.iface.getPackageList()
        return self.cached_packages

    def getActionName(self):
        return {self.INSTALL:i18n("Install Package(s)"),
                self.REMOVE :i18n("Remove Package(s)"),
                self.UPGRADE:i18n("Upgrade Package(s)")}[self.state]

    def getActionIcon(self):
        return {self.INSTALL:KIcon("list-add"),
                self.REMOVE :KIcon("list-remove"),
                self.UPGRADE:KIcon("view-refresh")}[self.state]

    def groups(self):
        return self.iface.getGroups()

    def groupPackages(self, name):
        return list(set(self.packages()).intersection(self.iface.getGroupPackages(name)))

    def takeAction(self, packages):
        return {self.INSTALL:self.iface.installPackages,
                self.REMOVE:self.iface.removePackages,
                self.UPGRADE:self.iface.upgradePackages}[self.state](packages)

    def __actionHandler(self, package, signal, args):
        # print "Signal:", signal
        # print "Args:", args

        if signal == "finished":
            self.emit(SIGNAL("finished(QString)"), args[0])
        elif signal == "progress":
            self.emit(SIGNAL("progress(int)"), args[2])

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

import backend

class Tray(KSystemTrayIcon):
    def __init__(self, parent):
        KSystemTrayIcon.__init__(self, parent)
        self.iface = backend.pm.Iface()
        self.initialize()

    def initialize(self):
        self.setIcon(KIcon(":/data/package-manager.png"))

        menu = KActionMenu(i18n("Update"), self)
        for name, address in self.iface.getRepositories():
            self.__addAction(name, menu)
        self.__addAction(i18n("All"), menu)
        self.contextMenu().addAction(menu)
        self.contextMenu().addSeparator()

    def __addAction(self, name, menu):
        action = QtGui.QAction(name, self)
        menu.addAction(action)
        self.connect(action, SIGNAL("triggered()"), self.updateRepo)

    def updateRepo(self):
        repoName = unicode(self.sender().iconText())
        pass


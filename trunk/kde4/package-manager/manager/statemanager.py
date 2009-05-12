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

import backend

class StateManager():

    (INSTALL, REMOVE, UPGRADE) = range(3)

    def __init__(self, parent=None):
        self.parent = parent
        self.state = self.INSTALL
        self.iface = backend.pm.Iface()

    def setState(self, state):
        self.state = state
        if self.state == self.REMOVE:
            self.iface.setSource(self.iface.SYSTEM)
        else:
            self.iface.setSource(self.iface.REPO)

    def packages(self):
        if self.state == self.UPGRADE:
            return self.iface.getUpdates()
        else:
            return self.iface.getPackageList()

    def groups(self):
        return self.iface.getGroups()

    def groupPackages(self, name):
        return list(set(self.packages()).intersection(self.iface.getGroupPackages(name)))

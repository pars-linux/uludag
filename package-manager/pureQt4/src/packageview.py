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

from pmutils import *

class PackageView(QtGui.QTreeView):
    def __init__(self, parent=None):
        QtGui.QTreeView.__init__(self, parent)

    def isIndexHidden(self, index):
        return False

    def setPackages(self, packages):
        self.model().sourceModel().setPackages(packages)
        self.model().reset()

    def selectedPackages(self):
        return self.model().sourceModel().selectedPackages()

    def extraPackages(self):
        return self.model().sourceModel().extraPackages()

    def selectedPackagesSize(self):
        return self.model().sourceModel().selectedPackagesSize()

    def extraPackagesSize(self):
        return self.model().sourceModel().extraPackagesSize()

    def packageCount(self):
        return len(self.selectedPackages()) + len(self.extraPackages())

    def isSelected(self):
        return bool(self.selectedPackages())

    def reverseSelection(self, packages):
        waitCursor()
        self.model().sourceModel().reverseSelection(packages)
        self.reset()
        restoreCursor()

    def selectAll(self, packages):
        waitCursor()
        self.model().sourceModel().selectPackages(packages)
        self.reset()
        restoreCursor()

    def resetMoreInfoRow(self):
        self.itemDelegate().reset()

    def search(self, text):
        return self.model().sourceModel().search(text)

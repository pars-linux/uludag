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

from PyQt4.QtCore import QThread, SIGNAL
from pmutils import humanReadableSize as humanize

class StatusUpdater(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.model = None
        self.needsUpdate = False

    def setModel(self, model):
        self.model = model

    def run(self):
        packages = len(self.model.selectedPackages())
        packagesSize = humanize(self.model.selectedPackagesSize())
        extraPackages = len(self.model.extraPackages())
        extraPackagesSize = humanize(self.model.extraPackagesSize())
        self.emit(SIGNAL("selectedInfoChanged(int, QString, int, QString)"), packages, packagesSize, extraPackages, extraPackagesSize)

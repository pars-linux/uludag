#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 TUBITAK/UEKAE
# Upgrade Manager
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

from PyQt4.QtGui import QWidget
from ui.ui_main import Ui_UpgradeManager

from backend import Iface

class UmGui(QWidget, Ui_UpgradeManager):

    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.progress.hide()

        self.iface = Iface()

        self.upgradeButton.clicked.connect(self.upgrade)

    def upgrade(self):
        self.upgradeButton.hide()
        self.progress.show()

        self.iface.installPackages(['abe'])


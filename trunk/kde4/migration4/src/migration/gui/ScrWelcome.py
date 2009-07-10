# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
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
from PyKDE4.kdecore import i18n

from migration.gui.ScreenWidget import ScreenWidget
from migration.gui.ui.welcomeWidget import Ui_welcomeWidget

class Widget(QtGui.QWidget, ScreenWidget):
    title = i18n("Welcome")
    desc = i18n("Welcome to Migration Tool Wizard :)")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_welcomeWidget()
        self.ui.setupUi(self)

        self.ui.pixMigrationLogo.setPixmap(QtGui.QPixmap(':/raw/pics/migration.png'))

    def shown(self):
        pass

    def execute(self):
        return True



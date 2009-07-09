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
from PyQt4.QtGui import *
from PyKDE4.kdecore import ki18n
from PyKDE4.kutils import KCModuleInfo, KCModuleProxy

from gui.ScreenWidget import ScreenWidget
from gui.networkWidget import Ui_networkWidget

class Widget(QtGui.QWidget, ScreenWidget):
    title = ki18n("Network Manager")
    desc = ki18n("Network Manager")

    running = False
    proc = QProcess()

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_networkWidget()
        self.ui.setupUi(self)

        moduleInfo = KCModuleInfo("kcm_networkmanager.desktop")
        nm = KCModuleProxy(moduleInfo)
        self.ui.layout.addWidget(nm)

    def execute(self):
        return True

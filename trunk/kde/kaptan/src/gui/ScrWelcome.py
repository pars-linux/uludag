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
from PyKDE4.kdecore import ki18n

from gui.ScreenWidget import ScreenWidget
from gui.welcomeWidget import Ui_welcomeWidget

import subprocess

class Widget(QtGui.QWidget, ScreenWidget):
    title = ki18n("Welcome")
    desc = ki18n("Welcome to Kaptan")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_welcomeWidget()
        self.ui.setupUi(self)

        #self.ui.pixKaptanLogo.setPixmap(QtGui.QPixmap(':/raw/pics/kaptan_welcome.png'))

        """
        self.release = self.getRelease().split()[0] + " " + self.getRelease().split()[1]
        self.ext = ""

        if self.release.__len__() > 2:
            self.ext = self.getRelease().split()[2]

        welcomeStr = "Welcome to " + self.release + " " + self.ext
        self.ui.label.setText(welcomeStr)

        def getRelease(self):
            try:
                p = subprocess.Popen(["cat","/etc/pardus-release"], stdout=subprocess.PIPE)
                release, err = p.communicate()
                return str(release)

            except:
                return "Pardus"
        """
    def shown(self):
        pass

    def execute(self):
        return True



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

from gui.screenwidget import ScreenWidget
from gui.userpassWidget import Ui_bugWidget

class Widget(QtGui.QWidget, ScreenWidget):
    title = ki18n("Bug Reporting Tool")
    desc = ki18n("Welcome to Bug Reporting Tool :)")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_bugWidget()
        self.ui.setupUi(self)

    def shown(self):
        pass

    def execute(self):
        return True

    def get_userpass(self):
        username = str(self.ui.username.text())
        password = str(self.ui.password.text())
        if len(username) == 0 or len(password) == 0:
            return None
        else:
            return (username, password)




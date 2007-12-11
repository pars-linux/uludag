#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

import sys
from PyQt4 import QtCore, QtGui
from uis.main import Ui_YaliMain
from uis.welcomewidget import Ui_WelcomeWidget

class yali4MainUi(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        # WTF ??
        self.center = QtGui.QWidget(self)
        layout = QtGui.QGridLayout(self.center)
        self.setCentralWidget(self.center)

        self.ui = Ui_YaliMain()
        self.ui.setupUi(self.center)
        #self.mainWidget = Ui_WelcomeWidget()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    Yali = yali4MainUi()
    Yali.show()
    sys.exit(app.exec_())


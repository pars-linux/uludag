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

class yali4MainUi(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_YaliMain()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    YaliMain = yali4MainUi()
    YaliMain.show()
    sys.exit(app.exec_())


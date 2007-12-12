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
from PyQt4 import QtGui
from PyQt4.QtCore import *
from uis.main import Ui_YaliMain

class yali4MainUi(Ui_YaliMain):
    def __init__(self):
        self.ui = QtGui.QWidget()
        self.setupUi(self.ui)
        QObject.connect(self.buttonNext,SIGNAL("clicked()"),self.slotNext)

    def slotNext(self):
        print "Yattaa !!"

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    YaliMain = yali4MainUi()
    YaliMain.ui.show()
    sys.exit(app.exec_())


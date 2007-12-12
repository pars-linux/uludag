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
from uis.welcomewidget import *
from uis.checkcdwidget import *
from uis.keyboardwidget import *
from uis.autopartwidget import *

screens = [Ui_WelcomeWidget,
           Ui_CheckCDWidget,
           Ui_KeyboardWidget,
           Ui_AutoPartWidget]

class yali4MainUi(Ui_YaliMain):
    def __init__(self):
        self.ui = QtGui.QWidget()
        self.setupUi(self.ui)
        QObject.connect(self.buttonNext,SIGNAL("clicked()"),self.slotNext)
        QObject.connect(self.buttonBack,SIGNAL("clicked()"),self.slotBack)
        self.createWidgets()
        self.mainStack.setCurrentIndex(0)

    def slotNext(self):
        self.stackMove(+1)

    def slotBack(self):
        self.stackMove(-1)

    def stackMove(self,d):
        new   = self.mainStack.currentIndex() + d
        total = self.mainStack.count()
        if new < 0: new = 0
        if new > total: new = total
        self.mainStack.setCurrentIndex(new)

    def createWidgets(self):
        self.mainStack.removeWidget(self.page)
        for screen in screens:
            _q = QtGui.QWidget()
            _w = screen()
            _w.setupUi(_q)
            self.mainStack.addWidget(_q)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    YaliMain = yali4MainUi()
    YaliMain.ui.show()
    sys.exit(app.exec_())


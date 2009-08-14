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
from gui.welcomeWidget import Ui_bugWidget

class Widget(QtGui.QWidget, ScreenWidget):
    title = ki18n("Bug Reporting Tool")
    desc = ki18n("Welcome to Bug Reporting Tool :)")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_bugWidget()
        self.ui.setupUi(self)
        QObject.connect(self.ui.comboBox,
                               SIGNAL("currentIndexChanged(int)"),
                               self.checkChoices)

    def shown(self):
        self.checkChoices(self.ui.comboBox.currentIndex())
        pass

    def execute(self):
        return True

    def checkChoices(self, value):
        if int(value) != 0:
            self.mainwindow.enableNext()
        else:
            self.mainwindow.disableNext()

    @property
    def mainwindow(self):
        return self.parentWidget().parentWidget().parentWidget()



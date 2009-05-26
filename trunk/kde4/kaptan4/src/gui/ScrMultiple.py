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
from PyKDE4.kdecore import ki18n, KStandardDirs, KGlobal, KConfig

from gui.ScreenWidget import ScreenWidget
from gui.multipleWidget import Ui_multipleWidget


class Widget(QtGui.QWidget, ScreenWidget):
    # Set title and description for the information widget
    title = ki18n("Some catchy title about multiple desktops")
    desc = ki18n("Some catchy description multiple desktops")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_multipleWidget()
        self.ui.setupUi(self)

        self.ui.spinBox.connect(self.ui.spinBox, SIGNAL("valueChanged(const QString &)"), self.addDesktop)

    def addDesktop(self, numberOfDesktop):
        config = KConfig("kwinrc")
        group = config.group("Desktops")
        group.writeEntry('Number', QString(numberOfDesktop))

    def shown(self):
        pass

    def execute(self):
        return True



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

import gui.ScrSummary  as summaryWidget
import gui.ScrSummary  as summaryWidget
from gui.ScreenWidget import ScreenWidget
from gui.keyboardWidget import Ui_keyboardWidget


class Widget(QtGui.QWidget, ScreenWidget):
    screenSettings = {}
    screenSettings["hasChanged"] = False

    # title and description at the top of the dialog window
    title = ki18n("Insert some catchy title about keyboards..")
    desc = ki18n("Select your keyboard layout")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_keyboardWidget()
        self.ui.setupUi(self)

    def shown(self):
        pass

    def execute(self):
        return True



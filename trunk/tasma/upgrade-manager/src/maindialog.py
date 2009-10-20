#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

from qt import *

from kdeui import *
from kdecore import *

from ui_maindialog import UI_MainDialog

import state

class MainDialog(UI_MainDialog):
    def __init__(self, parent=None):
        UI_MainDialog.__init__(self, parent)
        self.resetAllSteps()
        self.setFonts()
        self.state = state.State(self)

    def setFonts(self):
        self.normalFont = QFont()
        self.normalFont.setWeight(50)
        self.normalFont.setBold(False)

        self.boldFont = QFont()
        self.boldFont.setWeight(50)
        self.boldFont.setBold(True)

    def resetAllSteps(self):
        for step in range(1, 5):
            step_icon = getattr(self, "step%d_icon" % step)
            step_icon.setPixmap(QPixmap(""))

    def step_selected(self, step):
        step_icon = getattr(self, "step%d_icon" % step)
        step_icon.setPixmap(":/data/arrow.png")
        step_label = getattr(self, "step%d_label" % step)
        step_label.setFont(self.boldFont)

    def step_finished(self, step):
        step_icon = getattr(self, "step%d_icon" % step)
        step_icon.setPixmap(":/data/check.png")
        step_label = getattr(self, "step%d_label" % step)
        step_label.setFont(self.normalFont)

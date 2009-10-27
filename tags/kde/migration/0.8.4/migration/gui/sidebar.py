#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

# KDE-Qt Modules
from qt import *
from kdecore import *
from kdeui import *


class SideBar(QWidget):
    def __init__(self, parent, pagename):
        QWidget.__init__(self, parent)
        self.lay = QVBoxLayout(self)
        self.label = QLabel(self)
        self.logo = QPixmap(locate("appdata", "migration/migration.png"))
        self.label.setPixmap(self.logo)
        self.lay.addWidget(self.label)
        steps = [i18n("Selecting User"), i18n("Selecting Options"), i18n("Selecting Files"), i18n("Applying Changes")]
        for no, stepname in enumerate(steps):
            step = QLabel(self)
    	    step.setText(u"%d. %s" % (no + 1, stepname))
            font = step.font()
            font.setBold(True)
            step.setFont(font)
            step.setAlignment(step.alignment() | Qt.WordBreak)
            if stepname == pagename:
                step.setPaletteForegroundColor(QColor(171, 55, 14))
            else:
                step.setPaletteForegroundColor(QColor(243, 183, 17))
            self.lay.addWidget(step)

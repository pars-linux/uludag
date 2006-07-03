#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

import comar
from qt import *
from kdecore import *

from utility import *


class MonitorGroup(QIconView):
    def __init__(self, parent):
        QIconView.__init__(self, parent)
        QIconViewItem(self, "SyncMaster 172", getIconSet("display", KIcon.Desktop).pixmap(QIconSet.Automatic, QIconSet.Normal))
        QIconViewItem(self, "TV OUT", getIconSet("tv", KIcon.Desktop).pixmap(QIconSet.Automatic, QIconSet.Normal))


class MonitorEdit(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        grid = QGridLayout(self, 0, 0)
        grid.setSpacing(6)
        
        lab = QLabel(i18n("Monitor:"), self)
        grid.addWidget(lab, 0, 0, Qt.AlignRight)
        
        lab = QLabel(i18n("Resolution:"), self)
        grid.addWidget(lab, 1, 0, Qt.AlignRight)
        
        lab = QLabel(i18n("Number of colours:"), self)
        grid.addWidget(lab, 2, 0, Qt.AlignRight)


class Monitors(QVBox):
    def __init__(self, parent):
        QVBox.__init__(self, parent)
        self.setMargin(6)
        self.setSpacing(6)
        
        hb = QHBox(self)
        bar = QToolBar("lala", None, hb)
        
        but = QToolButton(getIconSet("configure.png"), i18n("Monitor Properties"), "lala", self.slotEdit, bar)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)
        
        bar.addSeparator()
        
        but = QToolButton(getIconSet("colors.png"), i18n("Color Properties"), "lala", self.slotEdit, bar)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)
        
        bar.addSeparator()
        
        but = QToolButton(getIconSet("kcmpci.png"), i18n("Hardware Settings"), "lala", self.slotEdit, bar)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)
        
        QLabel(" ", hb)
        
        self.group = MonitorGroup(self)
        self.edit = MonitorEdit(self)
    
    def slotEdit(self):
        pass

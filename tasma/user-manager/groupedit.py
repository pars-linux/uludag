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

from qt import *
from kdecore import *

from utility import *


class GID:
    def __init__(self, w, grid):
        lab = QLabel(i18n("ID:"), w)
        hb = QHBox(w)
        hb.setSpacing(6)
        self.gid = QLineEdit(hb)
        self.gid.setValidator(QIntValidator(0, 65535, self.gid))
        self.gid.setEnabled(False)
        self.gid_auto = QCheckBox(i18n("Select manually"), hb)
        w.connect(self.gid_auto, SIGNAL("toggled(bool)"), self.slotToggle)
        row = grid.numRows()
        grid.addWidget(lab, row, 0, Qt.AlignRight)
        grid.addWidget(hb, row, 1)
    
    def slotToggle(self, bool):
        self.gid.setEnabled(bool)
    
    def text(self):
        if self.gid_auto.isChecked():
            return int(self.uid.text())
        else:
            return "auto"


class GroupStack(QVBox):
    def __init__(self, parent, link):
        QVBox.__init__(self, parent)
        self.setMargin(6)
        self.setSpacing(6)
        
        lab = QLabel("<b>%s</b>" % i18n("Add a New Group"), self)
        
        w = QWidget(self)
        grid = QGridLayout(w, 0, 0)
        grid.setSpacing(6)
        
        self.g_id = GID(w, grid)
        
        lab = QLabel("Name:", w)
        self.g_name = QLineEdit(w)
        grid.addWidget(lab, 1, 0, Qt.AlignRight)
        grid.addWidget(self.g_name, 1, 1)
        
        hb = QHBox(self)
        hb.setSpacing(12)
        QLabel(" ", hb)
        but = QPushButton(getIconSet("add.png", KIcon.Small), i18n("Add"), hb)
        self.connect(but, SIGNAL("clicked()"), self.slotAdd)
        but = QPushButton(getIconSet("cancel.png", KIcon.Small), i18n("Cancel"), hb)
        self.connect(but, SIGNAL("clicked()"), parent.slotCancel)
        
        self.link = link
    
    def slotAdd(self):
        pass

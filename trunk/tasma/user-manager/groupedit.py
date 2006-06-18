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
from kdeui import *

from utility import *


class GID:
    def __init__(self, stack, w, grid):
        self.stack = stack
        lab = QLabel(i18n("ID:"), w)
        hb = QHBox(w)
        hb.setSpacing(6)
        self.gid = QLineEdit(hb)
        self.gid.setValidator(QIntValidator(0, 65535, self.gid))
        self.gid.setEnabled(False)
        lab.setBuddy(self.gid)
        self.gid_auto = QCheckBox(i18n("Select manually"), hb)
        w.connect(self.gid_auto, SIGNAL("toggled(bool)"), self.slotToggle)
        row = grid.numRows()
        grid.addWidget(lab, row, 0, Qt.AlignRight)
        grid.addWidget(hb, row, 1)
    
    def slotToggle(self, bool):
        self.gid.setEnabled(bool)
        self.stack.checkAdd()
    
    def text(self):
        if self.gid_auto.isChecked():
            return str(self.gid.text())
        else:
            return "auto"
    
    def check(self):
        t = self.text()
        if t == "":
            return i18n("Enter a group ID or use auto selection")
        return None


class Name:
    def __init__(self, stack, w, grid):
        self.stack = stack
        lab = QLabel(i18n("Name:"), w)
        self.name = QLineEdit(w)
        lab.setBuddy(self.name)
        self.name.setValidator(QRegExpValidator(QRegExp("[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_]*"), self.name))
        self.name.connect(self.name, SIGNAL("textChanged(const QString &)"), self.slotChange)
        row = grid.numRows()
        grid.addWidget(lab, row, 0, Qt.AlignRight)
        grid.addWidget(self.name, row, 1)
    
    def slotChange(self, text):
        self.stack.checkAdd()
    
    def text(self):
        return str(self.name.text())
    
    def check(self):
        if self.text() == "":
            return i18n("Enter a group name")
        return None


class GroupStack(QVBox):
    def __init__(self, parent, link):
        QVBox.__init__(self, parent)
        self.setMargin(6)
        self.setSpacing(24)
        
        lab = QLabel("<b>%s</b>" % i18n("Add a New Group"), self)
        
        hb = QHBox(self)
        
        w = QWidget(hb)
        hb.setStretchFactor(w, 2)
        grid = QGridLayout(w, 0, 0)
        grid.setSpacing(32)
        
        self.g_id = GID(self, w, grid)
        
        self.g_name = Name(self, w, grid)
        
        w2 = QWidget(w)
        hb2 = QHBoxLayout(w2)
        hb2.setMargin(6)
        hb2.setSpacing(6)
        lab = QLabel(w2)
        lab.setPixmap(getIconSet("help.png", KIcon.Panel).pixmap(QIconSet.Automatic, QIconSet.Normal))
        hb2.addWidget(lab, 0, hb2.AlignTop)
        self.info = KActiveLabel(" ", w2)
        hb2.addWidget(self.info)
        grid.addMultiCellWidget(w2, 2, 2, 0, 1)
        
        lab = QLabel(" ", hb)
        hb.setStretchFactor(lab, 1)
        
        hb = QHBox(self)
        hb.setSpacing(12)
        QLabel(" ", hb)
        but = QPushButton(getIconSet("add.png", KIcon.Small), i18n("Add"), hb)
        self.add_but = but
        self.connect(but, SIGNAL("clicked()"), self.slotAdd)
        but = QPushButton(getIconSet("cancel.png", KIcon.Small), i18n("Cancel"), hb)
        self.connect(but, SIGNAL("clicked()"), parent.slotCancel)
        
        self.link = link
        
        self.checkAdd()
    
    def slotAdd(self):
        if self.checkAdd():
            return
        
        dict = {}
        dict["gid"] = self.g_id.text()
        dict["name"] = self.g_name.text()
        
        self.link.call("User.Manager.addGroup", dict, 4)
        
        self.parent().slotCancel()
    
    def checkAdd(self):
        err = self.g_id.check()
        if not err:
            err = self.g_name.check()
        
        if err:
            self.info.setText(u"<font color=red>%s</font>" % err)
            self.add_but.setEnabled(False)
        else:
            self.info.setText("")
            self.add_but.setEnabled(True)
        
        return err

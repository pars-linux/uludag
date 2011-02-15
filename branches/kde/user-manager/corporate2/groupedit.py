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

from um_utility import *


class GID:
    def __init__(self, stack, w, grid):
        self.stack = stack
        lab = QLabel(i18n("ID:"), w)
        hb = QHBox(w)
        hb.setSpacing(6)
        self.gid = QLineEdit(hb)
        self.gid.connect(self.gid, SIGNAL("textChanged(const QString &)"), self.slotChange)
        self.gid.setValidator(QIntValidator(0, 65535, self.gid))
        self.gid.setEnabled(False)
        lab.setBuddy(self.gid)
        self.gid_auto = QCheckBox(i18n("Select manually"), hb)
        w.connect(self.gid_auto, SIGNAL("toggled(bool)"), self.slotToggle)
        row = grid.numRows()
        grid.addWidget(lab, row, 0, Qt.AlignRight)
        grid.addWidget(hb, row, 1)
    
    def slotChange(self, text):
        self.stack.guide.check()
    
    def slotToggle(self, bool):
        self.gid.setEnabled(bool)
        self.stack.guide.check()
    
    def text(self):
        if self.gid_auto.isChecked():
            return str(self.gid.text())
        else:
            return "auto"
    
    def setText(self, text):
        if text == "auto":
            self.gid_auto.setChecked(False)
            self.gid.setText("")
        else:
            self.gid_auto.setChecked(True)
            self.gid.setText(text)


class Name:
    def __init__(self, stack, w, grid):
        self.stack = stack
        lab = QLabel(i18n("Group name:"), w)
        self.name = QLineEdit(w)
        lab.setBuddy(self.name)
        self.name.setValidator(QRegExpValidator(QRegExp("[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_]*"), self.name))
        self.name.connect(self.name, SIGNAL("textChanged(const QString &)"), self.slotChange)
        row = grid.numRows()
        grid.addWidget(lab, row, 0, Qt.AlignRight)
        grid.addWidget(self.name, row, 1)
    
    def slotChange(self, text):
        self.stack.guide.check()
    
    def text(self):
        return str(self.name.text())
    
    def setText(self, text):
        self.name.setText(text)


class Guide(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        hb = QHBoxLayout(self)
        hb.setMargin(6)
        hb.setSpacing(6)
        lab = QLabel(self)
        lab.setPixmap(getIconSet("help.png", KIcon.Panel).pixmap(QIconSet.Automatic, QIconSet.Normal))
        hb.addWidget(lab, 0, hb.AlignTop)
        self.info = KActiveLabel(" ", self)
        hb.addWidget(self.info)

    def check(self):
        err = None
        p = self.parent()

        if p.g_id.text() == "":
            err = i18n("Enter a group ID or use auto selection")

        if not err and p.g_name.text() == "":
            err = i18n("Enter a group name")

        if err:
            self.info.setText(u"<font color=red>%s</font>" % err)
            self.ok_but.setEnabled(False)
        else:
            self.info.setText("")
            self.ok_but.setEnabled(True)

        return err

    def op_start(self, msg):
        self.buttons.setEnabled(False)
        self.info.setText(msg)
    
    def op_end(self, msg=None):
        self.buttons.setEnabled(True)
        if msg:
            self.info.setText(u"<big><font color=red>%s</font></big>" % msg)


class GroupStack(QVBox):
    def __init__(self, parent):
        QVBox.__init__(self, parent)
        self.setMargin(6)
        self.setSpacing(6)
        
        self.mainwidget = parent
        
        lab = QLabel(u"<big><b>%s</b></big>" % i18n("Enter Information For New Group"), self)
        
        hb = QHBox(self)
        
        w = QWidget(hb)
        hb.setStretchFactor(w, 2)
        grid = QGridLayout(w, 0, 0)
        grid.setSpacing(6)
        
        grid.addWidget(QLabel(" ", w), grid.numRows(), 0)
        
        self.g_id = GID(self, w, grid)
        
        grid.addWidget(QLabel(" ", w), grid.numRows(), 0)
        
        self.g_name = Name(self, w, grid)
        
        grid.addWidget(QLabel(" ", w), grid.numRows(), 0)
        
        lab = QLabel(" ", hb)
        hb.setStretchFactor(lab, 1)
        
        self.guide = Guide(self)
        
        hb = QHBox(self)
        hb.setSpacing(12)
        QLabel(" ", hb)
        but = QPushButton(getIconSet("add.png", KIcon.Small), i18n("Add"), hb)
        self.guide.ok_but = but
        self.connect(but, SIGNAL("clicked()"), self.slotAdd)
        but = QPushButton(getIconSet("cancel.png", KIcon.Small), i18n("Cancel"), hb)
        self.connect(but, SIGNAL("clicked()"), parent.slotCancel)
        
        self.guide.buttons = hb
    
    def slotAdd(self):
        if self.guide.check():
            return

        self.guide.op_start(i18n("Adding group..."))

        def handler(package, exception, args):
            if exception:
                self.parent().slotCancel()
                return
            gid = args[0]
            self.parent().browse.groupModified(gid, self.g_name.text())
            self.guide.op_end()
            self.parent().slotCancel()

        if self.g_id.text() == "auto":
            gid = -1
        else:
            gid = int (self.g_id.text())

        self.mainwidget.link.User.Manager["baselayout"].addGroup(gid, self.g_name.text(), async=handler)
    
    def startAdd(self):
        self.g_id.setText("auto")
        self.g_name.setText("")
        self.guide.check()
        self.g_name.name.setFocus()

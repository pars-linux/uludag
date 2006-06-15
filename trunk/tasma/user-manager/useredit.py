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


class UID:
    def __init__(self, w, grid):
        lab = QLabel(i18n("ID:"), w)
        hb = QHBox(w)
        hb.setSpacing(6)
        self.uid = QLineEdit(hb)
        self.uid.setValidator(QIntValidator(0, 65535, self.uid))
        self.uid.setEnabled(False)
        self.uid_auto = QCheckBox(i18n("Select manually"), hb)
        w.connect(self.uid_auto, SIGNAL("toggled(bool)"), self.slotToggle)
        row = grid.numRows()
        grid.addWidget(lab, row, 0, Qt.AlignRight)
        grid.addWidget(hb, row, 1)
    
    def slotToggle(self, bool):
        self.uid.setEnabled(bool)
    
    def text(self):
        if self.uid_auto.isChecked():
            return int(self.uid.text())
        else:
            return "auto"


class Homedir:
    def __init__(self, w, grid):
        self.w = w
        lab = QLabel(i18n("Home:"), w)
        hb = QHBox(w)
        hb.setSpacing(3)
        self.home = QLineEdit(hb)
        but = QPushButton("...", hb)
        w.connect(but, SIGNAL("clicked()"), self.browse)
        self.home_create = QCheckBox("Create directory", w)
        
        row = grid.numRows()
        grid.addWidget(lab, row, 0, Qt.AlignRight)
        grid.addWidget(hb, row, 1)
        grid.addWidget(self.home_create, row + 1, 1)
    
    def browse(self):
        s = QFileDialog.getExistingDirectory(
            self.home.text(),
            self.w,
            "lala",
            i18n("Select user's home directory"),
            False
        )
        self.home.setText(s)


class Password:
    def __init__(self, w, grid):
        lab = QLabel(i18n("Password:"), w)
        self.password = QLineEdit(w)
        self.password.setEchoMode(QLineEdit.Password)
        
        lab2 = QLabel(i18n("Confirm password:"), w)
        self.password2 = QLineEdit(w)
        self.password2.setEchoMode(QLineEdit.Password)
        
        row = grid.numRows()
        grid.addWidget(lab, row, 0, Qt.AlignRight)
        grid.addWidget(self.password, row, 1)
        row += 1
        grid.addWidget(lab2, row, 0, Qt.AlignRight)
        grid.addWidget(self.password2, row, 1)


class UserGroup(QCheckListItem):
    def __init__(self, parent, group):
        QCheckListItem.__init__(self, parent, group.name, self.CheckBox)
        self.name = group.name
        self.comment = group.comment
        self.desc = group.desc
    
    def text(self, col):
        return (self.name, self.comment)[col]
    
    def compare(self, item, col, ascend):
        if self.comment != "" and item.comment == "":
            return -1
        if self.comment == "" and item.comment != "":
            return 1
        
        return QCheckListItem.compare(self, item, 0, 0)


class UserStack(QVBox):
    def __init__(self, parent, link):
        QVBox.__init__(self, parent)
        self.setMargin(6)
        self.setSpacing(6)
        
        w = QWidget(self)
        hb = QHBoxLayout(w)
        lab = QLabel(u"<b>%s</b>" % i18n("Add a New User"), w)
        hb.addWidget(lab)
        toggle = QCheckBox("Show all groups", w)
        self.connect(toggle, SIGNAL("toggled(bool)"), self.slotToggle)
        hb.addWidget(toggle, 0, Qt.AlignRight)
        
        hb = QHBox(self)
        hb.setSpacing(18)
        
        w = QWidget(hb)
        grid = QGridLayout(w, 0, 0)
        grid.setSpacing(6)
        
        self.u_id = UID(w, grid)
        
        lab = QLabel("Name:", w)
        self.w_nick = QLineEdit(w)
        grid.addWidget(lab, 1, 0, Qt.AlignRight)
        grid.addWidget(self.w_nick, 1, 1)
        
        lab = QLabel("Real name:", w)
        self.w_name = QLineEdit(w)
        grid.addWidget(lab, 2, 0, Qt.AlignRight)
        grid.addWidget(self.w_name, 2, 1)
        
        self.u_home = Homedir(w, grid)
        
        lab = QLabel("Shell:", w)
        self.w_shell = QComboBox(True, w)
        self.w_shell.insertItem("/bin/bash", 0)
        self.w_shell.insertItem("/bin/false", 1)
        grid.addWidget(lab, 5, 0, Qt.AlignRight)
        grid.addWidget(self.w_shell, 5, 1)
        
        self.u_password = Password(w, grid)
        
        self.info = QLabel(" ", w)
        grid.addWidget(self.info, 8, 1)
        
        w = QWidget(hb)
        vb = QVBoxLayout(w)
        vb.setSpacing(3)
        
        self.groups = QListView(w)
        self.connect(self.groups, SIGNAL("selectionChanged()"), self.slotSelect)
        self.groups.addColumn("Group")
        self.groups.addColumn("Permission")
        self.groups.setResizeMode(QListView.LastColumn)
        self.groups.setAllColumnsShowFocus(True)
        vb.addWidget(self.groups, 2)
        
        hb = QHBox(w)
        lab = QLabel("Main group:", hb)
        self.w_main_group = QComboBox(False, hb)
        vb.addWidget(hb)
        
        self.desc = QTextEdit(w)
        self.desc.setReadOnly(True)
        vb.addWidget(self.desc, 1)
        
        hb = QHBox(self)
        hb.setSpacing(12)
        QLabel(" ", hb)
        but = QPushButton(getIconSet("add.png", KIcon.Small), i18n("Add"), hb)
        self.connect(but, SIGNAL("clicked()"), self.slotAdd)
        but = QPushButton(getIconSet("cancel.png", KIcon.Small), i18n("Cancel"), hb)
        self.connect(but, SIGNAL("clicked()"), parent.slotCancel)
    
    def slotSelect(self):
        item = self.groups.selectedItem()
        if item:
            self.desc.setText("<b>%s</b><br>%s" % (item.name, item.desc))
        else:
            self.desc.setText("")
    
    def slotToggle(self, bool):
        group = self.groups.firstChild()
        while group:
            if not group.comment:
                group.setVisible(bool)
            group = group.nextSibling()
    
    def slotAdd(self):
        #FIXME: check and add
        self.parent().slotCancel()
    
    def startAdd(self, groups):
        group = groups.firstChild()
        self.groups.clear()
        while group:
            g = UserGroup(self.groups, group)
            if not g.comment:
                g.setVisible(False)
            self.w_main_group.insertItem(g.name)
            group = group.nextSibling()

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

from utility import getIconSet


class PathEntry(QHBox):
    def __init__(self, parent, question, is_dir=True):
        QHBox.__init__(self, parent)
        self.is_dir = is_dir
        self.question = question
        self.setSpacing(3)
        self.path = QLineEdit(self)
        self.path.setMinimumWidth(160)
        but = QPushButton("...", self)
        self.connect(but, SIGNAL("clicked()"), self.browse)

    def browse(self):
        if self.is_dir:
            s = QFileDialog.getExistingDirectory(self.path.text(), self, "lala", self.question, False)
        else:
            s = QFileDialog.getOpenFileName(self.path.text(), "All (*)", self, "lala", self.question)
        self.path.setText(s)

    def text(self):
        return str(self.path.text())

    def setText(self, text):
        self.path.setText(text)


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
        lab = QLabel("<b>Add a New User</b>", w)
        hb.addWidget(lab)
        toggle = QRadioButton("Show all groups", w)
        self.connect(toggle, SIGNAL("toggled(bool)"), self.slotToggle)
        hb.addWidget(toggle, 0, Qt.AlignRight)
        
        hb = QHBox(self)
        hb.setSpacing(12)
        
        w = QWidget(hb)
        grid = QGridLayout(w)
        grid.setSpacing(6)
        
        lab = QLabel("ID:", w)
        hb2 = QHBox(w)
        hb2.setSpacing(6)
        self.w_id = QLineEdit(hb2)
        self.w_id_auto = QRadioButton("Automatic", hb2)
        grid.addWidget(lab, 0, 0, Qt.AlignRight)
        grid.addWidget(hb2, 0, 1)
        
        lab = QLabel("Name:", w)
        self.w_nick = QLineEdit(w)
        grid.addWidget(lab, 1, 0, Qt.AlignRight)
        grid.addWidget(self.w_nick, 1, 1)
        
        lab = QLabel("Real name:", w)
        self.w_name = QLineEdit(w)
        grid.addWidget(lab, 2, 0, Qt.AlignRight)
        grid.addWidget(self.w_name, 2, 1)
        
        lab = QLabel("Main group:", w)
        grid.addWidget(lab, 3, 0, Qt.AlignRight)
        self.w_main_group = QComboBox(False, w)
        grid.addWidget(self.w_main_group, 3, 1)
        
        lab = QLabel("Home:", w)
        self.w_home = PathEntry(w, "Select home directory for user")
        grid.addWidget(lab, 4, 0, Qt.AlignRight)
        grid.addWidget(self.w_home, 4, 1)
        
        self.w_home_create = QRadioButton("Create directory", w)
        grid.addWidget(self.w_home_create, 5, 1)
        
        lab = QLabel("Shell:", w)
        self.w_shell = QComboBox(True, w)
        self.w_shell.insertItem("/bin/bash", 0)
        self.w_shell.insertItem("/bin/false", 1)
        grid.addWidget(lab, 6, 0, Qt.AlignRight)
        grid.addWidget(self.w_shell, 6, 1)
        
        lab = QLabel("Password:", w)
        self.w_pass = QLineEdit(w)
        self.w_pass.setEchoMode(self.w_pass.Password)
        grid.addWidget(lab, 7, 0, Qt.AlignRight)
        grid.addWidget(self.w_pass, 7, 1)
        
        lab = QLabel("Confirm password:", w)
        self.w_pass2 = QLineEdit(w)
        self.w_pass2.setEchoMode(self.w_pass2.Password)
        grid.addWidget(lab, 8, 0, Qt.AlignRight)
        grid.addWidget(self.w_pass2, 8, 1)
        
        lab = QLabel(" ", w)
        grid.addWidget(lab, 9, 1)
        
        w = QWidget(hb)
        vb = QVBoxLayout(w)
        vb.setSpacing(3)
        
        self.groups = QListView(w)
        self.connect(self.groups, SIGNAL("selectionChanged()"), self.slotSelect)
        self.groups.addColumn("Group")
        self.groups.addColumn("Permission")
        self.groups.setResizeMode(QListView.LastColumn)
        self.groups.setAllColumnsShowFocus(True)
        vb.addWidget(self.groups)
        
        self.desc = QTextEdit(w)
        self.desc.setReadOnly(True)
        vb.addWidget(self.desc)
        
        hb = QHBox(self)
        hb.setSpacing(12)
        QLabel(" ", hb)
        but = QPushButton(getIconSet("add.png", KIcon.Small), "Add", hb)
        self.connect(but, SIGNAL("clicked()"), self.slotAdd)
        but = QPushButton(getIconSet("cancel.png", KIcon.Small), "Cancel", hb)
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

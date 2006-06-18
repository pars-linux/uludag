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

import os

from qt import *
from kdecore import *
from kdeui import *

from utility import *


class UID:
    def __init__(self, stack, w, grid):
        self.stack = stack
        lab = QLabel(i18n("ID:"), w)
        hb = QHBox(w)
        hb.setSpacing(6)
        self.uid = QLineEdit(hb)
        lab.setBuddy(self.uid)
        self.uid.setValidator(QIntValidator(0, 65535, self.uid))
        self.uid.setEnabled(False)
        self.uid_auto = QCheckBox(i18n("Select manually"), hb)
        w.connect(self.uid_auto, SIGNAL("toggled(bool)"), self.slotToggle)
        row = grid.numRows()
        grid.addWidget(lab, row, 0, Qt.AlignRight)
        grid.addWidget(hb, row, 1)
    
    def slotToggle(self, bool):
        self.uid.setEnabled(bool)
        self.stack.checkAdd()
    
    def text(self):
        if self.uid_auto.isChecked():
            return str(self.uid.text())
        else:
            return "auto"
    
    def check(self):
        t = self.text()
        if t == "":
            return i18n("Enter a user ID or use auto selection")
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
        self.stack.u_home.guess(text)
    
    def text(self):
        return str(self.name.text())
    
    def check(self):
        if self.text() == "":
            return i18n("Enter a user name")
        return None


class RealName:
    def __init__(self, w, grid):
        lab = QLabel(i18n("Real name:"), w)
        self.name = QLineEdit(w)
        lab.setBuddy(self.name)
        self.name.setValidator(QRegExpValidator(QRegExp("[^\n:]*"), self.name))
        row = grid.numRows()
        grid.addWidget(lab, row, 0, Qt.AlignRight)
        grid.addWidget(self.name, row, 1)
    
    def text(self):
        return str(self.name.text())


class Homedir:
    def __init__(self, w, grid):
        self.w = w
        lab = QLabel(i18n("Home:"), w)
        hb = QHBox(w)
        hb.setSpacing(3)
        self.home = QLineEdit(hb)
        lab.setBuddy(self.home)
        but = QPushButton("...", hb)
        w.connect(but, SIGNAL("clicked()"), self.browse)
        
        row = grid.numRows()
        grid.addWidget(lab, row, 0, Qt.AlignRight)
        grid.addWidget(hb, row, 1)
    
    def guess(self, name):
        cur = unicode(self.home.text())
        if cur == "" or cur.startswith("/home/"):
            self.home.setText("/home/" + name)
    
    def text(self):
        return unicode(self.home.text())
    
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
    def __init__(self, stack, w, grid):
        self.stack = stack
        lab = QLabel(i18n("Password:"), w)
        self.password = QLineEdit(w)
        lab.setBuddy(self.password)
        self.password.connect(self.password, SIGNAL("textChanged(const QString &)"), self.slotChange)
        self.password.setEchoMode(QLineEdit.Password)
        
        lab2 = QLabel(i18n("Confirm password:"), w)
        self.password2 = QLineEdit(w)
        lab2.setBuddy(self.password2)
        self.password2.connect(self.password2, SIGNAL("textChanged(const QString &)"), self.slotChange)
        self.password2.setEchoMode(QLineEdit.Password)
        
        row = grid.numRows()
        grid.addWidget(lab, row, 0, Qt.AlignRight)
        grid.addWidget(self.password, row, 1)
        row += 1
        grid.addWidget(lab2, row, 0, Qt.AlignRight)
        grid.addWidget(self.password2, row, 1)
    
    def slotChange(self, text):
        self.stack.checkAdd()
    
    def text(self):
        return unicode(self.password.text())
    
    def check(self):
        if self.password.text() == "":
            return i18n("You should enter a password for this user")
        if self.password.text() != self.password2.text():
            return i18n("Passwords don't match")
        return None


class Shell:
    def __init__(self, stack, w, grid):
        self.stack = stack
        lab = QLabel(i18n("Shell:"), w)
        self.shell = QComboBox(True, w)
        lab.setBuddy(self.shell)
        self.shell.insertItem("/bin/bash", 0)
        self.shell.insertItem("/bin/false", 1)
        self.shell.connect(self.shell, SIGNAL("textChanged(const QString &)"), self.slotChange)
        row = grid.numRows()
        grid.addWidget(lab, row, 0, Qt.AlignRight)
        grid.addWidget(self.shell, row, 1)
    
    def slotChange(self, text):
        self.stack.checkAdd()
    
    def text(self):
        return unicode(self.shell.currentText())
    
    def check(self):
        path = unicode(self.shell.currentText())
        if not os.path.isfile(path):
            return i18n("Please specify an existing shell command")
        if not os.access(path, os.X_OK):
            return i18n("Specified shell command is not executable")
        return None


class UserGroup(QCheckListItem):
    def __init__(self, stack, parent, group):
        self.stack = stack
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
    
    def stateChange(self, bool):
        self.stack.slotGroup()


class UserGroupList(QWidget):
    def __init__(self, stack, parent):
        QWidget.__init__(self, parent)
        self.stack = stack
        vb = QVBoxLayout(self)
        vb.setSpacing(3)
        
        self.groups = QListView(self)
        self.connect(self.groups, SIGNAL("selectionChanged()"), self.slotSelect)
        self.groups.addColumn(i18n("Group"))
        self.groups.addColumn(i18n("Permission"))
        self.groups.setResizeMode(QListView.LastColumn)
        self.groups.setAllColumnsShowFocus(True)
        vb.addWidget(self.groups, 2)
        
        w = QWidget(self)
        hb = QHBoxLayout(w)
        lab = QLabel(i18n("Main group:"), w)
        hb.addWidget(lab, 0, Qt.AlignRight)
        self.main_group = QComboBox(False, w)
        self.main_group.setEnabled(False)
        lab.setBuddy(self.main_group)
        hb.addWidget(self.main_group)
        vb.addWidget(w)
        
        self.desc = QTextEdit(self)
        self.desc.setReadOnly(True)
        vb.addWidget(self.desc, 1)
    
    def populate(self, groups):
        group = groups.firstChild()
        self.groups.clear()
        while group:
            g = UserGroup(self, self.groups, group)
            if not g.comment:
                g.setVisible(False)
            group = group.nextSibling()
    
    def slotGroup(self):
        groups = []
        item = self.groups.firstChild()
        while item:
            if item.state() == item.On:
                groups.append(item.name)
            item = item.nextSibling()
        self.main_group.clear()
        if groups == []:
            self.main_group.setEnabled(False)
        else:
            self.main_group.setEnabled(True)
            for item in groups:
                self.main_group.insertItem(item)
        self.stack.checkAdd()
    
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
    
    def text(self):
        groups = []
        group = self.groups.firstChild()
        while group:
            if group.state() == group.On:
                groups.append(group.name)
            group = group.nextSibling()
        return ",".join(groups)
    
    def check(self):
        if self.main_group.count() == 0:
            return i18n("You should select at least one group this user belongs to")
        return None


class UserStack(QVBox):
    def __init__(self, parent, link):
        QVBox.__init__(self, parent)
        self.setMargin(6)
        self.setSpacing(6)
        
        w = QWidget(self)
        hb = QHBoxLayout(w)
        lab = QLabel(u"<b>%s</b>" % i18n("Add a New User"), w)
        hb.addWidget(lab)
        toggle = QCheckBox(i18n("Show all groups"), w)
        hb.addWidget(toggle, 0, Qt.AlignRight)
        
        hb = QHBox(self)
        hb.setSpacing(18)
        
        w = QWidget(hb)
        grid = QGridLayout(w, 0, 0)
        grid.setSpacing(9)
        
        self.u_id = UID(self, w, grid)
        
        self.u_name = Name(self, w, grid)
        
        self.u_password = Password(self, w, grid)
        
        self.u_realname = RealName(w, grid)
        
        line = QFrame(w)
        line.setFrameStyle(QFrame.HLine | QFrame.Sunken)
        row = grid.numRows()
        grid.addMultiCellWidget(line, row, row, 0, 1)
        
        self.u_home = Homedir(w, grid)
        
        self.u_shell = Shell(self, w, grid)
        
        line = QFrame(w)
        line.setFrameStyle(QFrame.HLine | QFrame.Sunken)
        row = grid.numRows()
        grid.addMultiCellWidget(line, row, row, 0, 1)
        
        w2 = QWidget(w)
        hb2 = QHBoxLayout(w2)
        hb2.setMargin(6)
        hb2.setSpacing(6)
        lab = QLabel(w2)
        lab.setPixmap(getIconSet("help.png", KIcon.Panel).pixmap(QIconSet.Automatic, QIconSet.Normal))
        hb2.addWidget(lab, 0, hb2.AlignTop)
        self.info = KActiveLabel(" ", w2)
        hb2.addWidget(self.info)
        grid.addMultiCellWidget(w2, 9, 9, 0, 1)
        
        self.u_groups = UserGroupList(self, hb)
        self.connect(toggle, SIGNAL("toggled(bool)"), self.u_groups.slotToggle)
        
        hb = QHBox(self)
        hb.setSpacing(12)
        QLabel(" ", hb)
        but = QPushButton(getIconSet("add.png", KIcon.Small), i18n("Add"), hb)
        self.add_but = but
        self.connect(but, SIGNAL("clicked()"), self.slotAdd)
        but = QPushButton(getIconSet("cancel.png", KIcon.Small), i18n("Cancel"), hb)
        self.connect(but, SIGNAL("clicked()"), parent.slotCancel)
        
        self.checkAdd()
    
    def checkAdd(self):
        err = self.u_id.check()
        if not err:
            err = self.u_name.check()
        if not err:
            err = self.u_password.check()
        if not err:
            err = self.u_groups.check()
        if not err:
            err = self.u_shell.check()
        
        if err:
            self.info.setText(u"<font color=red>%s</font>" % err)
            self.add_but.setEnabled(False)
        else:
            self.info.setText("")
            self.add_but.setEnabled(True)
        
        return err
    
    def slotAdd(self):
        if self.checkAdd():
            return
        
        dict = {}
        dict["uid"] = self.u_id.text()
        dict["name"] = self.u_name.text()
        dict["realname"] = self.u_realname.text()
        dict["password"] = self.u_password.text()
        dict["homedir"] = self.u_home.text()
        dict["groups"] = self.u_groups.text()
        
        self.link.call("User.Manager.addUser", dict, 3)
        
        self.parent().slotCancel()
    
    def startAdd(self, groups):
        self.u_groups.populate(groups)

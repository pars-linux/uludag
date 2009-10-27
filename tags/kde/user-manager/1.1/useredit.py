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
    def __init__(self, stack, w, grid, edit=False):
        self.edit = edit
        self.stack = stack
        lab = QLabel(i18n("ID:"), w)
        if edit:
            self.uid = QLabel(w)
            hb = self.uid
        else:
            hb = QHBox(w)
            hb.setSpacing(6)
            self.uid = QLineEdit(hb)
            self.uid.connect(self.uid, SIGNAL("textChanged(const QString &)"), self.slotChange)
            lab.setBuddy(self.uid)
            self.uid.setValidator(QIntValidator(0, 65535, self.uid))
            self.uid.setEnabled(False)
            self.uid_auto = QCheckBox(i18n("Select manually"), hb)
            w.connect(self.uid_auto, SIGNAL("toggled(bool)"), self.slotToggle)
        row = grid.numRows()
        grid.addWidget(lab, row, 0, Qt.AlignRight)
        grid.addWidget(hb, row, 1)
    
    def slotChange(self, text):
        self.stack.checkAdd()
    
    def slotToggle(self, bool):
        self.uid.setEnabled(bool)
        self.stack.checkAdd()
    
    def setText(self, text):
        if text == "auto":
            if not self.edit:
                self.uid_auto.setChecked(False)
            self.uid.setText("")
        else:
            if not self.edit:
                self.uid_auto.setChecked(True)
            self.uid.setText(text)
    
    def text(self):
        if self.edit or self.uid_auto.isChecked():
            return str(self.uid.text())
        else:
            return "auto"


class Name:
    def __init__(self, stack, w, grid, edit=False):
        self.stack = stack
        self.edit = edit
        self.usednames = []
        lab = QLabel(i18n("User name:"), w)
        if edit:
            self.name = QLabel(w)
        else:
            self.name = QLineEdit(w)
            lab.setBuddy(self.name)
            self.name.setValidator(QRegExpValidator(QRegExp("[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_]*"), self.name))
            self.name.connect(self.name, SIGNAL("textChanged(const QString &)"), self.slotChange)
        row = grid.numRows()
        grid.addWidget(lab, row, 0, Qt.AlignRight)
        grid.addWidget(self.name, row, 1)
    
    def slotChange(self, text):
        self.stack.checkAdd()
        if not self.edit:
            self.stack.u_home.guess(text)
    
    def guess(self, text):
        self.setText(nickGuess(text, self.usednames))
    
    def text(self):
        return str(self.name.text())
    
    def setText(self, text):
        self.name.setText(text)


class RealName:
    def __init__(self, stack, w, grid, edit=False):
        self.stack = stack
        self.edit = edit
        lab = QLabel(i18n("Full name:"), w)
        self.name = QLineEdit(w)
        lab.setBuddy(self.name)
        self.name.setValidator(QRegExpValidator(QRegExp("[^\n:]*"), self.name))
        self.name.connect(self.name, SIGNAL("textChanged(const QString &)"), self.slotChange)
        row = grid.numRows()
        grid.addWidget(lab, row, 0, Qt.AlignRight)
        grid.addWidget(self.name, row, 1)
    
    def slotChange(self, text):
        if not self.edit:
            self.stack.u_name.guess(text)
    
    def setText(self, text):
        self.name.setText(text)
    
    def text(self):
        return unicode(self.name.text())


class Homedir:
    def __init__(self, w, grid, edit):
        self.w = w
        lab = QLabel(i18n("Home:"), w)
        if edit:
            self.home = QLabel(w)
            hb = self.home
        else:
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
    
    def setText(self, text):
        self.home.setText(text)
    
    def browse(self):
        s = QFileDialog.getExistingDirectory(
            self.text(),
            self.w,
            "lala",
            i18n("Select user's home directory"),
            False
        )
        self.setText(s)


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
        if self.password.text() != self.password2.text():
            return None
        return unicode(self.password.text())
    
    def setText(self, text):
        self.password.setText(text)
        self.password2.setText(text)


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
    
    def setText(self, text):
        self.shell.setCurrentText(text)
    
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


class Tipper(QToolTip):
    def maybeTip(self, point):
        item = self.list.itemAt(point)
        if item:
            self.tip(self.list.itemRect(item), "<b>%s</b><br>%s" % (item.name, item.desc))


class UserGroupList(QWidget):
    def __init__(self, stack, parent):
        QWidget.__init__(self, parent)
        self.stack = stack
        vb = QVBoxLayout(self)
        vb.setSpacing(3)
        
        self.groups = QListView(self)
        self.groups.addColumn(i18n("Group"))
        self.groups.addColumn(i18n("Permission"))
        self.groups.setResizeMode(QListView.LastColumn)
        self.groups.setAllColumnsShowFocus(True)
        vb.addWidget(self.groups, 2)
        
        self.tipper = Tipper(self.groups.viewport())
        self.tipper.list = self.groups
        
        w = QWidget(self)
        hb = QHBoxLayout(w)
        lab = QLabel(i18n("Main group:"), w)
        hb.addWidget(lab, 0, Qt.AlignRight)
        self.main_group = QComboBox(False, w)
        self.connect(self.main_group, SIGNAL("activated(const QString &)"), self.slotMain)
        self.main_group.setEnabled(False)
        lab.setBuddy(self.main_group)
        hb.addWidget(self.main_group)
        vb.addWidget(w)
    
    def populate(self, groups):
        self.main_sel = None
        self.toggle.setChecked(False)
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
            if self.main_sel and self.main_sel in groups:
                self.main_group.setCurrentText(self.main_sel)
            else:
                self.main_sel = groups[0]
        self.stack.checkAdd()
    
    def slotMain(self, text):
        self.main_sel = unicode(text)
    
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
        main = unicode(self.main_group.currentText())
        if main in groups:
            groups.remove(main)
            groups.insert(0, main)
        return ",".join(groups)
    
    def setText(self, groups):
        self.main_sel = None
        if groups == "":
            return
        groups = groups.split(",")
        if len(groups) > 0:
            item = self.groups.firstChild()
            while item:
                if item.name in groups:
                    item.setState(item.On)
                item = item.nextSibling()
            self.main_sel = groups[0]
            self.main_group.setCurrentText(groups[0])


class Guide(QWidget):
    def __init__(self, parent, edit):
        QWidget.__init__(self, parent)
        self.edit = edit
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
        
        if p.u_realname.text() == "" and p.u_name.text() == "":
            err = i18n("Start with typing this user's full name.")
        
        if not err and not self.edit and p.u_password.text() == "":
            err = i18n("You should enter a password for this user.")
        
        if not err:
            pw = unicode(p.u_password.password.text())
            if pw != "" and len(pw) < 4:
                err = i18n("Password must be longer.")
            
            if not err:
                if pw == p.u_realname.text() or pw == p.u_name.text():
                    err = i18n("Dont use your full name or user name as a password.")
        
        if not err and p.u_password.text() == None:
            err = i18n("Passwords don't match.")
        
        if not err and p.u_id.text() == "":
            err = i18n("You must enter a user ID or use the auto selection.")
        
        nick = p.u_name.text()
        
        if not err and nick == "":
            err = i18n("You must enter a user name.")
        
        if not err and nick in p.u_name.usednames:
            err = i18n("This user name is used by another user.")
        
        if not err:
            if len(nick) > 0 and nick[0] >= "0" and nick[0] <= "9":
                err = i18n("User name must not start with a number.")
        
        if not err and p.u_groups.text() == "":
            err = i18n("You should select at least one group this user belongs to.")
        
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


class UserStack(QVBox):
    def __init__(self, parent, link, edit=False):
        QVBox.__init__(self, parent)
        self.setMargin(6)
        self.setSpacing(6)
        
        w = QWidget(self)
        hb = QHBoxLayout(w)
        hb.setMargin(6)
        if edit:
            lab = QLabel(u"<b><big>%s</big></b>" % i18n("Edit User's Information"), w)
        else:
            lab = QLabel(u"<b><big>%s</big></b>" % i18n("Enter Information For New User"), w)
        hb.addWidget(lab)
        toggle = QCheckBox(i18n("Show all groups"), w)
        hb.addWidget(toggle, 0, Qt.AlignRight)
        
        hb = QHBox(self)
        self.setStretchFactor(hb, 4)
        hb.setSpacing(18)
        
        w = QWidget(hb)
        grid = QGridLayout(w, 0, 0)
        grid.setSpacing(9)
        
        self.u_realname = RealName(self, w, grid, edit)
        
        self.u_password = Password(self, w, grid)
        
        line = QFrame(w)
        line.setFrameStyle(QFrame.HLine | QFrame.Sunken)
        row = grid.numRows()
        grid.addMultiCellWidget(line, row, row, 0, 1)
        
        self.u_id = UID(self, w, grid, edit)
        
        self.u_name = Name(self, w, grid, edit)
        
        self.u_home = Homedir(w, grid, edit)
        
        self.u_shell = Shell(self, w, grid)
        
        line = QFrame(w)
        line.setFrameStyle(QFrame.HLine | QFrame.Sunken)
        row = grid.numRows()
        grid.addMultiCellWidget(line, row, row, 0, 1)
        
        lab = KActiveLabel(w)
        row = grid.numRows()
        grid.addMultiCellWidget(lab, row, row, 0, 1)
        
        self.u_groups = UserGroupList(self, hb)
        self.u_groups.toggle = toggle
        self.connect(toggle, SIGNAL("toggled(bool)"), self.u_groups.slotToggle)
        
        self.guide = Guide(self, edit)
        self.setStretchFactor(self.guide, 1)
        
        hb = QHBox(self)
        self.guide.buttons = hb
        hb.setSpacing(12)
        QLabel(" ", hb)
        if edit:
            but = QPushButton(getIconSet("apply.png", KIcon.Small), i18n("Apply"), hb)
            self.connect(but, SIGNAL("clicked()"), self.slotEdit)
        else:
            but = QPushButton(getIconSet("add.png", KIcon.Small), i18n("Add"), hb)
            self.connect(but, SIGNAL("clicked()"), self.slotAdd)
        self.guide.ok_but = but
        but = QPushButton(getIconSet("cancel.png", KIcon.Small), i18n("Cancel"), hb)
        self.connect(but, SIGNAL("clicked()"), parent.slotCancel)
        
        self.link = link
    
    def checkAdd(self):
       return self.guide.check()
    
    def slotEdit(self):
        if self.checkAdd():
            return
        
        dict = self.editdict.copy()
        tmp = self.u_realname.text()
        if tmp == dict["realname"]:
            del dict["realname"]
        else:
            dict["realname"] = tmp
        tmp = self.u_password.text()
        if tmp:
            dict["password"] = tmp
        tmp = self.u_shell.text()
        if tmp == dict["shell"]:
            del dict["shell"]
        else:
            dict["shell"] = tmp
        tmp = self.u_groups.text()
        tmpA = set(tmp.split(","))
        tmpB = set(dict["groups"].split(","))
        if tmpA == tmpB:
            del dict["groups"]
        else:
            if int(dict["uid"]) == os.getuid() and not "wheel" in tmpA and "wheel" in tmpB:
                ret = KMessageBox.warningContinueCancel(
                    self,
                    i18n("You are removing yourself from the 'wheel' system group, you might not use your administrator permissions after that."),
                    i18n("Important Group Change")
                )
                if ret == KMessageBox.Cancel:
                    return
            dict["groups"] = tmp
        
        if len(dict) > 1:
            self.guide.op_start(i18n("Changing user information..."))
            self.link.call("User.Manager.setUser", dict, 6)
    
    def slotEditReply(self, reply):
        if reply.command == "result":
            dict = self.editdict
            tmp = dict.get("realname", None)
            if tmp:
                self.parent().browse.userModified(int(dict["uid"]), realname=tmp)
            self.parent().slotCancel()
            return
        
        if reply.command == "fail":
            msg = unicode(i18n("Operation failed, reason:<br>%s")) % reply.data
        elif reply.command == "denied":
            msg = i18n("You are not allowed to do that")
        else:
            msg = i18n("Comar script error :(")
        
        self.guide.op_end(msg)
    
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
        self.adddict = dict
        
        self.guide.op_start(i18n("Adding user..."))
        self.link.call("User.Manager.addUser", dict, 3)
    
    def slotAddReply(self, reply):
        if reply.command == "result":
            dict = self.adddict
            self.parent().browse.userModified(int(reply.data), dict["name"], dict["realname"])
            self.parent().slotCancel()
            return
        
        if reply.command == "fail":
            msg = unicode(i18n("Operation failed, reason:<br>%s")) % reply.data
        elif reply.command == "denied":
            msg = i18n("You are not allowed to do that")
        else:
            msg = i18n("Comar script error :(")
        
        self.guide.op_end(msg)
    
    def reset(self):
        self.u_id.setText("auto")
        self.u_name.setText("")
        self.u_realname.setText("")
        self.u_password.setText("")
        self.u_home.setText("")
        self.u_groups.setText("")
        self.checkAdd()
    
    def startAdd(self, groups, names):
        self.u_groups.populate(groups)
        self.reset()
        self.u_name.usednames = names
        self.u_groups.setText("users,audio,pnp,removable")
        self.guide.op_end()
        self.u_realname.name.setFocus()
    
    def startEdit(self, groups, uid):
        self.u_groups.populate(groups)
        self.reset()
        self.editdict = None
        self.guide.op_start(i18n("Getting user information..."))
        self.link.call("User.Manager.userInfo", [ "uid", uid ], 5)
    
    def slotInfo(self, reply):
        self.guide.op_end()
        dict = {}
        for line in unicode(reply.data).split("\n"):
            key, value = line.split(" ", 1)
            if key == "uid":
                self.u_id.setText(value)
                dict["uid"] = value
            elif key == "name":
                self.u_name.setText(value)
            elif key == "realname":
                self.u_realname.setText(value)
                dict["realname"] = value
            elif key == "homedir":
                self.u_home.setText(value)
            elif key == "shell":
                self.u_shell.setText(value)
                dict["shell"] = value
            elif key == "groups":
                self.u_groups.setText(value)
                dict["groups"] = value
        self.editdict = dict

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

import qt

from qt import *
from kdecore import *
from kdeui import *

from um_utility import *

import polkit

import functools

categories = {"tr.org.pardus.comar.user.manager": [I18N_NOOP("User/group operations"), "user"],
        "org.freedesktop.NetworkManager|org.freedesktop.network-manager-settings.system|tr.org.pardus.comar.net.filter|tr.org.pardus.comar.net.share": [I18N_NOOP("Network settings"), "network"],
        "tr.org.pardus.comar.system.manager": [I18N_NOOP("Package operations"), "package"],
        "tr.org.pardus.comar.system.service": [I18N_NOOP("Service operations"), "ksysv"],
        "tr.org.pardus.comar.time": [I18N_NOOP("Date/time operations"), "history"],
        "tr.org.pardus.comar.boot.modules": [I18N_NOOP("Kernel module operations"), "gear"],
        "tr.org.pardus.comar.boot.loader": [I18N_NOOP("Bootloader settings"), "blockdevice"],
        "tr.org.pardus.comar.xorg": [I18N_NOOP("Screen settings"), "randr"]
        }

class UID:
    def __init__(self, stack, w, grid, edit=False):
        self.edit = edit
        self.stack = stack
        self.usedids = []
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
        else:
            self.stack.checkAdd()

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
    def __init__(self, stack, parent, group, updateItem = None):
        self.stack = stack
        QCheckListItem.__init__(self, parent, group.name, self.CheckBox)
        self.name = group.name
        self.gid = group.gid
        self.updateItem = updateItem

    def text(self, col):
        return (self.name, "")[col]

    def stateChange(self, bool):
        self.stack.slotGroup()
        if self.updateItem:
            self.updateItem.setChecked(bool)

class UserGroupList(QWidget):
    def __init__(self, stack, parent):
        QWidget.__init__(self, parent)
        self.stack = stack
        vb = QVBoxLayout(self)
        vb.setSpacing(3)

        self.groups = QListView(self)
        self.groups.addColumn(i18n("Group"))
        self.groups.setResizeMode(QListView.LastColumn)
        vb.addWidget(self.groups, 2)

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
        group = groups.firstChild()
        self.groups.clear()
        while group:
            updateItem = None
            if group.text(1) == "wheel":
                updateItem = self.stack.checkBoxAdmin
            g = UserGroup(self, self.groups, group, updateItem)
            group = group.nextSibling()

    def slotGroup(self):
        groups = []
        mainGroup = None
        item = self.groups.firstChild()
        while item:
            if item.state() == item.On:
                groups.append(item.name)
                if self.stack.editdict and item.gid == self.stack.editdict['gid']:
                    mainGroup = item.name
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
                if mainGroup:
                    self.main_sel = mainGroup
        self.stack.checkAdd()

    def slotMain(self, text):
        self.main_sel = unicode(text)
        self.stack.checkAdd()

    def slotToggle(self, bool):
        group = self.groups.firstChild()
        while group:
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
        if len(groups) > 0:
            item = self.groups.firstChild()
            while item:
                if item.name in groups:
                    item.setState(item.On)
                else:
                    item.setState(item.Off)
                item = item.nextSibling()
            self.main_sel = groups[0]
            self.main_group.setCurrentText(groups[0])

class Guide(QWidget):
    def __init__(self, parent, stack, edit):
        QWidget.__init__(self, parent)
        self.edit = edit
        self.stack = stack
        hb = QHBoxLayout(self)
        hb.setMargin(6)
        hb.setSpacing(6)
        lab = QLabel(self)
        lab.setPixmap(getIconSet("help.png", KIcon.Panel).pixmap(QIconSet.Automatic, QIconSet.Normal))
        hb.addWidget(lab, 1, hb.AlignTop)
        self.info = QLabel(" ", self)
        hb.addWidget(self.info, 5)

    def check(self):
        err = None
        p = self.stack

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
                    err = i18n("Don't use your full name or user name as a password.")

        if not err and p.u_password.text() == None:
            err = i18n("Passwords don't match.")

        if not err:
            if p.u_id.text() == "":
                err = i18n("You must enter a user ID or use the auto selection.")
            elif not p.u_id.text() == "auto":
                uid = int(p.u_id.text())
                if uid < 1000 or uid > 65535:
                    err = i18n("You must enter a user ID between 999 and 65535.")

        nick = p.u_name.text()

        if not err and nick == "":
            err = i18n("You must enter a user name.")

        if not err and nick in p.u_name.usednames:
            err = i18n("This user name is used by another user.")

        if not err and not p.u_id.text() == 'auto' and int(p.u_id.text()) in p.u_id.usedids:
            err = i18n("This user ID is used by another user.")

        if not err:
            if len(nick) > 0 and nick[0] >= "0" and nick[0] <= "9":
                err = i18n("User name must not start with a number.")

        if not err and p.u_groups.text() == "":
            err = i18n("You should select at least one group this user belongs to.")

        def isRealNameDirty():
            if p.u_realname.text() == p.editdict['realname']:
                return False
            return True

        def isShellDirty():
            if p.u_shell.text() == p.editdict['shell']:
                return False
            return True

        def isPasswordDirty():
            if p.u_password.text() == "":
                return False
            return True

        def isGroupsDirty():
            groups = []
            for gr in p.editdict['groups']:
                groups.append(gr)
            # current (changed!) groups
            u_groups = p.u_groups.text().split(',')
            diff_list = list(set(u_groups).symmetric_difference(set(groups)))
            if len(diff_list) == 0:
                return False
            return True

        def isAdminCheckDirty():
            if (p.u_isWheel and not p.checkBoxAdmin.isChecked()) or (not p.u_isWheel and p.checkBoxAdmin.isChecked()):
                return True
            return False

        def isPolicyDirty():
            if len(p.u_operations) == 0:
                return False
            return True

        def isMainGroupDirty():
            if p.editdict['gid'] == p.findGroupID(p.u_policygrouptab.groupsWidget.groups, p.u_policygrouptab.groupsWidget.main_sel):
                return False
            return True

        if err:
            self.info.setText(u"<font color=red>%s</font>" % err)
            self.ok_but.setEnabled(False)
        else:
            self.info.setText("")
            self.ok_but.setEnabled(True)
            if p.edit:
                if isRealNameDirty() or isPasswordDirty() or isShellDirty() or isGroupsDirty() or isAdminCheckDirty() or isPolicyDirty() or isMainGroupDirty():
                    p.setDirty(True)
                else:
                    p.setDirty(False)

        return err

    def op_start(self, msg):
        self.buttons.setEnabled(False)
        self.info.setText(msg)

    def op_end(self, msg=None):
        self.buttons.setEnabled(True)
        if msg:
            self.info.setText(u"<big><font color=red>%s</font></big>" % msg)


class UserStack(QVBox):
    def __init__(self, parent, edit=False):
        QVBox.__init__(self, parent)
        self.setMargin(6)
        self.setSpacing(6)
        self.edit = edit

        self.mainwidget = parent

        w = QWidget(self)
        hb = QHBoxLayout(w)
        hb.setMargin(6)
        if edit:
            lab = QLabel(u"<b><big>%s</big></b>" % i18n("Edit User's Information"), w)
        else:
            lab = QLabel(u"<b><big>%s</big></b>" % i18n("Enter Information For New User"), w)
        hb.addWidget(lab)

        mainhb = QHBox(self)
        self.setStretchFactor(mainhb, 4)
        mainhb.setSpacing(18)

        w = QWidget(mainhb)
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

        self.u_isWheel = False

        self.editdict = None

        line = QFrame(w)
        line.setFrameStyle(QFrame.HLine | QFrame.Sunken)
        row = grid.numRows()
        grid.addMultiCellWidget(line, row, row, 0, 1)

        a_hb = QHBox(w)
        a_hb.setSpacing(8)

        self.checkBoxAdmin = QCheckBox(i18n("Give administrator privileges to this user"), a_hb)
        row = grid.numRows()
        grid.addMultiCellWidget(a_hb, row, row, 0, 1)
        self.checkBoxAdmin.setAutoMask(True)

        self.connect(self.checkBoxAdmin, SIGNAL("toggled(bool)"), self.slotAddAdministrator)

        line = QFrame(w)
        line.setFrameStyle(QFrame.HLine | QFrame.Sunken)
        row = grid.numRows()
        grid.addMultiCellWidget(line, row, row, 0, 1)

        self.u_policygrouptab = PolicyGroupTab(mainhb, self, self.mainwidget, self.u_id, edit)
        self.u_groups = self.u_policygrouptab.groupsWidget
        self.u_operations = self.u_policygrouptab.policytab.operations

        # make PolicyGroupTab longer than the left side of the dialog contains username/password fields
        mainhb.setStretchFactor(w, 3)
        mainhb.setStretchFactor(self.u_policygrouptab, 4)

        self.guide = Guide(w, self, edit)
        self.setStretchFactor(self.guide, 1)
        row = grid.numRows()
        grid.addMultiCellWidget(self.guide, row, row, 0, 1)

        hb = QHBox(self)
        self.guide.buttons = hb
        hb.setSpacing(12)
        QLabel(" ", hb)
        if edit:
            self.applyButton = QPushButton(getIconSet("apply.png", KIcon.Small), i18n("Apply"), hb)
            self.connect(self.applyButton, SIGNAL("clicked()"), self.slotEdit)
            self.applyButton.setEnabled(False)
            self.guide.ok_but = self.applyButton
        else:
            self.addButton = QPushButton(getIconSet("add.png", KIcon.Small), i18n("Add"), hb)
            self.connect(self.addButton, SIGNAL("clicked()"), self.slotAdd)
            self.guide.ok_but = self.addButton
        but = QPushButton(getIconSet("cancel.png", KIcon.Small), i18n("Cancel"), hb)
        self.connect(but, SIGNAL("clicked()"), parent.slotCancel)

    def findGroupID(self, list, name):
        it = list.firstChild()
        while it:
            if it.name == name:
                return it.gid
            it = it.nextSibling()
        return -1

    def setDirty(self, isDirty):
        self.applyButton.setEnabled(isDirty)

    def slotAddAdministrator(self):
        tmpGroups =  self.u_groups.text().split(",")

        if self.checkBoxAdmin.isChecked():
            if not "wheel" in tmpGroups:
                tmpGroups.append(unicode("wheel"))
                self.u_groups.setText(tmpGroups)
        else:
            if "wheel" in tmpGroups:
                tmpGroups.remove(unicode("wheel"))
                self.u_groups.setText(tmpGroups)

    def checkAdd(self):
       return self.guide.check()

    def slotEdit(self):
        if self.checkAdd():
            return

        dict = self.editdict.copy()
        tmp = self.u_realname.text()
        if tmp:
            dict["realname"] = tmp
        tmp = self.u_password.text()
        if tmp:
            dict["password"] = tmp
        tmp = self.u_shell.text()
        if tmp:
            dict["shell"] = tmp
        tmp = self.u_groups.text()
        tmpA = set(tmp.split(","))
        tmpB = set(dict["groups"])

        if tmpA != tmpB:
            if int(dict["uid"]) == os.getuid() and not "wheel" in tmpA and "wheel" in tmpB:
                ret = KMessageBox.warningContinueCancel(
                    self,
                    i18n("You are removing yourself from the 'wheel' system group, you might not use your administrator permissions after that."),
                    i18n("Important Group Change")
                )
                if ret == KMessageBox.Cancel:
                    return
            dict["groups"] = tmp.split(",")
        else:
            dict["groups"] = tmp.split(",")
        if len(dict) > 1:
            self.guide.op_start(i18n("Changing user information..."))

            try:
                # synchronous call 'setuser'
                self.mainwidget.link.User.Manager["baselayout"].setUser(dict["uid"], dict["realname"], "", dict["shell"], dict["password"], dict["groups"])
                self.parent().browse.userModified(int(dict["uid"]), realname=dict["realname"])
            except:
                self.parent().slotCancel()
                return

            for key in self.u_operations.keys():
                value = self.u_operations[key]
                if value == "grant":
                    self.mainwidget.link.User.Manager["baselayout"].grantAuthorization(int(self.u_id.text()), key)
                elif value == "block":
                    self.mainwidget.link.User.Manager["baselayout"].blockAuthorization(int(self.u_id.text()), key)
                else:
                    self.mainwidget.link.User.Manager["baselayout"].revokeAuthorization(int(self.u_id.text()), key)

            self.parent().slotCancel()

    def slotAdd(self):
        if self.checkAdd():
            return

        self.guide.op_start(i18n("Adding user..."))

        def handler(package, exception, args):
            if exception:
                self.parent().slotCancel()
                return
            uid = args[0]
            self.parent().browse.userModified(uid, self.u_name.text(), self.u_realname.text())
            self.parent().slotCancel()

        if self.u_id.text() == "auto":
            uid = -1
        else:
            uid = int (self.u_id.text())

        a_groups = self.u_groups.text()

        if self.checkBoxAdmin.isChecked():
            if not "wheel" in a_groups:
                a_groups = a_groups + ",wheel"

        grants = []
        blocks = []

        for op in self.u_operations.keys():
            if self.u_operations[op] == "grant":
                grants.append(op)
            elif self.u_operations[op] == "block":
                blocks.append(op)

        #dbus does not like empty lists as parameters
        for ls in [grants, blocks]:
            if len(ls) == 0:
                ls.append("")

        self.mainwidget.link.User.Manager["baselayout"].addUser(uid, self.u_name.text(), self.u_realname.text(), self.u_home.text(), self.u_shell.text(), self.u_password.text(), a_groups.split(","), grants, blocks, async=handler)

    def reset(self):
        self.u_id.setText("auto")
        self.u_name.setText("")
        self.u_realname.setText("")
        self.u_password.setText("")
        self.u_home.setText("")
        self.u_groups.setText("")
        self.u_policygrouptab.reset()
        grants = []
        blocks = []
        self.checkAdd()
        self.checkBoxAdmin.setChecked(False)

    def startAdd(self, groups, names, ids):
        self.u_groups.populate(groups)
        self.reset()
        self.u_name.usednames = names
        self.u_id.usedids = ids
        self.u_groups.setText(["users", "pnp", "pnpadmin", "removable", "disk", "audio", "video", "power", "dialout"])
        self.guide.op_end()
        self.u_realname.name.setFocus()

    def startEdit(self, groups, uid):
        self.u_groups.populate(groups)
        self.reset()
        self.editdict = None
        self.guide.op_start(i18n("Getting user information..."))

        def userInfo(package, exception, args):
            if exception:
                return
            nick, name, gid, homedir, shell, groups = args
            dict = {}
            dict["uid"] = uid
            dict["realname"] = name
            dict["shell"] = shell
            dict["groups"] = groups
            dict["password"] = ""
            dict["gid"] = gid
            self.editdict = dict
            self.u_id.setText(str(uid))
            self.u_name.setText(nick)
            self.u_realname.setText(name)
            self.u_home.setText(homedir)
            self.u_shell.setText(shell)
            self.u_groups.setText(groups)
            self.guide.op_end()
            self.applyButton.setEnabled(False)

            if "wheel" in self.u_groups.text():
                self.checkBoxAdmin.setChecked(True)
                self.u_isWheel = True
            else:
                self.u_isWheel = False

        self.mainwidget.link.User.Manager["baselayout"].userInfo(uid, async=userInfo)

class PolicyGroupTab(KTabWidget):
    def __init__(self, parent, stack, mainwidget, uid, edit):
        KTabWidget.__init__(self, parent)

        #add policy tab
        hb = QHBox(self)
        hb.setSpacing(12)
        hb.setMargin(6)
        self.policytab = PolicyTab(hb, mainwidget, stack, uid, edit)
        self.addTab(hb, i18n("Authorizations"))

        #add groups tab
        hb2 = QHBox(self)
        hb2.setSpacing(12)
        hb2.setMargin(6)
        self.groupsWidget = UserGroupList(stack, hb2)
        self.addTab(hb2, i18n("Groups"))

    def reset(self):
        self.policytab.reset()

class PolicyTab(QVBox):
    def __init__(self, parent, mainwidget, stack, uid, edit):
        QVBox.__init__(self, parent)
        self.policyview = KListView(self)
        self.policyview.setRootIsDecorated(True)
        self.policyview.setResizeMode(KListView.LastColumn)
        self.policyview.addColumn(i18n("Actions"))
        self.uid = uid
        self.edit = edit
        self.mainwidget = mainwidget
        self.operations = {}
        self.inOperation = False
        self.stack = stack

        #add radio buttons
        w = QButtonGroup(self)
        w.setFrameShape(QFrame.NoFrame)
        hb = QHBoxLayout(w)
        self.authorized = QRadioButton(i18n("Authorize"), w)
        hb.addStretch(1)
        hb.addWidget(self.authorized)
        hb.addStretch(3)
        self.blocked = QRadioButton(i18n("Block"), w)
        self.connect(self.blocked, SIGNAL("toggled(bool)"), self.blockedSlot)
        hb.addWidget(self.blocked)
        hb.addStretch(1)

        #add checkbox
        w = QWidget(self)
        hb = QHBoxLayout(w)
        hb.addStretch(1)
        lbl = QLabel("   ", w)
        hb.addWidget(lbl)
        self.passwordCheck = QCheckBox(i18n("Do not ask password"), w)
        self.connect(self.authorized, SIGNAL("toggled(bool)"), self.slotAuthorized)
        self.connect(self.passwordCheck, SIGNAL("toggled(bool)"), self.passwordCheckSlot)
        hb.addWidget(self.passwordCheck, 1)
        hb.addStretch(3)

        w = QWidget(self)
        hb = QHBoxLayout(w)
        self.applyAllButton = QPushButton(i18n("Apply this policy to all"), w)
        hb.addWidget(self.applyAllButton)
        self.connect(self.applyAllButton, SIGNAL("clicked()"), self.slotAuthAll)

        self.selectionPopup = QPopupMenu(self)
        self.selectionPopup.insertItem(i18n("Apply this policy to all"), self.slotAuthAll)
        self.selectionPopup.insertItem(i18n("Apply this policy to category"), self.slotAuthAllForCategory)
        self.selectionPopup.insertSeparator(2)
        self.resetID = self.selectionPopup.insertItem(i18n("Reset"), self.slotResetChanges)

        #disable buttons about policy until one of the policies is selected
        self.setPolicyButtonsEnabled(False)

        #put all necessary actions to listview
        #self.fillAuths()

        self.connect(self.policyview, SIGNAL("selectionChanged(QListViewItem *)"), self.listviewClicked)
        self.connect(self.policyview, SIGNAL("expanded(QListViewItem *)"), self.listviewExpanded)
        self.connect(self.policyview, SIGNAL("contextMenuRequested(QListViewItem *, const QPoint &, int)"), self.showPopup)


    def showPopup(self, item, point, column):
        if item.depth() != 1:
            return
        else:
            self.checkResetStatus()
            self.selectionPopup.exec_loop(qt.QCursor.pos())

    def checkResetStatus(self):
        if len(self.operations) > 0:
            self.selectionPopup.setItemEnabled(self.resetID, True)
        else:
            self.selectionPopup.setItemEnabled(self.resetID, False)

    def slotResetChanges(self):
        self.operations.clear()
        self.reset()
        self.stack.checkAdd()

    def slotAuthAllForCategory(self):
        item = self.policyview.selectedItem()
        if not item or item.depth() != 1:
            return

        def categoryAuth(item, package, exception, auths):
            if not auths:
                return
            auths = map(lambda x: {"action_id": str(x[0]), "negative": bool(x[4])}, auths[0])
            storedAuths = {}
            for i in auths:
                storedAuths[i["action_id"]] = i["negative"]
            it = item.parent().firstChild()
            while it:
                if it.id == item.id:
                    it = it.nextSibling()
                    continue
                self.checkItemStatus(it, storedAuths)
                it = it.nextSibling()
            self.stack.checkAdd()

        self.mainwidget.link.User.Manager["baselayout"].listUserAuthorizationsByCategory(int(self.uid.text()), item.parent().name, async=functools.partial(categoryAuth, item))

    def checkItemStatus(self, item, storedAuths):
        icon = "yes"
        if item.id in storedAuths.keys():
            # saved as blocked
            if storedAuths[item.id]:
                if self.authorized.isOn():
                    if self.passwordCheck.isChecked():
                        self.operations[item.id] = "grant"
                    else:
                        self.operations[item.id] = "block_revoke"
                elif self.blocked.isOn():
                    icon = "no"
                    if self.operations.has_key(item.id):
                        self.operations.pop(item.id)
            # negative = False. granted.
            elif not storedAuths[item.id]:
                if self.authorized.isOn():
                    if self.passwordCheck.isChecked():
                        if self.operations.has_key(item.id):
                            self.operations.pop(item.id)
                    else:
                        self.operations[item.id] = "grant_revoke"
                elif self.blocked.isOn():
                    self.operations[item.id] = "block"
                    icon = "no"
        else:
            if self.authorized.isOn() and self.passwordCheck.isChecked():
                self.operations[item.id] = "grant"
            elif self.blocked.isOn():
                self.operations[item.id] = "block"
                icon = "no"
            else:
                if self.operations.has_key(item.id):
                    self.operations.pop(item.id)
        item.setAuthIcon(icon)

    def slotAuthAll(self):
        item = self.policyview.selectedItem()
        if not item:
            return
        def listUserAuthorizations(package, exception, auths):
            if exception:
                return
            auths = map(lambda x: {"action_id": str(x[0]), "negative": bool(x[4])}, auths[0])
            storedAuths = {}
            for i in auths:
                storedAuths[i["action_id"]] = i["negative"]
            it = QListViewItemIterator(self.policyview)
            item = it.current()
            while item:
                if item.depth() == 1:
                    self.checkItemStatus(item, storedAuths)
                it += 1
                item = it.current()
            self.stack.checkAdd()

        self.mainwidget.link.User.Manager["baselayout"].listUserAuthorizations(int(self.uid.text()), async=listUserAuthorizations)

    def reset(self):
        it = self.policyview.firstChild()
        while it:
            it.setOpen(False)
            it = it.nextSibling()
        self.setPolicyButtonsEnabled(False)
        self.policyview.clearSelection()
        self.passwordCheck.setChecked(False)
        self.authorized.setChecked(False)
        self.blocked.setChecked(False)
        self.operations.clear()
        self.inOperation = False

    def fillAuths(self):
        #do not show policies require policy type yes or no, only the ones require auth_* type
        allActions = filter(lambda x: polkit.action_info(x)['policy_active'].startswith("auth_"),polkit.action_list())

        for cats in categories:
            catitem = CategoryItem(self.policyview, i18n(categories[cats][0]), cats)
            catitem.setPixmap(0, getIcon(categories[cats][1]))
            cats = cats.split('|')
            for category in cats:
                catactions = filter(lambda x: x.startswith(category), allActions)
                for cataction in catactions:
                    actioninfo = polkit.action_info(cataction)
                    actionitem = ActionItem(catitem, cataction, unicode(actioninfo['description']), actioninfo['policy_active'])

    def setPolicyButtonsEnabled(self, enable):
        self.authorized.setEnabled(enable)
        self.blocked.setEnabled(enable)
        self.applyAllButton.setEnabled(enable)
        if enable and self.blocked.isOn():
            self.passwordCheck.setEnabled(False)
        elif enable and self.authorized.isOn():
            self.passwordCheck.setEnabled(True)
        else:
            self.passwordCheck.setEnabled(False)

    def listviewClicked(self, item):
        if not item:
            return
        if item.depth() != 1:
            self.setPolicyButtonsEnabled(False)
        else:
            self.setPolicyButtonsEnabled(True)
            self.actionClicked(item)

    def checkNegativeAndCall(self, item, method):
        def checkNegative(method, package, exception, negative):
            if exception:
                return
            method(item, negative[0])
            self.stack.checkAdd()
        self.mainwidget.link.User.Manager["baselayout"].getNegativeValue(int(self.uid.text()), item.id, async=functools.partial(checkNegative, method))

    def passwordCheckSlot(self, toggle):
        if self.inOperation:
            return

        item = self.policyview.selectedItem()
        if not item or item.depth() != 1:
            return

        if toggle:
            self.checkNegativeAndCall(item, self.passwordCheckChecked)
        else:
            self.checkNegativeAndCall(item, self.passwordCheckUnchecked)

    def passwordCheckChecked(self, item, negative):
        if negative != -1: # registered to policykit
            if negative == 0: # blocked
                self.operations[item.id] = "grant"
            else: # grant
                if item.id in self.operations.keys():
                    self.operations.pop(item.id)
        else: # not registered
            self.operations[item.id] = "grant"

    def passwordCheckUnchecked(self, item, negative):
        if negative != -1: # registered to policykit
            if negative == 0: # blocked
                self.operations[item.id] = "block_revoke"
            else: # grant
                self.operations[item.id] = "grant_revoke"
        else: # not registered
            if item.id in self.operations.keys():
                self.operations.pop(item.id)

    def blockedSlot(self, toggle):
        if self.inOperation:
            return
        item = self.policyview.selectedItem()
        if not item or item.depth() != 1:
            return

        if toggle:
            item.setAuthIcon("no")
            self.checkNegativeAndCall(item, self.doBlock)

    def doBlock(self, item, negative):
        if negative != -1: # registered to policykit
            if negative == 0: # blocked
                if item.id in self.operations.keys():
                    self.operations.pop(item.id)
            else: # granted
                self.operations[item.id] = "block"
        else:
            self.operations[item.id] = "block"

    def slotAuthorized(self, toggle):
        if self.inOperation:
            return
        item = self.policyview.selectedItem()
        if not item or item.depth() != 1:
            return
        self.passwordCheck.setEnabled(toggle)

        if toggle:
            item.setAuthIcon("yes")
            self.checkNegativeAndCall(item, self.doAuthorize)

    def doAuthorize(self, item, negative):
        if negative != -1: # registered to policykit
            if negative == 0: # blocked
                if self.authorized.isOn() and self.passwordCheck.isChecked():
                    self.operations[item.id] = "grant"
                else:
                    self.operations[item.id] = "block_revoke"
            else: # granted
                if self.authorized.isOn() and self.passwordCheck.isChecked():
                    if item.id in self.operations.keys():
                        self.operations.pop(item.id)
                else:
                    self.operations[item.id] = "grant_revoke"
        else: # not registered
            if self.authorized.isOn() and self.passwordCheck.isChecked():
                self.operations[item.id] = "grant"
            else:
                if item.id in self.operations.keys():
                    self.operations.pop(item.id)

    def listviewExpanded(self, item):
        if not item: # or self.policyview.selectedItem()
            return

        # get list of children items
        childCount = item.childCount()
        if childCount < 1:
            return

        children = []
        newItem = item.firstChild()
        while newItem:
            children.append(newItem)
            newItem = newItem.nextSibling()

        def setIcons(auths):
            blocks = map(lambda x: x["action_id"], filter(lambda x: x["negative"], auths))

            if self.operations:
                # add selections done via user-manager
                for op in self.operations:
                    if op in blocks:
                        blocks.remove(op)
                blocks.extend(filter(lambda x: self.operations[x] == "block", self.operations.keys()))
                blocks = list(set(blocks))

            for child in children:
                if child.id in blocks:
                    child.setAuthIcon("no")
                else:
                    child.setAuthIcon("yes")

        def listUserAuthorizations(package, exception, auths):
            if exception:
                item.setOpen(False)
                return
            auths = map(lambda x: {"action_id": str(x[0]), "negative": bool(x[4])}, auths[0])
            setIcons(auths)

        if not self.edit:
            setIcons([])
            return

        self.mainwidget.link.User.Manager["baselayout"].listUserAuthorizations(int(self.uid.text()), async=listUserAuthorizations)


    def actionClicked(self, actionItem):
        #now we will setup radiobuttons and checkbox according to the action clicked, but during this setup
        #slots of the widgets should not be executed so we set this inOperation variable and check this variable in slots of the widgets
        self.inOperation = True

        #if user changed the default value select buttons according to it
        if actionItem.id in self.operations.keys():
            pol =  self.operations[actionItem.id]
            if pol == "grant":
                self.authorized.setOn(True)
                self.passwordCheck.setChecked(True)
            elif pol.endswith("revoke"):
                self.authorized.setOn(True)
                self.passwordCheck.setChecked(False)
            else: #block
                self.blocked.setOn(True)
                self.passwordCheck.setChecked(False)

            self.inOperation = False
            return

        # if it is a new user, default is authorized
        if not self.edit:
            self.authorized.setOn(True)
            self.passwordCheck.setChecked(False)
            self.inOperation = False
            return

        def listUserAuthorizations(package, exception, authList):
            #since COMAR calls this handler twice, we have a workaround like this
            if exception:
                self.setPolicyButtonsEnabled(False)
                return

            self.inOperation = True

            # convert comar answer to pypolkit call structure
            authList = map(lambda x: {"action_id": str(x[0]), "negative": bool(x[4])}, authList[0])
            self.selectRightButtons(authList, actionItem)

        #try:
        #    auths = polkit.auth_list_uid(int(self.uid.text()))
        #    self.inOperation = True
        #    self.selectRightButtons(auths, actionItem)
        #except:
        #call COMAR see different users' auths

        self.mainwidget.link.User.Manager["baselayout"].listUserAuthorizations(int(self.uid.text()), async=listUserAuthorizations)


    def selectRightButtons(self, auths, actionItem):
        auths = filter(lambda x: x['action_id'] == actionItem.id, auths)

        if len(auths) == 0:
            self.authorized.setOn(True)
            self.passwordCheck.setEnabled(True)
            self.passwordCheck.setChecked(False)

            self.inOperation = False
            return

        if len(filter(lambda x: x['negative'], auths)) > 0:
            #if action is blocked
            self.blocked.setOn(True)
            self.passwordCheck.setEnabled(False)
            self.passwordCheck.setChecked(False)
        else:
            self.authorized.setOn(True)
            self.passwordCheck.setEnabled(True)
            self.passwordCheck.setChecked(True)

        self.inOperation = False

class CategoryItem(KListViewItem):
    def __init__(self, parent, label, name):
        KListViewItem.__init__(self, parent, label)
        self.name = name

class ActionItem(KListViewItem):
    def __init__(self, parent, id, desc, policy):
        KListViewItem.__init__(self, parent, desc)
        self.id = id
        self.desc = desc
        self.policy = policy

        # icon mappings
        self.states = {"yes": "ok", "no": "cancel", "n/a": "history"}
        self.setAuthIcon("n/a")

    def setAuthIcon(self, state):
        self.setPixmap(0, getIcon(self.states[state]))


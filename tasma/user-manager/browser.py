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

from utility import getIconSet


class UserItem(QListViewItem):
    def __init__(self, parent, line):
        QListViewItem.__init__(self, parent)
        self.uid, self.nick, self.name = line.split("\t")
        self.uid = int(self.uid)
    
    def text(self, col):
        return (str(self.uid), self.nick, self.name)[col]
    
    def compare(self, item, col, ascend):
        if col == 0:
            if self.uid < item.uid:
                return -1
            elif self.uid == item.uid:
                return 0
            else:
                return 1
        else:
            return QListViewItem.compare(self, item, col, ascend)


class GroupItem(QListViewItem):
    def __init__(self, parent, line):
        QListViewItem.__init__(self, parent)
        args = line.split("\t")
        self.gid = int(args[0])
        self.name = args[1]
        self.comment = ""
        self.desc = ""
        if len(args) > 2:
            self.comment = args[2]
            self.desc = args[3]
    
    def text(self, col):
        return (str(self.gid), self.name)[col]
    
    def compare(self, item, col, ascend):
        if col == 0:
            if self.gid < item.gid:
                return -1
            elif self.gid == item.gid:
                return 0
            else:
                return 1
        else:
            return QListViewItem.compare(self, item, col, ascend)


class BrowseStack(QVBox):
    def __init__(self, parent, link):
        QWidget.__init__(self, parent)
        self.setMargin(6)
        self.setSpacing(6)
        
        bar = QToolBar("lala", None, self)
        but = QToolButton(getIconSet("add.png"), i18n("Add"), "lala", parent.slotAdd, bar)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)
        bar.addSeparator()
        but = QToolButton(getIconSet("configure.png"), i18n("Edit"), "lala", parent.slotEdit, bar)
        self.edit_but = but
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)
        bar.addSeparator()
        but = QToolButton(getIconSet("remove.png"), i18n("Delete"), "lala", self.slotDelete, bar)
        self.delete_but = but
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)
        
        lab = QLabel("", bar)
        bar.setStretchableWidget(lab)
        
        toggle = QCheckBox(i18n("Show system user and groups"), bar)
        self.connect(toggle, SIGNAL("toggled(bool)"), self.slotToggle)
        
        tab = QTabWidget(self)
        self.connect(tab, SIGNAL("currentChanged(QWidget*)"), self.slotTabChanged)
        self.tab = tab
        tab.setMargin(6)
        
        self.users = QListView(tab)
        self.users.addColumn(i18n("ID"))
        self.users.setColumnAlignment(0, Qt.AlignRight)
        self.users.addColumn(i18n("User name"))
        self.users.addColumn(i18n("Full name"))
        self.users.setResizeMode(QListView.LastColumn)
        self.users.setAllColumnsShowFocus(True)
        self.connect(self.users, SIGNAL("selectionChanged()"), self.slotSelect)
        self.connect(self.users, SIGNAL("doubleClicked(QListViewItem *, const QPoint &, int)"), self.slotDouble)
        
        self.groups = QListView(tab)
        self.groups.addColumn(i18n("ID"))
        self.groups.setColumnAlignment(0, Qt.AlignRight)
        self.groups.addColumn(i18n("Group name"))
        self.groups.setResizeMode(QListView.LastColumn)
        self.groups.setAllColumnsShowFocus(True)
        self.connect(self.groups, SIGNAL("selectionChanged()"), self.slotSelect)
        
        tab.addTab(self.users, getIconSet("personal.png", KIcon.Small), i18n("Users"))
        tab.addTab(self.groups, getIconSet("kuser.png", KIcon.Small), i18n("Groups"))
        
        self.link = link
        link.call("User.Manager.userList", id=1)
        link.call("User.Manager.groupList", id=2)
        
        self.slotSelect()
    
    def slotDelete(self):
        if self.tab.currentPageIndex() == 0:
            item = self.users.selectedItem()
            if item:
                msg = unicode(i18n("<big><b>Should I delete this user?</b></big><br><br>Name: %s<br>User name: %s<br>ID: %d")) % (
                    item.name, item.nick, item.uid
                )
                ret = KMessageBox.warningYesNoCancel(
                    self,
                    msg,
                    i18n("Delete User"),
                    KGuiItem(i18n("Delete user and files"), "trashcan_empty"),
                    KGuiItem(i18n("Delete user"), "remove"),
                )
                if ret == KMessageBox.Yes:
                    self.link.call("User.Manager.deleteUser", [ "uid", str(item.uid), "deletefiles", "true" ])
                    self.userModified(item.uid)
                if ret == KMessageBox.No:
                    self.link.call("User.Manager.deleteUser", [ "uid", str(item.uid) ])
                    self.userModified(item.uid)
        else:
            item = self.groups.selectedItem()
            if item:
                msg = unicode(i18n("<big><b>Should I delete this group?</b></big><br><br>Group name: %s<br>ID: %d")) % (
                    item.name, item.gid
                )
                if KMessageBox.Yes == KMessageBox.warningYesNo(
                    self,
                    msg,
                    i18n("Delete Group"),
                    KGuiItem(i18n("Delete Group"), "remove"),
                    KStdGuiItem.cancel()
                ):
                    self.link.call("User.Manager.deleteGroup", [ "gid", str(item.gid) ])
                    self.groupModified(item.gid)
    
    def slotSelect(self):
        bool = False
        bool2 = False
        if self.tab.currentPageIndex() == 0:
            item = self.users.selectedItem()
            if item:
                bool = True
                bool2 = True
                # You shouldn't delete your user while logged in :)
                if item.uid == 0 or item.uid == os.getuid():
                    bool2 = False
        else:
            if self.groups.selectedItem():
                bool2 = True
        self.edit_but.setEnabled(bool)
        self.delete_but.setEnabled(bool2)
    
    def slotDouble(self, item, point, col):
        self.parent().slotEdit()
    
    def slotTabChanged(self, w):
        self.slotSelect()
    
    def slotToggle(self, on):
        item = self.users.firstChild()
        while item:
            if item.uid < 1000 or item.uid > 65000:
                item.setVisible(on)
            item = item.nextSibling()
        item = self.groups.firstChild()
        while item:
            if item.gid < 1000 or item.gid > 65000:
                item.setVisible(on)
            item = item.nextSibling()
        self.slotSelect()
    
    def comarUsers(self, reply):
        if reply[0] != self.link.RESULT:
            return
        for user in unicode(reply[2]).split("\n"):
            item = UserItem(self.users, user)
            if item.uid < 1000 or item.uid > 65000:
                item.setVisible(False)
    
    def comarGroups(self, reply):
        if reply[0] != self.link.RESULT:
            return
        for group in unicode(reply[2]).split("\n"):
            item = GroupItem(self.groups, group)
            if item.gid < 1000 or item.gid > 65000:
                item.setVisible(False)
    
    def userModified(self, uid, name=None, realname=None):
        if name:
            UserItem(self.users, "%d\t%s\t%s" % (uid, name, realname))
        else:
            item = self.users.firstChild()
            while item:
                if item.uid == uid:
                    if realname:
                        item.name = realname
                        item.repaint()
                    else:
                        self.users.takeItem(item)
                    return
                item = item.nextSibling()
    
    def groupModified(self, gid, name=None):
        if name:
            GroupItem(self.groups, "%d\t%s" % (gid, name))
        else:
            item = self.groups.firstChild()
            while item:
                if item.gid == gid:
                    self.groups.takeItem(item)
                    return
                item = item.nextSibling()

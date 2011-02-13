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
from utility import HelpDialog

class UserItem(QListViewItem):
    def __init__(self, parent, uid, nick, name):
        QListViewItem.__init__(self, parent)
        self.uid = uid
        self.nick = nick
        self.name = name
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
    def __init__(self, parent, gid, name):
        QListViewItem.__init__(self, parent)
        self.gid = gid
        self.name = name
    
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
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setMargin(6)
        self.setSpacing(6)
        
        self.mainwidget = parent
        
        bar = QToolBar("lala", None, self)
        but = QToolButton(getIconSet("add.png"), i18n("Add"), "lala", parent.slotAdd, bar)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)
        self.new_but = but
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
        bar.addSeparator()
        but = QToolButton(getIconSet("help.png"), i18n("Help"), "lala", self.slotHelp, bar)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)
        
        toggle = QCheckBox(i18n("Show system user and groups"), bar)
        toggle.setAutoMask(True)
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
        
        self.mainwidget.link.User.Manager["baselayout"].userList(async=self.comarUsers)
        self.mainwidget.link.User.Manager["baselayout"].groupList(async=self.comarGroups)
        
        self.showControls()
        
        self.slotSelect()
    
    def slotHelp(self):
        help = HelpDialog("user-manager", i18n("User Manager Help"), self)
        help.show()
    
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
                def handler(package, exception, args):
                    if exception:
                        return
                    self.userModified(item.uid)
                if ret == KMessageBox.Yes or ret == KMessageBox.No:
                    self.mainwidget.link.User.Manager["baselayout"].deleteUser(item.uid, ret == KMessageBox.Yes, async=handler)
                elif ret == KMessageBox.Cancel:
                    pass
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
                    def handler(package, exception, args):
                        if exception:
                            return
                        self.groupModified(item.gid)
                    self.mainwidget.link.User.Manager["baselayout"].deleteGroup(item.gid, async=handler)
    
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
    
    def comarUsers(self, package, exception, args):
        if exception:
            return
        users = args[0]
        for uid, nick, name in users:
            item = UserItem(self.users, uid, nick, name)
            if uid < 1000 or uid > 65000:
                item.setVisible(False)
    
    def comarGroups(self, package, exception, args):
        if exception:
            return
        groups = args[0]
        for gid, name in groups:
            item = GroupItem(self.groups, gid, name)
            if gid < 1000 or gid > 65000:
                item.setVisible(False)
    
    def userModified(self, uid, name=None, realname=None):
        if name:
            UserItem(self.users, uid, name, realname)
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
            GroupItem(self.groups, gid, name)
        else:
            item = self.groups.firstChild()
            while item:
                if item.gid == gid:
                    self.groups.takeItem(item)
                    return
                item = item.nextSibling()
    
    def hideControls(self):
        self.new_but.setEnabled(False)
        self.edit_but.setEnabled(False)
        self.delete_but.setEnabled(False)
    
    def showControls(self):
        self.new_but.setEnabled(True)
        self.edit_but.setEnabled(True)
        self.delete_but.setEnabled(True)

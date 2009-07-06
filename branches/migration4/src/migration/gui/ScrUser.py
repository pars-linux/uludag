#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyKDE4.kdecore import i18n
from PyKDE4.kdeui import KIcon

from migration.gui.ui.usersItemWidget import Ui_usersItemWidget
from migration.gui.ui.usersWidget import Ui_usersWidget
from migration.gui.ScreenWidget import ScreenWidget

from migration.utils import partition
from migration.utils import info
import migration.gui.context as ctx

class UserItemWidget(QtGui.QWidget, Ui_usersItemWidget):

    def __init__(self, parent, name, partition, icon):
        QtGui.QWidget.__init__(self, parent)

        self.setupUi(self)

        self.userName.setText( name )
        self.partition.setText( partition )
        self.labelIcon.setPixmap(icon.pixmap(32, 32))
        self.data = None

        self.connect(self.checkState, SIGNAL("stateChanged(int)"), self.slotUserCheck)

    def slotUserCheck(self):
        print "ctx.user=%s" % self.getData()[2]
        ctx.user = self.getData()

    def setData(self, data):
        self.data = data

    def getData(self):
        return self.data

class UserItemList(QtGui.QListWidgetItem):
    def __init__(self, parent, widget):
        QtGui.QListWidgetItem.__init__(self, parent)
        self.widget = widget
        self.setSizeHint(QSize(300,48))

class Widget(QtGui.QWidget, ScreenWidget):
    screenSettings = {}
    screenSettings["hasChanged"] = False

    title = i18n("Selecting User")
    desc = i18n("User Profiles")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_usersWidget()
        self.ui.setupUi(self)

        self.addUsers()

        self.connect(self.ui.listUsers, SIGNAL("itemSelectionChanged()"), self.setUser)


    def addUsers(self):
        "Searches old users and adds them to UserListViewWidget"
        self.users = partition.allUsers()
        print "len(users)=%d" % len(self.users)
        icon = KIcon("tux")
        for user in self.users:
            part, parttype, username, userdir = user
            if parttype == "Windows XP":
                widget = UserItemWidget(self.ui.listUsers, unicode(username), unicode(part), icon)
            elif parttype =="Windows Vista":
                widget = UserItemWidget(self.ui.listUsers, unicode(username), unicode(part), icon)

            widget.setData(user)

            widgetItem = UserItemList(self.ui.listUsers, widget)
            self.ui.listUsers.setItemWidget(widgetItem, widget)


    def setUser(self):
        self.screenSettings["selectedUser"] = self.ui.listUsers.currentItem().statusTip()
        self.screenSettings["hasChanged"] = True

    def shown(self):
        pass

    def execute(self):
        user = ctx.user
        part, ostype, username, userdir = user
        sources = {"Partition":part, "OS Type":ostype, "User Name":username, "Home Path":userdir}
        ctx.sources = info.userInfo(sources)
        ctx.destinations = info.localInfo()
        return True


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
from PyKDE4.kdecore import ki18n

from migration.gui.ui.usersItemWidget import Ui_usersItemWidget
from migration.gui.ui.usersWidget import Ui_usersWidget
from migration.gui.ScreenWidget import ScreenWidget
from migration.gui.ui.welcomeWidget import Ui_welcomeWidget

from migration.utils import partition

class UserListItemWidget(QtGui.QWidget, Ui_usersWidget):

    def __init__(self, name, partition, icon, parent):
        QtGui.QWidget.__init__(self, parent)

        self.setupUi(self)

        self.userName.setText( name )
        self.part.setText( partition )
        self.partIcon.setPixmap(icon.pixmap(32, 32))
        

class Widget(QtGui.QWidget, ScreenWidget):
    screenSettings = {}
    screenSettings["hasChanged"] = False
    
    title = ki18n("User")
    desc = ki18n("User Profiles")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_welcomeWidget()
        self.ui.setupUi(self)
        
        item = QtGui.QListWidgetItem(self.ui.listUsers)    
        self.addUsers(item)
        item.setSizeHint(QSize(38,110))
        
        self.ui.listUsers.connect(self.ui.listWallpaper, SIGNAL("itemSelectionChanged()"), self.setUser)
    

    def addUsers(self, item):
        "Searches old users and adds them to UserListViewWidget"
        self.users = partition.allUsers()
        icon = kdeui.KIcon("tux")
        for user in self.users:
            part, parttype, username, userdir = user
            if parttype == "Windows XP":
                widget = UserListItemWidget(unicode(username), unicode(part), icon, self.ui.listUsers)
            elif parttype =="Windows Vista":
                widget = UserListItemWidget(unicode(username), unicode(part), icon, self.ui.listUsers)
            
            self.ui.listUsers.setItemWidget(item, widget)
            item.setStatusTip(user)
            
    def setUser(self):
        self.screenSettings["selectedUser"] = self.ui.listUsers.currentItem().statusTip()
        self.screenSettings["hasChanged"] = True
    
    def shown(self):
        pass

    def execute(self):
        return True
    

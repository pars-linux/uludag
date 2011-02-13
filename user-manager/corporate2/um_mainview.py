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

import sys
import time
from qt import *
from kdecore import *
from kdeui import *

import browser
import useredit
import groupedit
from utility import *

import comar
import dbus

class UserManager(QWidgetStack):
    def __init__(self, parent):
        QWidgetStack.__init__(self, parent)

        self.link = comar.Link()
        self.link.setLocale()

        self.browse = browser.BrowseStack(self)
        self.user = useredit.UserStack(self)
        self.useredit = useredit.UserStack(self, edit=True)
        self.group = groupedit.GroupStack(self)

    def slotCancel(self):
        self.raiseWidget(self.browse)

    def slotAdd(self):
        if self.browse.tab.currentPageIndex() == 0:
            names = []
            ids = []
            item = self.browse.users.firstChild()
            while item:
                names.append(item.nick)
                ids.append(item.uid)
                item = item.nextSibling()
            self.raiseWidget(self.user)
            self.user.startAdd(self.browse.groups, names, ids)
        else:
            self.raiseWidget(self.group)
            self.group.startAdd()

    def slotEdit(self):
        if self.browse.users.selectedItem():
            self.raiseWidget(self.useredit)
            self.useredit.startEdit(self.browse.groups, self.browse.users.selectedItem().uid)

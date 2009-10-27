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

import comar
from qt import *

import browser
import useredit
import groupedit
from utility import *


class UserManager(QWidgetStack):
    def __init__(self, parent):
        link = comar.Link()
        link.localize(languageCode())
        self.link = link
        self.notifier = QSocketNotifier(link.sock.fileno(), QSocketNotifier.Read)
        self.connect(self.notifier, SIGNAL("activated(int)"), self.slotComar)
        
        QWidgetStack.__init__(self, parent)
        self.browse = browser.BrowseStack(self, link)
        self.user = useredit.UserStack(self, link)
        self.useredit = useredit.UserStack(self, link, edit=True)
        self.group = groupedit.GroupStack(self, link)
    
    def slotComar(self, sock):
        reply = self.link.read_cmd()
        id = reply[1]
        if id == 1:
            self.browse.comarUsers(reply)
        elif id == 2:
            self.browse.comarGroups(reply)
        elif id == 3:
            self.user.slotAddReply(reply)
        elif id == 4:
            self.group.slotAddReply(reply)
        elif id == 5:
            self.useredit.slotInfo(reply)
        elif id == 6:
            self.useredit.slotEditReply(reply)
    
    def slotCancel(self):
        self.raiseWidget(self.browse)
    
    def slotAdd(self):
        if self.browse.tab.currentPageIndex() == 0:
            names = []
            item = self.browse.users.firstChild()
            while item:
                names.append(item.nick)
                item = item.nextSibling()
            self.raiseWidget(self.user)
            self.user.startAdd(self.browse.groups, names)
        else:
            self.raiseWidget(self.group)
            self.group.startAdd()
    
    def slotEdit(self):
        self.raiseWidget(self.useredit)
        self.useredit.startEdit(self.browse.groups, self.browse.users.selectedItem().uid)

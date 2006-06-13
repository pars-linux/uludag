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


class UserManager(QWidgetStack):
    def __init__(self, parent):
        link = comar.Link()
        self.link = link
        self.notifier = QSocketNotifier(link.sock.fileno(), QSocketNotifier.Read)
        self.connect(self.notifier, SIGNAL("activated(int)"), self.slotComar)
        
        QWidgetStack.__init__(self, parent)
        self.browse = browser.BrowseStack(self, link)
        self.user = useredit.UserStack(self, link)
        self.group = groupedit.GroupStack(self, link)
    
    def slotComar(self, sock):
        reply = self.link.read_cmd()
        if reply[1] == 1:
            self.browse.comarUsers(reply)
        elif reply[1] == 2:
            self.browse.comarGroups(reply)
    
    def slotCancel(self):
        self.raiseWidget(self.browse)
    
    def slotAdd(self):
        if self.browse.tab.currentPageIndex() == 0:
            self.raiseWidget(self.user)
            self.user.startAdd(self.browse.groups)
        else:
            self.raiseWidget(self.group)
    
    def slotEdit(self):
        pass

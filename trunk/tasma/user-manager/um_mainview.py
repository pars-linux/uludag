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
from handler import CallHandler

import dbus

class UserManager(QWidgetStack):
    def __init__(self, parent):
        QWidgetStack.__init__(self, parent)

        if not self.setupBusses():
            sys.exit(1)

        self.browse = browser.BrowseStack(self)
        self.user = useredit.UserStack(self)
        self.useredit = useredit.UserStack(self, edit=True)
        self.group = groupedit.GroupStack(self)

    def setupBusses(self):
        try:
            self.busSys = dbus.SystemBus()
            self.busSes = dbus.SessionBus()
        except dbus.DBusException:
            KMessageBox.error(self, i18n("Unable to connect to DBus."), i18n("DBus Error"))
            return False
        return True

    def callMethod(self, method, action, async = True, handleCancel = True):
        ch = CallHandler("baselayout", "User.Manager", method,
                         action,
                         self.winId(), async, self.busSys, self.busSes)
        ch.registerError(self.comarError)
        ch.registerAuthError(self.comarError)
        ch.registerDBusError(self.busError)
        if handleCancel:
            ch.registerCancel(self.cancelError)
        return ch

    def cancelError(self):
        message = i18n("You are not authorized for this operation.")
        KMessageBox.sorry(self, message, i18n("Error"))

    def busError(self, exception):
        KMessageBox.error(self, str(exception), i18n("DBus Error"))
        self.setupBusses()

    def comarError(self, exception):
        if "Access denied" in exception.message:
            message = i18n("You are not authorized for this operation.")
            KMessageBox.sorry(self, message, i18n("Error"))
        else:
            KMessageBox.error(self, str(exception), i18n("COMAR Error"))

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

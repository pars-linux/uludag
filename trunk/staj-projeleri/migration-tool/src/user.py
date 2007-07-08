#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

import user_ui

import partition

class UserWidget(user_ui.UserWid):
    def __init__(self, parent):
        self.parent = parent
        user_ui.UserWid.__init__(self, parent)
        self.users = partition.allUsers()
        for user in self.users:
            part, parttype, username, userdir = user
            self.usersBox.insertItem("%s - %s (%s)" % (username, parttype, part))
        if len(self.users) > 0:
            self.parent.setNextEnabled(self, True)
        else:
            self.parent.setNextEnabled(self, False)

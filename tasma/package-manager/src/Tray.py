#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

import sys

from qt import *
from kdeui import *
from kdecore import *

from BalloonMessage import *

class Tray(KSystemTray):
    def __init__(self, parent=None):
        KSystemTray.__init__(self, parent)
        self.parent = parent
        icon = KGlobal.iconLoader().loadIcon("pisi-kga", KIcon.Desktop, 24)
        self.setPixmap(icon)

    def showPopup(self, updates):
        icon = KGlobal.iconLoader().loadIcon("package-manager", KIcon.Desktop, 48)
        message = i18n("There are <b>%1</b> updates available!").arg(len(updates))
        self.popup = BalloonMessage(self, icon, message)
        pos = self.mapToGlobal(self.pos())
        self.popup.setAnchor(pos)
        self.popup.show()

#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# PyKDE4 Stuff
from PyKDE4.kdeui import *
from PyKDE4.kdecore import KGlobal

# Network Manager
from networkmanager.base import MainManager

class NetworkManager(KMainWindow):
    def __init__ (self, app):
        KMainWindow.__init__(self)

        # This is very important for translations when running as kcm_module
        KGlobal.locale().insertCatalog("network-manager")

        self.resize (640, 480)
        self.setCentralWidget(MainManager(self, True, app))


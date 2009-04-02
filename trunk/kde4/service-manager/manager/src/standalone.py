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

# Service Manager
from base import MainManager

class ServiceManager(KMainWindow):
    def __init__ (self, *args):
        KMainWindow.__init__(self)

        self.resize (640, 480)
        self.setCentralWidget(MainManager(self))


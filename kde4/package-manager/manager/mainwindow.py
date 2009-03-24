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

from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

from mainwidget import MainWidget

class MainWindow(KMainWindow):
    def __init__(self, parent=None):
        KMainWindow.__init__(self, parent)
        self.setCentralWidget(MainWidget(self))
        self.setCaption(i18n("Package Manager"))
        self.resize(640, 480)


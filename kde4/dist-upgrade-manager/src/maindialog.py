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

from PyQt4 import QtGui
from PyQt4.QtCore import *

from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

from ui_maindialog import Ui_MainDialog

class MainDialog(QtGui.QDialog, Ui_MainDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowIcon(KIcon(":/data/package-manager.png"))

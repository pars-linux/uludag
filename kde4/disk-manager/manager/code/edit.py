#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# PyQt
from PyQt4 import QtCore
from PyQt4 import QtGui

# PyKDE
from PyKDE4 import kdeui
from PyKDE4 import kdecore

# UI
from ui_edit import Ui_EditWidget


class EditWidget(QtGui.QWidget, Ui_EditWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

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

# Qt Stuff
from PyQt4 import QtGui
from PyQt4.QtCore import *

# Application Stuff
from ui import Ui_mainManager
from uiitem import Ui_ConnectionItemWidget
import time

class ConnectionItem(QtGui.QListWidgetItem):

    def __init__(self, package, parent):
        QtGui.QListWidgetItem.__init__(self, parent)

        self.package = package

class ConnectionItemWidget(QtGui.QWidget):

    def __init__(self, package, parent, item):
        QtGui.QWidget.__init__(self, None)

        self.ui = Ui_ConnectionItemWidget()
        self.ui.setupUi(self)

        self.ui.labelName.setText(package)

        self.iface = parent.iface
        self.item = item
        self.package = package
        self.desc = None

        self.connect(self.ui.buttonEdit,   SIGNAL("clicked()"), parent.editConnection)
        self.connect(self.ui.buttonDelete, SIGNAL("clicked()"), parent.deleteConnection)


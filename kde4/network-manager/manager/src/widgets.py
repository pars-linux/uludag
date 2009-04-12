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

# KDE Stuff
from PyKDE4.kdeui import KIcon

# Application Stuff
from ui import Ui_mainManager
from uiitem import Ui_ConnectionItemWidget
import time

iconForPackage = {"net_tools":"network-wired",
                  "wireless_tools":"network-wireless"}

class ConnectionItemWidget(QtGui.QWidget):

    def __init__(self, package, profile, parent, item):
        QtGui.QWidget.__init__(self, parent)

        self.ui = Ui_ConnectionItemWidget()
        self.ui.setupUi(self)

        self.ui.labelName.setText(profile)

        self.iface = parent.iface
        self.item = item
        self.package = package
        self.profile = profile
        self.desc = None

        self.connect(self.ui.buttonEdit,   SIGNAL("clicked()"), parent.editConnection)
        self.connect(self.ui.buttonDelete, SIGNAL("clicked()"), parent.deleteConnection)
        self.connect(self.ui.checkToggler, SIGNAL("clicked()"), self.toggleConnection)

    def mouseDoubleClickEvent(self, event):
        self.ui.buttonEdit.animateClick(100)

    def update(self, data):
        if type(data) == list:
            name, state, detail = data
        elif type(data) == str:
            splitted = data.split(' ',1)
            state = splitted[0]
            detail = ""
            if len(splitted) > 1:
                detail = splitted[1]
        if state == "down":
            self.ui.labelDesc.setText("Disconnected")
            self.ui.checkToggler.setChecked(False)
            self.ui.labelStatus.setPixmap(KIcon(iconForPackage[self.package]).pixmap(32))
        elif state == "up":
            self.ui.labelDesc.setText("Connected %s" % detail)
            self.ui.checkToggler.setChecked(True)
            self.ui.labelStatus.setPixmap(KIcon("games-endturn").pixmap(32))
        elif state == "connecting":
            self.ui.labelDesc.setText("Connecting")
            self.ui.labelStatus.setPixmap(KIcon("chronometer").pixmap(32))
        elif state == "inaccessible":
            self.ui.labelDesc.setText(detail)
            self.ui.checkToggler.setChecked(True)
            self.ui.labelStatus.setPixmap(KIcon("emblem-important").pixmap(32))

    def toggleConnection(self):
        if self.ui.checkToggler.isChecked():
            self.iface.connect(self.package, self.profile)
        else:
            self.iface.disconnect(self.package, self.profile)


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
from ui_service import Ui_ServiceWidget


class ServiceWidget(QtGui.QWidget, Ui_ServiceWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.state = False

        # Signals
        self.connect(self.pushToggle, QtCore.SIGNAL("clicked()"), lambda: self.emit(QtCore.SIGNAL("stateChanged(int)"), not self.getState()))

    def setState(self, state):
        self.state = state
        if state:
            self.labelStatus.setText(kdecore.i18n("Firewall is activated."))
            self.labelIcon.setPixmap(kdeui.KIcon("document-encrypt").pixmap(48, 48))
            self.pushToggle.setIcon(kdeui.KIcon("media-playback-stop"))
            self.pushToggle.setText(kdecore.i18n("Stop"))
        else:
            self.labelStatus.setText(kdecore.i18n("Firewall is deactivated."))
            self.labelIcon.setPixmap(kdeui.KIcon("document-decrypt").pixmap(48, 48))
            self.pushToggle.setIcon(kdeui.KIcon("media-playback-start"))
            self.pushToggle.setText(kdecore.i18n("Start"))

    def getState(self):
        return self.state

    def setEnabled(self, enabled):
        self.pushToggle.setEnabled(enabled)

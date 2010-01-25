#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file

from qt import *
from kdecore import *
from InfoDialog import *
from Notifier import *
from Icons import *
import PisiIface
import Globals

class Info(InfoDialog):
    def __init__(self, parent=None):
        InfoDialog.__init__(self)
        self.parent = parent
        self.autoRestart = False
        self.notifier = Notifier()
        self.iface = PisiIface.Iface()
        self.timer = QTimer()
        self.timer.connect(self.timer, SIGNAL("timeout()"), self.updateNotification)
        self.connect(self.okButton, SIGNAL('clicked()'), self.accept)
        self.connect(self.cancelButton, SIGNAL('clicked()'), self.reject)
        self.connect(self.autoRestartCheckBox, SIGNAL("toggled(bool)"), self.setAutoRestart)

    def reset(self):
        self.counter = 10
        self.autoRestart = False
        self.autoRestartCheckBox.setChecked(False)

    def setAutoRestart(self, enabled):
        self.autoRestart = enabled

    def autoRestartChecked(self):
        return self.autoRestart

    def showRequirements(self):
        self.reset()
        self.updateNotification()
        return self.exec_loop()

    def updateNotification(self):
        self.timer.stop()
        self.showNotification()
        if self.counter:
            self.timer.start(1000)
        self.counter -= 1

    def showNotification(self):
        icon = getIconPath("package-manager")
        message = i18n("Will Restart in %1 Seconds!").arg(self.counter)
        header = i18n("Will Restart!")
        actions = ["cancel", unicode(i18n("Cancel"))]
        self.notifier.show(icon, header, message, actions)

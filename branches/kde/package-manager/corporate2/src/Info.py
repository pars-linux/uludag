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
import PisiIface
import Globals

class Info(InfoDialog):
    def __init__(self, parent=None):
        InfoDialog.__init__(self)
        self.parent = parent
        self.autoRestart = False
        self.iface = PisiIface.Iface()
        self.connect(self.okButton, SIGNAL('clicked()'), self.accept)
        self.connect(self.cancelButton, SIGNAL('clicked()'), self.reject)
        self.connect(self.autoRestartCheckBox, SIGNAL("toggled(bool)"), self.setAutoRestart)

    def reset(self):
        self.autoRestart = False
        self.autoRestartCheckBox.setChecked(False)

    def setAutoRestart(self, enabled):
        self.autoRestart = enabled

    def autoRestartChecked(self):
        return self.autoRestart

    def showRequirements(self):
        self.reset()
        return self.exec_loop()

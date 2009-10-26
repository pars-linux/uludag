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

from qt import *

from kdeui import *
from kdecore import *

from ui_maindialog import UI_MainDialog

import state

class MainDialog(UI_MainDialog):
    def __init__(self, parent=None):
        UI_MainDialog.__init__(self, parent)
        self.setFonts()
        self.setTitle()
        self.state = state.State(self)
        self.connect(self.upgradeButton, SIGNAL("clicked()"), self.upgrade)
        self.connect(self.cancelButton, SIGNAL("clicked()"), self.cancel)

    def setTitle(self):
        try:
            currentRelease = " ".join(open("/etc/pardus-release", "r").readline().split()[0:2])
        except Exception, e:
            currentRelease = "Pardus 2008"
        self.versionTo.setText(i18n("Upgrading from %1 to version 2009.1").arg(currentRelease))

    def upgrade(self):
        self.state.runNextStep()
        self.upgradeButton.setEnabled(False)
        self.cancelButton.setEnabled(True)

    def cancel(self):
        self.operationStatus.setText("")
        self.state.comar.cancel()
        self.state.reset()
        self.cancelButton.setEnabled(False)
        self.upgradeButton.setEnabled(True)
        self.resetSteps()

    def setFonts(self):
        self.normalFont = QFont()
        self.normalFont.setWeight(50)
        self.normalFont.setBold(False)

        self.boldFont = QFont()
        self.boldFont.setWeight(50)
        self.boldFont.setBold(True)

    def loadIcon(self, name, group=KIcon.Desktop, size=16):
        return KGlobal.iconLoader().loadIcon(name, group, size)

    def resetSteps(self):
        for step in range(1, 5):
            step_icon = getattr(self, "step%d_icon" % step)
            step_icon.setPixmap(QPixmap(""))
            step_label = getattr(self, "step%d_label" % step)
            step_label.setFont(self.normalFont)

    def step_selected(self, step):
        step_icon = getattr(self, "step%d_icon" % step)
        step_icon.setPixmap(self.loadIcon("arrow", KIcon.Small))
        step_label = getattr(self, "step%d_label" % step)
        step_label.setFont(self.boldFont)

    def step_finished(self, step):
        step_icon = getattr(self, "step%d_icon" % step)
        step_icon.setPixmap(self.loadIcon("check", KIcon.Small))
        step_label = getattr(self, "step%d_label" % step)
        step_label.setFont(self.normalFont)

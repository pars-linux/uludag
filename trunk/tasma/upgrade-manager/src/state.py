#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING .
#

from qt import QObject, PYSIGNAL, QTimer
from kdecore import i18n
from kdeui import KMessageBox, KGuiItem

import os
import commander
import pisiiface

STEPS = ["prepare", "setRepositories", "download", "upgrade"]

class State(QObject):

    def __init__(self, parent):
        self.parent = parent
        self.comar = commander.Commander()
        self.step = 0
        self.connect(self.comar, PYSIGNAL("stepStarted(QString)"), self.stepStarted)
        self.connect(self.comar, PYSIGNAL("stepFinished(QString)"), self.stepFinished)
        self.connect(self.comar, PYSIGNAL("stepFinished(QString)"), lambda:QTimer.singleShot(1000, self.runNextStep))
        self.connect(self.comar, PYSIGNAL("statusDownloading(int, int)"), self.statusDownloading)
        self.connect(self.comar, PYSIGNAL("statusInstalling(int, int)"), self.statusInstalling)

    def reset(self):
        self.step = 0

    def statusDownloading(self, total, current):
        message = i18n("<qt>Downloading %1 of %2 packages</qt>").arg(current).arg(total)
        self.parent.operationStatus.setText(message)

    def statusInstalling(self, total, current):
        message = i18n("<qt>Installing %1 of %2 packages</qt>").arg(current).arg(total)
        self.parent.operationStatus.setText(message)

    def stepStarted(self, operation):
        # System.Upgrader.{prepare, setRepositories...}
        step = operation.split(".")[-1]
        self.parent.step_selected(STEPS.index(step) + 1)

    def stepFinished(self, operation):
        step = operation.split(".")[-1]
        self.parent.step_finished(STEPS.index(step) + 1)
        self.step += 1

    def checkObsoletes(self):
        obsoletes = pisiiface.getObsoletedList()
        message = i18n("<qt>Following packages are obsoleted and are not maintained anymore in Pardus 2009 repositories. These packages are going to be removed from your system:<br><br> %1").arg(", ".join(obsoletes))
        message += i18n("<br><br>Do you want to continue?</qt>")

        if KMessageBox.Yes == KMessageBox.warningYesNo(self.parent,
                                                       message,
                                                       i18n("Warning"),
                                                       KGuiItem(i18n("Continue"), "ok"),
                                                       KGuiItem(i18n("Cancel"), "no"),
                                                       ):
            return True

    def runNextStep(self):
        if STEPS[self.step] == "download":
            if not self.checkObsoletes():
                self.parent.cancel()
                return
        method = getattr(self.comar, STEPS[self.step])
        method()

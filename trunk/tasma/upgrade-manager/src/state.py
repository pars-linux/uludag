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

from qt import QObject, PYSIGNAL

import os
import commander

STEPS = ["prepare", "setRepositories", "download", "upgrade", "cleanup"]

class State(QObject):

    def __init__(self, parent):
        self.parent = parent
        self.comar = commander.Commander()
        self.step = 0
        self.connect(self.comar, PYSIGNAL("stepStarted(QString)"), self.stepStarted)
        self.connect(self.comar, PYSIGNAL("stepFinished(QString)"), self.stepFinished)
        self.connect(self.comar, PYSIGNAL("stepFinished(QString)"), self.runNextStep)

    def reset(self):
        self.step = 0

    def stepStarted(self, operation):
        # System.Upgrader.{prepare, setRepositories...}
        step = operation.split(".")[-1]
        self.parent.step_selected(STEPS.index(step) + 1)

    def stepFinished(self, operation):
        step = operation.split(".")[-1]
        self.parent.step_finished(STEPS.index(step) + 1)
        self.step += 1

    def runNextStep(self):
        method = getattr(self.comar, STEPS[self.step])
        method()

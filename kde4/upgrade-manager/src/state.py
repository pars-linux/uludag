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

from PyQt4.QtCore import QObject, SIGNAL

import comariface

STEPS = ["prepare", "setRepositories", "download", "upgrade", "cleanup"]

class State(QObject):

    def __init__(self, parent):
        self.parent = parent
        self.comar = comariface.ComarIface()
        self.connect(self.comar, SIGNAL("stepStarted(QString)"), self.stepStarted)
        self.connect(self.comar, SIGNAL("stepFinished(QString)"), self.stepFinished)
        self.current = self.__get_state() or "prepare"

    def prepare(self):
        self.comar.prepare()

    def setRepositories(self):
        self.comar.setRepositories()

    def download(self):
        self.comar.download()

    def upgrade(self):
        self.comar.upgrade()

    def cleanup(self):
        self.comar.cleanup()

    def stepStarted(self, operation):
        # System.Upgrader.{prepare, setRepositories...}
        step = operation.split(".")[-1]
        self.parent.step_selected(STEPS.index(step) + 1)

    def stepFinished(self, operation):
        step = operation.split(".")[-1]
        self.parent.step_finished(STEPS.index(step) + 1)

    def __get_state(self):
        stateFile = os.path.join("/var/log/", "pisiUpgradeState")
        if not os.path.exists(stateFile):
            return None

        step = open(stateFile, "r").read()
        if step in STEPS:
            return step

        return None

    def run(self):
        for step in STEPS:
            if step == self.current:
                method = getattr(self, step)
                method()

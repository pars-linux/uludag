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

class State:

    def __init__(self):
        pass

    def prepare(self):
        pass

    def setrepos(self):
        pass

    def download(self):
        pass

    def install(self):
        pass

    def cleanup(self):
        pass

    def migrate(self):
        self.prepare()
        self.setrepos()
        self.download()
        self.install()
        self.cleanup()

    def __set_state(self, state):
        stateFile = os.path.join("/var/log/", "upgradeState")
        open(stateFile, "w").write(state)

    def __get_state(self):
        stateFile = os.path.join("/var/log/", "upgradeState")
        if not os.path.exists(stateFile):
            return None
        return open(stateFile, "r").read()

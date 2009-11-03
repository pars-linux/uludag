#!/usr/bin/python
# -*- coding: utf-8 -*-

from ahenk.ajan import utils


class PisiPolicy(utils.Policy):
    label = "PiSi"

    def init(self):
        self.log.debug("*** Reloaded PiSi policy")

    def settingsUpdated(self):
        self.log.debug("*** Updated settings: %s" % self.settings)

    def getTimers(self):
        self.log.debug("*** Returning PiSi timers: %s" % self.settings)
        interval = 20
        if "pisiAutoUpdateInterval" in self.settings:
            interval = int(self.settings["pisiAutoUpdateInterval"][0])

        return {
            "test123": (self.test, interval),
        }

    def apply(self):
        self.log.debug("*** Applying PiSi settings: %s" % self.settings)

    def test(self):
        self.log.debug("*** TEST")


policy = PisiPolicy()

#!/usr/bin/python
# -*- coding: utf-8 -*-

import pisi

from ahenk.ajan import utils


class PisiPolicy(utils.Policy):
    """
        PiSi policy module for keeping system up-to-date.

        Properties:
            label: Policy module label for logger
            pisiInterval: Upgrade interval in seconds
            pisiRepositories: List of package repositories
            pisiMode: Upgrade mode (off, full, security)
    """

    label = "PiSi"

    pisiInterval = 60 * 60 * 12
    pisiRepositories = []
    pisiMode = "off"

    def init(self):
        """
            Thigs to do after module is loaded.
        """
        self.setValues()

    def settingsUpdated(self):
        """
            Things to do after policy has changed.
        """
        self.setValues()

    def getTimers(self):
        """
            Scheduled tasks of policy module.
        """
        return {
            "upgradePackages": (self.upgradePackages, self.pisiInterval),
        }

    def apply(self):
        """
            Things to do after new policy has been fetched.
        """
        pass

    def setValues(self):
        """
            Load policy settings.
        """
        # Update mode
        self.pisiMode = "off"
        if "pisiAutoUpdateMode" in self.settings:
            mode = self.settings["pisiAutoUpdateMode"][0]
            if mode in ["off", "full", "security"]:
                self.pisiMode = mode
        # Update interval
        self.pisiInterval = 60 * 60 * 12
        if "pisiAutoUpdateInterval" in self.settings:
            try:
                self.pisiInterval = int(self.settings["pisiAutoUpdateInterval"][0])
            except ValueError:
                pass
        # Repositories
        self.pisiRepositories = []
        if "pisiRepositories" in self.settings:
            self.pisiRepositories = self.settings["pisiRepositories"][0].split(",")
            # TODO: Set new repository URLs

    def upgradePackages(self):
        """
            Upgrades packages, if necessary.
        """
        if self.pisiMode == "off":
            return
        if pisi.context.locked:
            self.log.debug("PiSi is already updating system. Will try later.")
            return
        if not len(pisi.api.list_repos()):
            self.log.debug("No PiSi repositories defined.")
            return
        # Update PiSi first
        self.runCommand("pisi up --yes-all pisi")
        # Do other updates
        if self.pisiMode == "full":
            self.runCommand("pisi up --yes-all")
        elif self.pisiMode == "security":
            self.runCommand("pisi up --yes-all --security-only")


policy = PisiPolicy

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
# Please read the COPYING file.
#

# Comar
import comar


class Interface:
    def __init__(self):
        self.link = comar.Link()
        self.link.setLocale()
        self.link.useAgent()
        self.package = self.getMainPackage()

    def listenSignals(self, func):
        self.link.listenSignals("System.Settings", func)

    def getPackages(self):
        """
            List of packages that provide System.Settings model
        """
        return list(self.link.System.Settings)

    def getMainPackage(self):
        """
            System Manager is heavily mudur dependent.
        """
        return "mudur"

    def listServices(self):
        """
            Returns list of services.
        """
        services = []
        for package in self.link.System.Service:
            services.append((package, self.link.System.Service[package].info()[1]))
        services.sort(key=lambda x: x[1])
        return services

    def listLanguages(self):
        """
            Returns list of languages."
        """
        languages = self.link.System.Settings[self.package].listLanguages()
        languages.sort(key=lambda x: x[1])
        return languages

    def getLanguage(self):
        """
            Returns selected language.
        """
        return self.link.System.Settings[self.package].getLanguage()

    def setLanguage(self, language):
        """
            Sets language.
        """
        self.link.System.Settings[self.package].setLanguage(language)

    def listKeymaps(self, language=""):
        """
            Returns list of keymaps."
        """
        keymaps = self.link.System.Settings[self.package].listKeymaps(language)
        keymaps.sort(key=lambda x: x[1])
        return keymaps

    def getKeymap(self):
        """
            Returns selected keymap.
        """
        return self.link.System.Settings[self.package].getKeymap()

    def setKeymap(self, keymap):
        """
            Sets keymap.
        """
        self.link.System.Settings[self.package].setKeymap(keymap)

    def getHeadStart(self):
        """
            Returns first service to be started.
        """
        return self.link.System.Settings[self.package].getHeadStart()

    def setHeadStart(self, package):
        """
            Sets first service to be started.
        """
        return self.link.System.Settings[self.package].setHeadStart(package)

    def getTTYs(self):
        """
            Returns number of consoles.
        """
        return self.link.System.Settings[self.package].getTTYs()

    def setTTYs(self, count):
        """
            Sets number of consoles.
        """
        return self.link.System.Settings[self.package].setTTYs(count)

    def getClock(self):
        """
            Returns clock settings.
        """
        return self.link.System.Settings[self.package].getClock()

    def setClock(self, utc, adjust):
        """
            Sets clock.
        """
        return self.link.System.Settings[self.package].setClock(utc, adjust)

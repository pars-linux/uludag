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

import string

import comar
import pisi
import groups

from pmlogging import logger

class Singleton(object):
    def __new__(type):
        if not '_the_instance' in type.__dict__:
            type._the_instance = object.__new__(type)
        return type._the_instance

class Iface(Singleton):

    (SYSTEM, REPO) = range(2)

    def __init__(self, source=REPO):
        if not self.initialized():
            self.source = source
            self.initComar()
            self.initDB()

    def initialized(self):
        return "link" in self.__dict__

    def initComar(self):
        self.link = comar.Link()
        self.link.setLocale()
        self.link.listenSignals("System.Manager", self.signalHandler)

    def initDB(self):
        self.pdb  = pisi.db.packagedb.PackageDB()
        self.cdb  = pisi.db.componentdb.ComponentDB()
        self.idb  = pisi.db.installdb.InstallDB()
        self.rdb  = pisi.db.repodb.RepoDB()

    def setHandler(self, handler):
        self.link.listenSignals("System.Manager", handler)

    def signalHandler(self, package, signal, args):
        if signal == "finished":
            pisi.db.invalidate_caches()
            self.initDB()

    def handler(self, *args):
        pass

    def installPackages(self, packages):
        logger.debug("Installing packages: %s" % packages)
        packages = string.join(packages,",")
        self.link.System.Manager["pisi"].installPackage(packages, async=self.handler)

    def removePackages(self, packages):
        logger.debug("Removing packages: %s" % packages)
        packages = string.join(packages,",")
        self.link.System.Manager["pisi"].removePackage(packages, async=self.handler)

    def upgradePackages(self, packages):
        logger.debug("Upgrading packages: %s" % packages)
        packages = string.join(packages,",")
        self.link.System.Manager["pisi"].updatePackage(packages, async=self.handler)

    def updateRepositories(self):
        logger.debug("Updating repositories...")
        self.link.System.Manager["pisi"].updateAllRepositories(async=self.handler)

    def clearCache(self, limit):
        logger.debug("Clearing cache with limit: %s" % limit)
        self.link.System.Manager["pisi"].clearCache("/var/cache/pisi/packages", limit)

    def setCacheLimit(self, useCache, limit):
        logger.debug("Use cache: %s - change limit to: %s" % (useCache, limit))
        self.link.System.Manager["pisi"].setCache(useCache, limit)

    def setConfig(self, category, name, value):
        logger.debug("Setting config... Category: %s, Name: %s, Value: %s" % (category, name, value))
        self.link.System.Manager["pisi"].setConfig(category, name, value)

    def setSource(self, source):
        self.source = source

    def getPackageList(self):
        if self.source == self.REPO:
            return list( set(pisi.api.list_available()) - set(pisi.api.list_installed()) - set(pisi.api.list_replaces().values()) )
        else:
            return pisi.api.list_installed()

    def getUpdates(self):
        return pisi.api.list_upgradable()

    def getGroups(self):
        _groups = []
        for group in groups.getGroups():
            _groups.append(groups.groups[group])
        return _groups

    def getGroupPackages(self, name):
        components = groups.getGroupComponents(name)
        packages = []
        for component in components:
            try:
                packages.extend(self.cdb.get_union_packages(component))
            except Exception:
                pass
        return packages

    def getGroupComponents(self, name):
        return groups.getGroupComponents(name)

    def getPackage(self, name):
        if self.source == self.REPO:
            return self.pdb.get_package(name)
        else:
            return self.idb.get_package(name)

    def getDepends(self, packages):
        if not self.idb.has_package(packages[0]):
            deps = set(pisi.api.get_install_order(packages))
        else:
            deps = set(pisi.api.get_upgrade_order(packages))
        return list(set(deps) - set(packages))

    def getRequires(self, packages):
        revDeps = set(pisi.api.get_remove_order(packages))
        return list(set(revDeps) - set(packages))

    def getConfig(self):
        return pisi.configfile.ConfigurationFile("/etc/pisi/pisi.conf")

    def getRepositories(self):
        repos = []
        for repo in self.rdb.get_binary_repos():
            repos.append((repo, self.rdb.get_repo_url(repo)))
        return repos

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

from qt import QMutex
from PmLogging import logger

class RepoError:
    pass

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
            self.com_lock = QMutex()
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
        self.gdb  = pisi.db.groupdb.GroupDB()
        self.replaces = self.pdb.get_replaces()

    def setHandler(self, handler):
        self.link.listenSignals("System.Manager", handler)

    def setExceptionHandler(self, handler):
        self.exceptionHandler = handler

    def invalidate_db_caches(self):
        pisi.db.invalidate_caches()
        self.initDB()

    def signalHandler(self, package, signal, args):
        if signal == "finished":
            self.invalidate_db_caches()

    def handler(self, package, exception, args):
        if exception:
            logger.debug("Exception caught by COMAR: %s" % exception)
            self.invalidate_db_caches()
            self.exceptionHandler(exception)

    def installPackages(self, packages):
        logger.debug("Installing packages: %s" % packages)
        packages = string.join(packages,",")
        self.com_lock.lock()
        self.link.System.Manager["pisi"].installPackage(packages, async=self.handler, timeout=2**16-1)

    def removePackages(self, packages):
        logger.debug("Removing packages: %s" % packages)
        packages = string.join(packages,",")
        self.com_lock.lock()
        self.link.System.Manager["pisi"].removePackage(packages, async=self.handler, timeout=2**16-1)

    def upgradePackages(self, packages):
        logger.debug("Upgrading packages: %s" % packages)
        packages = string.join(packages,",")
        self.com_lock.lock()
        self.link.System.Manager["pisi"].updatePackage(packages, async=self.handler, timeout=2**16-1)

    def updateRepositories(self):
        logger.debug("Updating repositories...")
        self.com_lock.lock()
        self.link.System.Manager["pisi"].updateAllRepositories(async=self.handler, timeout=2**16-1)

    def updateRepository(self, repo):
        logger.debug("Updating %s..." % repo)
        self.com_lock.lock()
        self.link.System.Manager["pisi"].updateRepository(repo, async=self.handler, timeout=2**16-1)

    def clearCache(self, limit):
        logger.debug("Clearing cache with limit: %s" % limit)
        self.com_lock.lock()
        self.link.System.Manager["pisi"].clearCache("/var/cache/pisi/packages", limit)

    def setRepositories(self,  repos):
        logger.debug("Re-setting repositories: %s" % repos)
        self.com_lock.lock()
        self.link.System.Manager["pisi"].setRepositories(repos)

    def setRepoActivities(self, repos):
        logger.debug("Re-setting repo activities: %s" % repos)
        self.com_lock.lock()
        self.link.System.Manager["pisi"].setRepoActivities(repos)

    def __configChanged(self, category, name, value):
        config = self.getConfig()
        return not str(config.get(category, name)) == str(value)

    def setCacheLimit(self, useCache, limit):
        logger.debug("Use cache: %s - change limit to: %s" % (useCache, limit))
        if not self.__configChanged("general", "package_cache", useCache) and not self.__configChanged("general", "package_cache_limit", limit):
            return
        self.link.System.Manager["pisi"].setCache(useCache, limit)

    def setConfig(self, category, name, value):
        logger.debug("Setting config... Category: %s, Name: %s, Value: %s" % (category, name, value))
        if not self.__configChanged(category, name, value):
            return
        self.link.System.Manager["pisi"].setConfig(category, name, value)

    def setSource(self, source):
        self.source = source

    def getPackageRepository(self, name):
        try:
            return self.pdb.which_repo(name)
        except Exception:
            return "N/A"

    def calculate_download_size(self, packages):
        try:
            total, cached = pisi.api.calculate_download_size(packages)
            return total - cached
        except OSError, e:
            return None

    def getPackageList(self):
        if self.source == self.REPO:
            return list( set(pisi.api.list_available()) - set(pisi.api.list_installed()) - set(self.replaces.values()) )
        else:
            return pisi.api.list_installed()

    def getUpdates(self):
        lu = set(pisi.api.list_upgradable())
        for replaced in self.replaces.keys():
            lu.remove(replaced)
            lu.add(self.replaces[replaced])
        return lu

    def getGroup(self, name):
        return self.gdb.get_group(name)

    def getGroups(self):
        return self.gdb.list_groups()

    def getGroupPackages(self, name):
        try:
            components = self.gdb.get_group_components(name)
        except pisi.db.groupdb.GroupNotFound:
            components = []
        packages = []
        for component in components:
            try:
                packages.extend(self.cdb.get_union_packages(component))
            except Exception:
                pass
        return packages

    def getGroupComponents(self, name):
        return groups.getGroupComponents(name)

    def getIsaPackages(self, isa):
        if self.source == self.REPO:
            return self.pdb.get_isa_packages(isa)
        else:
            return self.idb.get_isa_packages(isa)

    def getPackage(self, name):
        if self.source == self.REPO:
            return self.pdb.get_package(name)
        else:
            return self.idb.get_package(name)

    def getDepends(self, packages):
        base = pisi.api.get_base_upgrade_order(packages)
        if not self.idb.has_package(packages[0]):
            deps = pisi.api.get_install_order(packages)
        else:
            deps = pisi.api.get_upgrade_order(packages)
        return list(set(deps + base) - set(packages))

    def getRequires(self, packages):
        revDeps = set(pisi.api.get_remove_order(packages))
        return list(set(revDeps) - set(packages))

    def getExtras(self, packages):
        if not packages:
            return []
        if self.source == self.REPO:
            return self.getDepends(packages)
        else:
            return self.getRequires(packages)

    def getConfig(self):
        return pisi.configfile.ConfigurationFile("/etc/pisi/pisi.conf")

    def getRepositories(self):
        repos = []
        for repo in pisi.api.list_repos(only_active=False):
            repos.append((repo, self.rdb.get_repo_url(repo)))
        return repos

    def getRepositoryUrl(self, repo):
        return self.rdb.get_repo_url(repo)

    def getPackageSize(self, name):
        package = self.getPackage(name)
        if self.source == self.REPO:
            return package.packageSize
        else:
            return package.installedSize

    def getConflicts(self, packages):
        return pisi.api.get_conflicts(packages + self.getExtras(packages))

    def isRepoActive(self, name):
        return self.rdb.repo_active(name)

    def cancel(self):
        self.link.cancel()

    def operationInProgress(self):
        print self.link.listRunning()
        return False

    def search_in_installed(self, terms):
        return pisi.api.search_installed(terms)

    def search_in_repos(self, terms):
        installdb = pisi.db.installdb.InstallDB()
        # search in repos but filter installed ones
        return filter(lambda x:not installdb.has_package(x), pisi.api.search_package(terms))
    
    def search_in_upgradables(self, terms):
        return list(set(getUpdates()).intersection(pisi.api.search_package(terms)))

    def search(self, terms, packages=None):
        try:
            if self.source == self.REPO:
                return self.pdb.search_in_packages(packages, terms)
            else:
                return self.idb.search_package(terms)
        except Exception:
            return []

    def parsePackageName(self, name):
        return pisi.util.parse_package_name(name)
    
    def inProgress(self):
        return False


#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009-2010, TUBITAK/UEKAE
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

from pmlogging import logger
from statemanager import StateManager

class Singleton(object):
    def __new__(type):
        if not '_the_instance' in type.__dict__:
            type._the_instance = object.__new__(type)
        return type._the_instance

class Iface(Singleton):

    """ Pisi Iface for PM """

    def __init__(self):
        if not self.initialized():
            self.initComar()
            self.initDB()

    def initialized(self):
        return "link" in self.__dict__

    def initComar(self):
        """ Initialize Comar """
        self.link = comar.Link()
        self.link.setLocale()
        self.link.listenSignals("System.Manager", self.signalHandler)

    def initDB(self):
        """ DBs provided by Pisi Api """
        # Not Installed Packages DB
        self.pdb = pisi.db.packagedb.PackageDB()
        # Components DB
        self.cdb = pisi.db.componentdb.ComponentDB()
        # Installed Packages DB
        self.idb = pisi.db.installdb.InstallDB()
        # Repositories DB
        self.rdb = pisi.db.repodb.RepoDB()
        # Groups DB
        self.gdb = pisi.db.groupdb.GroupDB()
        # Replaced Packages list
        self.replaces = self.pdb.get_replaces()

    def setHandler(self, handler):
        """ Comar Handler """
        self.link.listenSignals("System.Manager", handler)

    def setExceptionHandler(self, handler):
        """ Exception Handler for all exceptions """
        self.exceptionHandler = handler

    def invalidate_db_caches(self):
        pisi.db.invalidate_caches()
        self.initDB()

    def signalHandler(self, package, signal, args):
        if signal == "finished":
            self.invalidate_db_caches()

    def handler(self, package, exception, args):
        """ Handler just for exceptions """
        if exception:
            logger.debug("Exception caught by COMAR: %s" % exception)
            self.invalidate_db_caches()
            self.exceptionHandler(exception)

    # Actions
    def installPackages(self, packages):
        logger.debug("Installing packages: %s" % packages)
        packages = string.join(packages,",")
        self.link.System.Manager["pisi"].installPackage(packages, async=self.handler, timeout=2**16-1)

    def removePackages(self, packages):
        logger.debug("Removing packages: %s" % packages)
        packages = string.join(packages,",")
        self.link.System.Manager["pisi"].removePackage(packages, async=self.handler, timeout=2**16-1)

    def upgradePackages(self, packages):
        logger.debug("Upgrading packages: %s" % packages)
        packages = string.join(packages,",")
        self.link.System.Manager["pisi"].updatePackage(packages, async=self.handler, timeout=2**16-1)

    def modifyPackages(self, packages):
        # FIXME
        pass

    def updateRepositories(self):
        logger.debug("Updating repositories...")
        self.link.System.Manager["pisi"].updateAllRepositories(async=self.handler, timeout=2**16-1)

    def updateRepository(self, repo):
        logger.debug("Updating %s..." % repo)
        self.link.System.Manager["pisi"].updateRepository(repo, async=self.handler, timeout=2**16-1)

    def removeRepository(self, repo):
        logger.debug("Removing repository: %s" % repo)
        self.link.System.Manager["pisi"].removeRepository(repo, async=self.handler, timeout=2**16-1)

    def clearCache(self, limit):
        config = self.getConfig()
        cache_dir = config.get("directories", "cached_packages_dir")
        logger.debug("Clearing cache %s with limit: %s" % (cache_dir, limit))
        self.link.System.Manager["pisi"].clearCache(cache_dir, limit)

    def setRepositories(self,  repos):
        logger.debug("Re-setting repositories: %s" % repos)
        self.link.System.Manager["pisi"].setRepositories(repos)

    def setRepoActivities(self, repos):
        logger.debug("Re-setting repo activities: %s" % repos)
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

    def getPackageRequirements(self, packages):
        """
            Returns dict from pisi api
            { "systemRestart" : ["kernel", "module-alsa-driver"],
              "serviceRestart": ["mysql-server", "memcached", "postfix"] }
        """
        return pisi.api.get_package_requirements(packages)

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
        return pisi.api.list_installed() + list( set(pisi.api.list_available()) - set(pisi.api.list_installed()) - set(sum(self.replaces.values(), [])) )

    def getInstalledPackages(self):
        return pisi.api.list_installed()

    def getNewPackages(self):
        return list( set(pisi.api.list_available()) - set(pisi.api.list_installed()) - set(sum(self.replaces.values(), [])) )

    def getUpdates(self):
        lu = set(pisi.api.list_upgradable())
        for replaced in self.replaces.keys():
            lu.remove(replaced)
            lu |= set(self.replaces[replaced])
        return lu

    def filterUpdates(self, updates, _type):
        return filter(lambda x: self.getPackage(x)._type == _type, updates)

    def filterPackages(self, packages, installed):
        return filter(lambda x: self.getPackage(x).installed == installed, packages)

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
        return self.pdb.get_isa_packages(isa) + self.idb.get_isa_packages(isa)

    def getPackage(self, name):

        if self.idb.has_package(name):
            pkg = self.idb.get_package(name)
            pkg._type = self.getUpdateType(pkg)
            pkg.installed = True
        else:
            pkg = self.pdb.get_package(name)
            pkg._type = None
            pkg.installed = False

        return pkg

    def getInstalledVersion(self, name):
        if self.idb.has_package(name):
            return self.idb.get_package(name).version
        return ''

    def getDepends(self, packages):
        base = pisi.api.get_base_upgrade_order(packages)
        includes_replaces = set(sum(self.replaces.values(), [])).intersection(packages)
        if not self.idb.has_package(packages[0]) and not includes_replaces:
            deps = pisi.api.get_install_order(packages)
        else:
            deps = pisi.api.get_upgrade_order(packages)
        return list(set(deps + base) - set(packages))

    def getRequires(self, packages):
        revDeps = set(pisi.api.get_remove_order(packages))
        return list(set(revDeps) - set(packages))

    def getExtras(self, packages, state):
        if not packages:
            return []
        if state == StateManager.INSTALL:
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

    def getUpdateType(self, pkg):
        (version, release, build) = self.idb.get_version(pkg.name)
        for type_name in ("security", "critical"):
            if pkg.has_update_type(type_name, release):
                return type_name
        return "normal"

    def getPackageSize(self, name):
        package = self.getPackage(name)
        if package.installed:
            return package.installedSize
        return package.packageSize

    def getConflicts(self, packages, state):
        return pisi.api.get_conflicts(packages + self.getExtras(packages, state))

    def isRepoActive(self, name):
        return self.rdb.repo_active(name)

    def checkDistributionAndArchitecture(self, repo):
        return self.rdb.check_distribution(repo) and self.rdb.check_architecture(repo)

    def checkUpdateActions(self, packages):
        actions = {'systemRestart':[], 'serviceRestart':[]}
        for package in packages:
            if self.idb.has_package(package):
                package = self.pdb.get_package(package)
                package_actions = package.get_update_actions()
                for action in actions:
                    if action in package_actions:
                        actions[action].extend(package_actions[action])
        return (set(actions['systemRestart']), set(actions['serviceRestart']))

    def cancel(self):
        self.link.cancel()

    def operationInProgress(self):
        print self.link.listRunning()
        return False

    def search(self, terms, packages = None, __tryOnce = False):
        try:
            if packages:
                return self.pdb.search_in_packages(packages, terms)
            return self.idb.search_package(terms) + self.pdb.search_package(terms)
        except IOError:
            if not __tryOnce:
                self.invalidate_db_caches()
                return self.search(terms, packages, __tryOnce = True)
            return []


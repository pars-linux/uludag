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

from pmlogging import logger

import operations

# for rewrited pisi.api functions
#--------------------------------
import pisi.context as ctx
import pisi.pgraph as pgraph
import pisi.util as util

import gettext
__trans = gettext.translation('pisi', fallback=True)
_ = __trans.ugettext
#--------------------------------

class Singleton(object):
    def __new__(type):
        if not '_the_instance' in type.__dict__:
            type._the_instance = object.__new__(type)
        return type._the_instance

class Iface(Singleton, state=None):

    (SYSTEM, REPO) = range(2)

    def __init__(self, source=REPO):
        if not self.initialized():
            self.source = source
            self.initComar()
            if not state == "inAction":  # if not doing any install or remove action
                self.oidb = pisi.db.offline_idb.Offline_InstallDB()
            self.initDB()

        self.operation = operations.Operations()

    def initialized(self):
        return "link" in self.__dict__

    def initComar(self):
        self.link = comar.Link()
        self.link.setLocale()
        self.link.listenSignals("System.Manager", self.signalHandler)

    def initDB(self):
        self.pdb  = pisi.db.packagedb.PackageDB()
        self.cdb  = pisi.db.componentdb.ComponentDB()
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
        all_packages = packages + self.depends_list

        for pkg in all_packages:
            self.oidb.add_package(pkg)

        self.operation.create(all_packages, "install")

    def removePackages(self, packages):
        all_packages = packages + self.requires_list

        for pkg in all_packages:
            self.oidb.remove_package(pkg)

        self.operation.create(all_packages, "remove")

    def upgradePackages(self, packages):
        self.installPackages(packages)

    def updateRepositories(self):
        self.link.System.Manager["pisi"].updateAllRepositories(async=self.handler, timeout=2**16-1)

    def updateRepository(self, repo):
        self.link.System.Manager["pisi"].updateRepository(repo, async=self.handler, timeout=2**16-1)

    def clearCache(self, limit):
        logger.debug("Clearing cache with limit: %s" % limit)
        self.link.System.Manager["pisi"].clearCache("/var/cache/pisi/packages", limit)

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
            return list( set(pisi.api.list_available()) - set(self.oidb.list_installed()) - set(self.replaces.values()) )
        else:
            return self.oidb.list_installed()

    def getUpdates(self):
        lu = set(self.list_upgradable())
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
            return self.oidb.get_isa_packages(isa)

    def getPackage(self, name):
        if self.source == self.REPO:
            return self.pdb.get_package(name)
        else:
            return self.oidb.get_package(name)

    def getDepends(self, packages):
        base = self.get_base_upgrade_order(packages)
        if not self.oidb.has_package(packages[0]):
            deps = pisi.api.get_install_order(packages)
        else:
            deps = self.get_upgrade_order(packages)
        self.depends_list = list(set(deps) - set(packages))
        return list(set(deps) - set(packages))

    def getRequires(self, packages):
        revDeps = set(self.get_remove_order(packages))
        requires_list = list(set(revDeps) - set(packages))
        self.requires_list = list(set(revDeps) - set(packages))
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

    def search(self, terms, packages=None):
        try:
            if self.source == self.REPO:
                return self.pdb.search_in_packages(packages, terms)
            else:
                return self.oidb.search_package(terms)
        except Exception:
            return []


    # Install and Remove package actions above

    def startOperations(self, filename):
        print "startOperations function is running..."
        self.operation.startOperations(filename)

    def install(self, packages):
        print "paketler yüklenecek"
        self.link.System.Manager["pisi"].installPackage(packages, async=self.handler, timeout=2**16-1)
        print "paketler yüklendi"

    def remove(self, packages):
        print "paketler kaldırılacak"
        self.link.System.Manager["pisi"].removePackage(packages, async=self.handler, timeout=2**16-1)
        print "paketler yüklendi"

# --------------------------------------------------------------
# Rewrited pisi.api functions are below with their requirements.
# --------------------------------------------------------------

    def list_upgradable(self):
        """
        Return a list of packages that are upgraded in the repository -> list_of_strings
        """

        #self.oidb = pisi.db.offline_idb.Offline_InstallDB()  # already defined above InitDB()
        is_upgradable = lambda pkg: self.is_upgradable(pkg, ctx.get_option('ignore_build_no'))

        upgradable = filter(self.is_upgradable, self.oidb.list_installed())
        # replaced packages can not pass is_upgradable test, so we add them manually.list_installed())
        upgradable.extend(pisi.api.list_replaces())

        # consider also blacklist filtering
        upgradable = pisi.blacklist.exclude_from(upgradable, ctx.const.blacklist)
        # YAMUK YAPARSA BU PISI.BLACKLIST YAPAR :)

        return upgradable


    def is_upgradable(self, name, ignore_build = False):

        if not self.oidb.has_package(name):
            return False

        (i_version, i_release, i_build, i_distro, i_distro_release) = self.oidb.get_version_and_distro_release(name)

        try:
            version, release, build, distro, distro_release = self.pdb.get_version_and_distro_release(name, self.pdb.which_repo(name))
        except KeyboardInterrupt:
            raise
        except Exception: #FIXME: what exception could we catch here, replace with that.
            return False

        if distro == i_distro and pisi.version.Version(distro_release) > pisi.version.Version(i_distro_release):
            return True
        elif ignore_build or (not i_build) or (not build):
            return pisi.version.Version(i_release) < pisi.version.Version(release)
        else:
            return i_build < build


    def get_base_upgrade_order(self, packages):
        """
        Return a list of packages of the system.base component that needs to be upgraded
        or installed in install order -> list_of_strings
        All the packages of the system.base component must be installed on the system
        @param packages: list of package names -> list_of_strings
        """
        upgrade_order = self.upgrade_base
        order = upgrade_order(packages)
        return list(order)

    def upgrade_base(self, A = set()):
        ignore_build = ctx.get_option('ignore_build_no')
        if not ctx.config.values.general.ignore_safety and not ctx.get_option('ignore_safety'):
            if self.cdb.has_component('system.base'):
                systembase = set(self.cdb.get_union_component('system.base').packages)
                extra_installs = filter(lambda x: not self.oidb.has_package(x), systembase - set(A))
                if extra_installs:
                    ctx.ui.warning(_('Safety switch: Following packages in system.base will be installed: ') +
                            util.strlist(extra_installs))
                G_f, install_order = pisi.operations.install.plan_install_pkg_names(extra_installs)
                extra_upgrades = filter(lambda x: self.is_upgradable(x, ignore_build), systembase - set(install_order))
                upgrade_order = []
                if extra_upgrades:
                    ctx.ui.warning(_('Safety switch: Following packages in system.base will be upgraded: ') +
                            util.strlist(extra_upgrades))
                    G_f, upgrade_order = self.plan_upgrade(extra_upgrades)
                # return packages that must be added to any installation
                return set(install_order + upgrade_order)
            else:
                ctx.ui.warning(_('Safety switch: the component system.base cannot be found'))
        return set()


    def get_upgrade_order(self, packages):
        """
        Return a list of packages in the upgrade order with extra needed
        dependencies -> list_of_strings
        @param packages: list of package names -> list_of_strings
        """
        upgrade_order = self.plan_upgrade
        i_graph, order = upgrade_order(packages)
        return order

    def plan_upgrade(self, A):
        # try to construct a pisi graph of packages to
        # install / reinstall

        G_f = pgraph.PGraph(self.pdb)               # construct G_f

        replaces = self.pdb.get_replaces()
        # Force upgrading of installed but replaced packages or else they will be removed (they are obsoleted also).
        # This is not wanted for a replaced driver package (eg. nvidia-X).
        A = set(A) | set(replaces.values())

        # find the "install closure" graph of G_f by package
        # set A using packagedb
        for x in A:
            G_f.add_package(x)
        B = A

        while len(B) > 0:
            Bp = set()
            for x in B:
                pkg = self.pdb.get_package(x)
                for dep in pkg.runtimeDependencies():
                    # add packages that can be upgraded,
                    if self.oidb.has_package(dep.package) and dep.satisfied_by_installed():
                        continue

                    if dep.satisfied_by_repo():
                        if not dep.package in G_f.vertices():
                            Bp.add(str(dep.package))
                        G_f.add_dep(x, dep)
                    else:
                        ctx.ui.error(_('Dependency %s of %s cannot be satisfied') % (dep, x))
                        raise Exception(_("Upgrade is not possible."))

            B = Bp
            # now, search reverse dependencies to see if anything
            # should be upgraded
            B = A
            while len(B) > 0:
                Bp = set()
                for x in B:
                    pkg = self.pdb.get_package(x)
                    rev_deps = self.pdb.get_rev_deps(x)
                    for (rev_dep, depinfo) in rev_deps:
                        # add only installed but unsatisfied reverse dependencies
                        if (self.oidb.has_package(rev_dep) and
                                not depinfo.satisfied_by_installed() and is_upgradable(rev_dep)):
                            if not depinfo.satisfied_by_repo():
                                raise Exception(_('Reverse dependency %s of %s cannot be satisfied') % (rev_dep, x))
                            if not rev_dep in G_f.vertices():
                                Bp.add(rev_dep)
                                G_f.add_plain_dep(rev_dep, x)
                B = Bp

        if ctx.config.get_option('debug'):
            G_f.write_graphviz(sys.stdout)
        order = G_f.topological_sort()
        order.reverse()
        return G_f, order


    def get_remove_order(self, packages):
        """
        Return a list of packages in the remove order -> list_of_strings
        @param packages: list of package names -> list_of_strings
        """
        remove_order = self.plan_remove
        i_graph, order = remove_order(packages)
        return order

    def plan_remove(self, A):
        # try to construct a pisi graph of packages to
        # install / reinstall

        G_f = pgraph.PGraph(self.oidb)               # construct G_f

        # find the (install closure) graph of G_f by package
        # set A using packagedb
        for x in A:
            G_f.add_package(x)
        B = A
        while len(B) > 0:
            Bp = set()
            for x in B:
                rev_deps = self.oidb.get_rev_deps(x)
                for (rev_dep, depinfo) in rev_deps:
                    # we don't deal with uninstalled rev deps
                    # and unsatisfied dependencies (this is important, too)
                    if self.oidb.has_package(rev_dep) and depinfo.satisfied_by_installed():
                        if not rev_dep in G_f.vertices():
                            Bp.add(rev_dep)
                            G_f.add_plain_dep(rev_dep, x)
            B = Bp
        if ctx.config.get_option('debug'):
            G_f.write_graphviz(sys.stdout)
        order = G_f.topological_sort()
        return G_f, order

# ----------------------------------------------------------------------------------

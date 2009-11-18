#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009 TUBITAK/UEKAE
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Please read the COPYING file.
#

import os
import glob

import pisi.api
from pisi.operations.delta import create_delta_package

from buildfarm import cli, logger, utils
from buildfarm.config import configuration as conf


class PisiApi:
    def __init__(self, stdout=None, stderr=None, outputDir = conf.workdir):
        import pisi.config
        self.options = pisi.config.Options()
        self.options.output_dir = outputDir
        self.options.yes_all = True
        self.options.ignore_file_conflicts = True
        self.options.ignore_package_conflicts = True

        # Enable debug and verbose
        self.options.debug = True
        self.options.verbose = True

        self.options.ignore_check = conf.ignorecheck

        self.options.ignore_sandbox = False

        # Set API options
        pisi.api.set_options(self.options)

        # Set IO streams
        pisi.api.set_io_streams(stdout=stdout, stderr=stderr)

        pisi.api.set_userinterface(cli.CLI(stdout))

        self.__newBinaryPackages = []
        self.__oldBinaryPackages = []

    def close(self):
        pisi.api.ctx.ui.prepareLogs()

    def getPreviousBuild(self, package):
        """ Returns the previous build with buildno < buildno(package) (nearest) """
        package = package.rstrip(".pisi\n").rsplit("-", 3)
        searchedBuild = int(package[3])-1
        retval = None
        foundPackages = None

        while not foundPackages and searchedBuild > 0:
            foundPackages = glob.glob1(conf.binarypath, "%s-[0-9]*-%s.pisi" % (package[0], searchedBuild))
            if foundPackages:
                retval = os.path.basename(foundPackages[0])
            else:
                searchedBuild = searchedBuild - 1

        return retval

    def delta(self, isopackages, oldBinaryPackages, newBinaryPackages):

        # If we don't want to generate delta packages, return None
        if not conf.generatedelta:
            return

        logger.debug("delta() -> oldBinaryPackages: %s" % oldBinaryPackages)
        logger.debug("delta() -> newBinaryPackages: %s" % newBinaryPackages)

        brandNewBinaryPackages = []

        # We should keep a list of the blacklisted packages and return them back
        # for being able to install their full packages correctly in case of a
        # 1->many source pisi package.
        blacklisted_packages = []

        for p in newBinaryPackages:
            if not utils.get_package_name(p) in [utils.get_package_name(pa) for pa in oldBinaryPackages]:
                brandNewBinaryPackages.append(p)

        map(newBinaryPackages.remove, brandNewBinaryPackages)

        # brandNew contains the possible first builds
        # Just add those to the end of newBinaryPackages for
        # correct delta generation..

        oldBinaryPackages.sort()
        newBinaryPackages.sort()
        newBinaryPackages.extend(brandNewBinaryPackages)

        # Delta packages to be installed on farm for upgrading to new packages
        deltas_to_install = []

        # Other delta packages (between older builds or iso builds)
        delta_packages = []

        for pl in zip(oldBinaryPackages, newBinaryPackages):
            # zip() returns [] if oldBinaryPackages is empty.
            logger.debug("Current (old,new) tuple is: %s" % str(pl))

            # Parse the name of the new package
            name = utils.get_package_name(os.path.basename(pl[1]))

            # globs are supported in blacklist delta e.g. module-*
            if name in conf.deltablacklist or name.startswith(tuple([d.split("*")[0] \
                                                        for d in conf.deltablacklist if "*" in d])):
                logger.debug("Skipping %s as it's blacklisted.." % name)
                blacklisted_packages.append(os.path.basename(pl[1]))
                continue

            # Full path of the new package
            p = os.path.join(conf.workdir, pl[1])

            # Look for an old build first
            if pl[0]:
                # Create a delta between the old build and the new one
                logger.info("Building delta between %s[previous build] and %s." % (pl[0], pl[1]))
                deltas_to_install.append(create_delta_package(os.path.join(conf.binarypath, pl[0]), p))

            if isopackages.has_key(name) and isopackages[name] != pl[0]:
                # Build delta between ISO build and current build
                package = os.path.join(conf.binarypath, isopackages[name])
                if os.path.exists(package):
                    logger.info("Building delta between %s[ISO] and %s." % (isopackages[name], pl[1]))
                    delta_packages.append(create_delta_package(package, p))

            # Search for an older build (older < previous)
            previous = self.getPreviousBuild(pl[0])

            if previous and previous != isopackages.get(name):
                # Found build (older-1)
                logger.info("Building delta between %s[older build] and %s." % (previous, pl[1]))
                delta_packages.append(create_delta_package(os.path.join(conf.binarypath, previous), p))

        # Ok for here
        logger.debug("delta() -> deltas_to_install: %s" % deltas_to_install)

        return (deltas_to_install, delta_packages, blacklisted_packages)

    def build(self, pspec):
        pspec = os.path.join(conf.localpspecrepo, pspec)
        if not os.path.exists(pspec):
            logger.error("'%s' does not exist!" % pspec)
            raise ("'%s' does not exist!" % pspec)

        logger.info("BUILD called for %s" % pspec)

        if conf.sandboxblacklist and pspec in conf.sandboxblacklist:
            logger.info("Disabling sandbox for %s" % pspec)
            pisi.api.ctx.set_option("ignore_sandbox", True)

        __newBinaryPackages, __oldBinaryPackages = pisi.api.build(pspec)

        logger.info("Created package(s): %s" % (__newBinaryPackages))
        self.__newBinaryPackages += __newBinaryPackages
        self.__oldBinaryPackages += __oldBinaryPackages

        return (self.__newBinaryPackages, self.__oldBinaryPackages)

    def getInstallOrder(self, packages):
        """ Get installation order for pisi packages. """
        import pisi.pgraph as pgraph

        # d_t: dict assigning package names to metadata's
        d_t = {}

        # dfn: dict assigning package names to package paths
        dfn = {}
        for p in packages:
            package = pisi.package.Package(os.path.join(conf.workdir, p))
            package.read()
            name = str(package.metadata.package.name)
            d_t[name] = package.metadata.package
            dfn[name] = p

        class PackageDB:
            def get_package(self, key, repo = None):
                return d_t[str(key)]

        packagedb = PackageDB()

        A = d_t.keys()
        G_f = pgraph.PGraph(packagedb)

        for x in A:
            G_f.add_package(x)

        B = A
        while len(B) > 0:
            Bp = set()
            for x in B:
                pkg = packagedb.get_package(x)
                for dep in pkg.runtimeDependencies():
                    if dep.satisfied_by_dict_repo(d_t):
                        if not dep.package in G_f.vertices():
                            Bp.add(str(dep.package))
                        G_f.add_dep(x, dep)
            B = Bp

        order = G_f.topological_sort()
        order.reverse()

        return [dfn[p] for p in order]

    def install(self, p):
        a = []
        a.append(p)
        pisi.api.install(a, ignore_file_conflicts=self.options.ignore_file_conflicts,
                            ignore_package_conflicts=self.options.ignore_package_conflicts,
                            reinstall=True)


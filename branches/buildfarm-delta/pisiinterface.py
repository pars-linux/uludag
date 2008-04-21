#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2008 TUBITAK/UEKAE
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Please read the COPYING file.
#

# Standart Python Modules
import os
import glob
import cPickle

# Pisi API
import pisi.api
from pisi.operations.delta import create_delta_package

# Buildfarm Modules
import cli
import config
import logger

# Gettext Support
import gettext
__trans = gettext.translation("buildfarm", fallback = True)
_  =  __trans.ugettext

class PisiApi:

    def __init__(self, stdout=None, stderr=None, outputDir = config.workDir):
        import pisi.config

        self.options = pisi.config.Options()
        self.options.output_dir = outputDir
        self.options.yes_all = True
        self.options.ignore_file_conflicts = True

        self.isoPackages = None

        # FIXME: Band-aid for a while...
        self.options.ignore_sandbox = True

        # Set API options
        pisi.api.set_options(self.options)

        # Set IO streams
        pisi.api.set_io_streams(stdout=stdout, stderr=stderr)

        # Set UI
        pisi.api.set_userinterface(cli.CLI())

        # Unpickle dictionary from data/
        if not self.isoPackages:
            self.isoPackages = cPickle.Unpickler(open("data/2007-3.db", "rb")).load()

        self.__newBinaryPackages = []
        self.__oldBinaryPackages = []

    def _getPreviousBuild(self, package):
        # Returns the previous build with buildno < buildno(package) (nearest one)
        package = package.rstrip(".pisi\n").rsplit("-", 3)
        searchedBuild = int(package[3])-1
        retval = None
        foundPackages = None
        while not foundPackages and searchedBuild > 0:
            foundPackages = glob.glob("%s-*-*-%s.pisi" % (os.path.join(config.binaryPath, package[0]), searchedBuild))
            if foundPackages:
                retval = os.path.basename(foundPackages[0])
            else:
                searchedBuild = searchedBuild - 1

        return retval

    def build(self, pspec):
        pspec = os.path.join(config.localPspecRepo, pspec)
        if not os.path.exists(pspec):
            logger.error(_("'%s' does not exist!") % (pspec))
            raise _("'%s' does not exist!") % pspec

        logger.info(_("BUILD called for %s") % (pspec)) 

        __newBinaryPackages, __oldBinaryPackages = pisi.api.build(pspec)
        logger.info(_("Created package(s): %s") % (__newBinaryPackages))
        self.__newBinaryPackages += __newBinaryPackages
        self.__oldBinaryPackages += __oldBinaryPackages

        # Normalize paths to file names
        return (set(map(lambda x: os.path.basename(x), self.__newBinaryPackages)), \
                set(map(lambda x: os.path.basename(x), self.__oldBinaryPackages)))

    def delta(self, oldBinaryPackages, newBinaryPackages):
        # Sort the lists
        oldBinaryPackages = sorted(oldBinaryPackages)
        newBinaryPackages = sorted(newBinaryPackages)

        # Delta packages to be installed on the farm for upgrading the packages.
        deltas_to_install = []

        # Other delta packages (between older builds or iso builds)
        delta_packages = []

        for pl in zip(oldBinaryPackages, newBinaryPackages):
            # zip() returns [] if oldBinaryPackages is empty.

            # Parse the name of the new package
            name = os.path.basename(pl[1]).rstrip(".pisi").rsplit("-", 3)[0]

            # full path of the new package, e.g : /var/pisi/traceroute-2.7.7-8-9.pisi
            p = os.path.join(config.workDir, pl[1])

            # Look for an old build first.
            if pl[0]:
                # Cached packages dir contains the old build b of the package, so create a delta.
                logger.info(_("Building delta between %s[previous build] and %s." % (pl[0], pl[1])))
                deltas_to_install.append(create_delta_package(os.path.join(config.binaryPath, pl[0]), p))

            if self.isoPackages.has_key(name) and self.isoPackages[name] != pl[0]:
                # build delta between ISO build and current build
                logger.info("building delta package between %s[iso] and %s..\n" % (self.isoPackages[name], pl[1]))
                delta_packages.append(create_delta_package(os.path.join(config.binaryPath, self.isoPackages[name]), p))

            # Search for a precedent build, (b-1).
            previous = self._getPreviousBuild(pl[0])

            if previous and previous != self.isoPackages.get(name):
                # Found build (b-1).
                logger.info(_("Building delta package between %s[more previous] and %s." % (previous, pl[1])))
                delta_packages.append(create_delta_package(os.path.join(config.binaryPath, previous), p))

        print "(deltas_to_install):%s" % str(deltas_to_install)
        print "(delta_packages):%s" % str(delta_packages)

        return (deltas_to_install, delta_packages)

    def install(self, p):
        a = []
        a.append(p)

        # Set ignore_file_conflicts here
        pisi.api.install(a, ignore_file_conflicts=self.options.ignore_file_conflicts)


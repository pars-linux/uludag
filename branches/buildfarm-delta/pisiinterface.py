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

# Pisi API
import pisi.api
from pisi.operations.delta import create_delta_package

# Buildfarm Modules
import config
import logger

# Gettext Support
import gettext
__trans = gettext.translation("buildfarm", fallback = True)
_  =  __trans.ugettext

class CLI(pisi.ui.UI):
    # FIXME: cli/__init__.py is weird!
    def confirm(self, msg):
        # return True for all cases, somehow "yes_all" is not working!
        return True

class PisiApi:

    def __init__(self, stdout=None, stderr=None, outputDir = config.workDir):
        import pisi.config

        self.options = pisi.config.Options()
        self.options.output_dir = outputDir
        self.options.yes_all = True
        self.options.ignore_file_conflicts = True

        # FIXME: Band-aid for a while...
        self.options.ignore_sandbox = True

        # Set API options
        pisi.api.set_options(self.options)

        # Set IO streams
        pisi.api.set_io_streams(stdout=stdout, stderr=stderr)

        # Set UI
        pisi.api.set_userinterface(CLI())

        # Create dictionary from 2007.3 ISO package list
        self._createIsoDictionary("data/packages-2007.3")

        self.__newBinaryPackages = []
        self.__oldBinaryPackages = []

    def _createIsoDictionary(self, packageList):
        self.isoPackages = {}
        lines = open(packageList, "r").readlines()

        for l in lines:
            name = l.rstrip(".pisi\n").rsplit("-", 3)[0]
            self.isoPackages[name] = l.rstrip("\n")

    def _getPreviousBuild(self, package):
        # Returns the previous build with buildno < buildno(package) (nearest one)
        package = package.rstrip(".pisi\n").rsplit("-", 3)
        searchedBuild = int(package[3])-1
        retval = None
        foundPackages = None
        while not foundPackages and searchedBuild > 0:
            #logger.info("searching for build %s" % str(searchedBuild))
            foundPackages = glob.glob("%s-*-*-%s.pisi" % (os.path.join(config.binaryPath, package[0]), searchedBuild))
            if foundPackages:
                retval = os.path.basename(foundPackages[0])
            else:
                searchedBuild = searchedBuild - 1

        #logger.info("retval from _getPreviousBuild() : %s" % str(retval))
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

        delta_packages = []

        for pl in zip(oldBinaryPackages, newBinaryPackages):

            # Parse the name of the new package
            name = os.path.basename(pl[1]).rstrip(".pisi").rsplit("-", 3)[0]

            # full path of the new package, e.g : /var/pisi/traceroute-2.7.7-8-9.pisi
            p = os.path.join(config.workDir, pl[1])

            # If ISO contains this package, build a delta between iso build and new build
            if self.isoPackages.has_key(name):
                logger.info("building delta package between %s[iso] and %s..\n" % (self.isoPackages[name], pl[1]))

                # build delta between ISO build and current build
                delta_packages.append(create_delta_package(os.path.join(config.binaryPath, self.isoPackages[name]), p))

            if pl[0] and pl[0] != self.isoPackages.get(name):
                # Cached packages dir contains the old build b of the package, so create a delta.
                logger.info(_("Building delta between %s[previous build] and %s." % (pl[0], pl[1])))
                delta_packages.append(create_delta_package(os.path.join(config.binaryPath, pl[0]), p))

            # Search for the precedent build, (b-1).
            previous = self._getPreviousBuild(pl[0])

            if previous and previous != self.isoPackages.get(name):
                # Found build (b-1).
                logger.info(_("Building delta package between %s[more previous] and %s." % (previous, pl[1])))
                delta_packages.append(create_delta_package(os.path.join(config.binaryPath, previous), p))

        return delta_packages

    def install(self, p):
        a = []
        a.append(p)

        # Set ignore_file_conflicts here
        pisi.api.install(a, ignore_file_conflicts=self.options.ignore_file_conflicts)


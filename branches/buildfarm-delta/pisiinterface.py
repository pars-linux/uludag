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
    # FIXME: cli/__init__.py
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

        self.__newBinaryPackages = []
        self.__oldBinaryPackages = []

    def _createIsoDictionary(self, packageList):
        self.isoPackages = {}
        lines = open(packageList, "r").readlines()

        for l in lines:
            name = l.rstrip(".pisi\n").rsplit("-", 3)[0]
            self.isoPackages[name] = l.rstrip("\n")

    def build(self, pspec):
        pspec = os.path.join(config.localPspecRepo, pspec)
        if not os.path.exists(pspec):
            logger.error(_("'%s' does not exist!") % (pspec))
            raise _("'%s' is does not exist!") % pspec

        logger.info(_("BUILD called for %s") % (pspec)) 

        (newBinaryPackages, oldBinaryPackages) = pisi.api.build(pspec)
        logger.info(_("Created package(s): %s") % (newBinaryPackages))
        self.__newBinaryPackages += newBinaryPackages
        self.__oldBinaryPackages += oldBinaryPackages

        # Normalize paths to file names
        return (set(map(lambda x: os.path.basename(x), self.__newBinaryPackages)), \
                set(map(lambda x: os.path.basename(x), self.__oldBinaryPackages)))

    def delta(self, oldBinaryPackages, newBinaryPackages):
        # Create dictionary from 2007.3 ISO package list
        self._createIsoDictionary("data/packages-2007.3")

        # Sort the lists
        oldBinaryPackages = sorted(oldBinaryPackages)
        newBinaryPackages = sorted(newBinaryPackages)

        delta_packages = []

        for pl in zip(oldBinaryPackages, newBinaryPackages):
            if pl[0]:
                # Cached packages dir contains the previous build of the package, so create delta.
                logger.info(_("Building delta between %s(previous build) and %s." % (pl[0], pl[1])))
                delta_packages.append(create_delta_package(os.path.join(config.binaryPath, pl[0]), \
                                                           os.path.join(config.workDir, pl[1])))

            # Parse the name, version, release and buildno informations of the new package
            p_list = os.path.basename(pl[1]).rstrip(".pisi").rsplit("-", 3)
            name = p_list[0]
            version = p_list[1]
            release = p_list[2]
            build = p_list[3]

            # ISO build may be equal to the previous build of the package so it's unnecessary
            # to rebuild the same delta.
            if self.isoPackages.has_key(name) and self.isoPackages[name] != pl[0]:
                # FIXME : replace config.pardus2007 with /var/cache/pisi/packages when moved into buildfarm machine

                # full path of the new binary package, e.g : /var/pisi/traceroute-2.7.7-8-9.pisi
                p = os.path.join(config.workDir, pl[1])
                logger.info("building delta between %s(latest iso build) and %s..\n" % (self.isoPackages[name], p))

                # build delta between ISO build and current build
                delta_packages.append(create_delta_package(os.path.join(config.pardus2007, self.isoPackages[name]), p))

        logger.info(_("Created delta package(s): %s" % str(delta_packages)))
        return delta_packages

    def install(self, p):
        a = []
        a.append(p)

        # Set ignore_file_conflicts here
        pisi.api.install(a, ignore_file_conflicts=self.options.ignore_file_conflicts)


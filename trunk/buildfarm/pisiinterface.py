#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Please read the COPYING file.
#

""" Standart Python Modules """
import os

import pisi.api
import pisi.fetcher

""" BuildFarm Modules """
import config
import logger

""" Gettext Support """
import gettext
__trans = gettext.translation("buildfarm", fallback = True)
_  =  __trans.ugettext

class PisiApi:

    def __init__(self, outputDir = config.workDir):
        import pisi.config
        self.options = pisi.config.Options()
        self.options.output_dir = outputDir
        self.options.yes_all = True
        self.options.ignore_file_conflicts = True

        self.__newBinaryPackages = []
        self.__oldBinaryPackages = []

    def init(self, stdout, stderr):
        logger.info(_("Initialising PiSi API..."))
        pisi.api.init(options = self.options, stdout = stdout, stderr = stderr)

    def finalize(self):
        logger.info(_("Finalising PiSi API"))
        pisi.api.finalize()

    def build(self, pspec):
        pspec = os.path.join(config.localPspecRepo, pspec)
        if not os.path.exists(pspec):
            logger.error(_("'%s' is not exists!") % (pspec))
            raise _("'%s' is not exists!") % pspec

        logger.info(_("BUILD called for %s") % (pspec)) 

        __newBinaryPackages, __oldBinaryPackages = pisi.api.build(pspec)
        logger.info(_("Created package(s): %s") % (__newBinaryPackages)) 
        self.__newBinaryPackages += __newBinaryPackages
        self.__oldBinaryPackages += __oldBinaryPackages

        return (self.__newBinaryPackages, self.__oldBinaryPackages)

    def install(self, p):
        a = []
        a.append(p)
        pisi.api.install(a)

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

""" Standart Python Modules """
import os
import sys

""" PiSi Modules """
import pisi.specfile

""" BuildFarm Modules """
import config
import logger

class DependencyResolver:
    def __init__(self, pspeclist):
        self.oldwd = os.getcwd()
        os.chdir(config.localPspecRepo)

        # work queue and wait queue may contain same pspecs,
        # be sure that every pspec is unique in the pspeclist.
        self.pspeclist = [pspec for pspec in set(pspeclist)]

        self.bdepmap, self.rdepmap, self.namemap, self.pspeccount = {}, {}, {}, len(self.pspeclist)

        for pspec in self.pspeclist: self.bdepmap[pspec] = self.__getBuildDependencies__(pspec)
        for pspec in self.pspeclist: self.rdepmap[pspec] = self.__getRuntimeDependencies__(pspec)
        for pspec in self.pspeclist: self.namemap[pspec] = self.__getPackageNames__(pspec)

    # FIXME: http://bugs.pardus.org.tr/show_bug.cgi?id=3854
    def __getBuildDependencies__(self, pspec):
        specFile = pisi.specfile.SpecFile()
        try:
            specFile.read(pspec)
        except:
            logger.error("%s'de sorun var :(" % pspec)
            # FIXME: sys.exit is fatal for server
            sys.exit(-1)

        deps = []
        for package in specFile.source.buildDependencies:
            deps += [package.package]

        return deps

    # FIXME: http://bugs.pardus.org.tr/show_bug.cgi?id=3854
    def __getRuntimeDependencies__(self, pspec):
        try:
            specFile = pisi.specfile.SpecFile(pspec)
        except:
            logger.error("%s'de sorun var :(" % pspec)
            # FIXME: sys.exit is fatal for server
            sys.exit(-1)

        deps = []
        for package in specFile.packages:
            for dep in package.runtimeDependencies():
                deps += [dep.package]

        return deps

    def __getPackageNames__(self, pspec):
        try:
            specFile = pisi.specfile.SpecFile(pspec)
        except:
            logger.error("%s'de sorun var :(" % pspec)
            # FIXME: sys.exit is fatal for server
            sys.exit(-1)

        try:
            return [package.name for package in specFile.packages]
        except:
            return [""]

    def __runtimeDepResolver__(self):
        """arranges the order of the pspec's in the pspeclist to satisfy runtime deps"""
        clean = True
        for i in range(0, self.pspeccount):
            pspec = self.pspeclist[i]
            for p in self.rdepmap.get(pspec):
                for j in range(i+1, self.pspeccount):
                    if p in self.namemap.get(self.pspeclist[j]):
                        self.pspeclist.insert(j+1, self.pspeclist.pop(i))
                        clean = False
        return clean


    def __buildtimeDepResolver__(self):
        """arranges the order of the pspec's in the pspeclist to satisfy build deps"""
        clean = True
        for i in range(0, self.pspeccount):
            pspec = self.pspeclist[i]
            for p in self.bdepmap.get(pspec):
                for j in range(i+1, self.pspeccount):
                    if p in self.namemap.get(self.pspeclist[j]):
                        self.pspeclist.insert(j+1, self.pspeclist.pop(i))
                        clean = False
        return clean

    def resolveDependencies(self):
        while not (self.__buildtimeDepResolver__() and self.__runtimeDepResolver__()): pass

        os.chdir(self.oldwd)
        return self.pspeclist

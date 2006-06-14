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
import sys
import xml.dom.minidom as mdom

""" BuildFarm Modules """
import buildfarm.config as config
import buildfarm.logger as logger
from buildfarm import Get


class DependencyError(Exception):
    pass


class DependencyResolver:
    def __init__(self, pspeclist):
        self.oldwd = os.getcwd()
        os.chdir(config.localPspecRepo)
        
        #work queue and wait queue may contain same pspecs.
        #be sure that every pspec is unique in the pspeclist.
        self.pspeclist = [pspec for pspec in set(pspeclist)]
        
        self.bdepmap, self.rdepmap, self.namemap, self.pspeccount = {}, {}, {}, len(self.pspeclist)

        for pspec in self.pspeclist: self.bdepmap[pspec] = self.__getBuildDependencies(pspec)
        for pspec in self.pspeclist: self.rdepmap[pspec] = self.__getRuntimeDependencies(pspec)
        for pspec in self.pspeclist: self.namemap[pspec] = self.__getPackageNames(pspec)

    def resolvDeps(self):
        while not (self.buildDepResolver() and self.runtimeDepResolver()): pass

        os.chdir(self.oldwd)
        return self.pspeclist

    def __getBuildDependencies(self, pspec):
        try:
            dom = mdom.parse(pspec)
        except:
            logger.error("%s'de sorun var :(" % pspec)
            sys.exit(-1)

        try:
            return [bdep.firstChild.wholeText for bdep in Get(Get(Get(dom.documentElement, "Source")[0], "BuildDependencies")[0], 'Dependency')]
        except:
            return ['']

    def __getRuntimeDependencies(self, pspec):
        try:
            dom = mdom.parse(pspec)
        except:
            logger.error("%s'de sorun var :(" % pspec)
            sys.exit(-1)

        rdeps = []
        try:
            for p in Get(dom.documentElement, "Package"):
                rdeps += [bdep.firstChild.wholeText for bdep in Get(Get(p, "RuntimeDependencies")[0], 'Dependency')]
        except:
            pass

        #remove duplicated entries..
        for d in rdeps:
            for i in range(0, rdeps.count(d)-1):
                rdeps.remove(d)

        return rdeps

    def __getPackageNames(self, pspec):
        packages = []
        try:
            dom = mdom.parse(pspec)
            pspecdata = dom.documentElement
        except:
            logger.error("%s'de sorun var :(" % pspec)
            sys.exit(-1)

        for p in Get(pspecdata, "Package"):
            packages.append(Get(p, "Name")[0].firstChild.wholeText)
        return packages

    def runtimeDepResolver(self):
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


    def buildDepResolver(self):
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

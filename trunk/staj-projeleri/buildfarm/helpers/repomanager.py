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
from string import find

""" BuildFarm Modules """
import config
import logger

Exclude = ["packages", "pisi-index.xml", "README", "TODO", "useful-scripts"]

class RepoError(Exception):
    pass


class RepositoryManager:
    def __getChanges__(self, type="ALL", filter='', exclude=Exclude):
        self.keys = {"U": self.__MODIFIED__, "A": self.__ADDED__, "D": self.__REMOVED__, "ALL": self.__ALL__}
        data = self.keys.get(type)()
        if not len(exclude):
            return [x for x in data if find(x, filter) > -1]
        else:
            rval = data
            for i in range(0, len(exclude)):
                rval = [t for t in [x for x in rval if find(x, filter) > -1] if find(t, exclude[i]) == -1]
            return rval

    def __getRevision__(self):
        # Parses the output and returns the revision number e.g. '15061'
        o = self.output[len(self.output) - 1]
        for i in range(0, len(o)):
            if o[i] == "revision":
                return int(o[i+1].strip("."))

    def __MODIFIED__(self):
        # Returns the list of items marked with U
        data=[]
        for d in self.output:
            if d[0] == "U": data.append(d[1])
        return data

    def __ADDED__(self):
        # Returns the list of items marked with A
        data=[]
        for d in self.output:
            if d[0] == "A": data.append(d[1])
        return data

    def __REMOVED__(self):
        # Returns the list of items marked with D
        data=[]
        for d in self.output:
            if d[0] == "D": data.append(d[1])
        return data

    def __ALL__(self, filter='', exclude=[]):
        # Returns all the items in a list
        return self.__MODIFIED__() + self.__REMOVED__() + self.__ADDED__()

    def updateRepository(self):
        def update():
            # Calls 'svn up' from the directory 'config.localPspecRepo'
            oldwd = os.getcwd()
            os.chdir(config.localPspecRepo)
            logger.info("Yerel pspec deposu güncelleniyor: '%s'" % (config.localPspecRepo))
            f = os.popen("svn up")

            out = [o.split() for o in f.readlines()]
            if f.close():
                logger.error("SVN'de bir sorun var :(")
                raise RepoError("SVN'de bir sorun var:\n %s" % (out))
                # FIXME: sys.exit is fatal for server
                sys.exit(-1)
            os.chdir(oldwd)
            return out

        self.output = update()
        if self.__getRevision__():
            logger.info("Depo güncellendi (%d satır çıktı): Revizyon '%d'" % (len(self.output), self.__getRevision__()))
        else:
            logger.error("Güncelleme başarısız! (localPspecRepo için verilen '%s' adresi yanlış olabilir)" % (config.localPspecRepo))
            raise RepoError("Güncelleme başarısız! (localPspecRepo için verilen '%s' adresi yanlış olabilir)" % (config.localPspecRepo))

        updatedpspecfiles = self.__getChanges__(type = "U", filter="pspec.xml")
        newpspecfiles     = self.__getChanges__(type = "A", filter="pspec.xml")

        if len(updatedpspecfiles + newpspecfiles):
            queue = open(os.path.join(config.workDir, "workQueue"), "a")
            for pspec in updatedpspecfiles + newpspecfiles:
                queue.write("%s\n" % pspec)
            queue.close()
        return updatedpspecfiles + newpspecfiles

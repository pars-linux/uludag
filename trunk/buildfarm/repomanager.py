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

sys.path.append(".")
sys.path.append("..")

""" BuildFarm Modules """
import buildfarm.config as config
import buildfarm.logger as logger
import buildfarm.qmanager as qmanager

Exclude = ["packages", "pisi-index.xml", "README", "TODO", "useful-scripts"]

class RepoError(Exception):
    pass


class RepositoryManager:
    def __init__(self):
        self.keys = {"U": self.MODIFIED, "A": self.ADDED, "D": self.REMOVED, "ALL": self.ALL}

        def update():
            oldwd = os.getcwd()
            os.chdir(config.localPspecRepo)
            logger.info("Yerel pspec deposu güncelleniyor: '%s'" % (config.localPspecRepo))
            f = os.popen("cat svnup")

            out = [o.split() for o in f.readlines()]
            if f.close():
                logger.error("SVN'de bir sorun var :(")
                raise RepoError("SVN'de bir sorun var:\n %s" % (out))
                sys.exit(-1)
            os.chdir(oldwd)
            return out

        self.output = update()
        if self.getRevision():
            logger.info("Depo güncellendi (%d satır çıktı): Revizyon '%d'" % (len(self.output), self.getRevision()))
        else:
            logger.error("Güncelleme başarısız! (localPspecRepo için verilen '%s' adresi yanlış olabilir)" % (config.localPspecRepo))
            raise RepoError("Güncelleme başarısız! (localPspecRepo için verilen '%s' adresi yanlış olabilir)" % (config.localPspecRepo))

    def getChanges(self, type="ALL", filter='', exclude=Exclude):
        data = self.keys.get(type)()
        if not len(exclude):
            return [x for x in data if find(x, filter) > -1]
        else:
            rval = data
            for i in range(0, len(exclude)):
                rval = [t for t in [x for x in rval if find(x, filter) > -1] if find(t, exclude[i]) == -1]
            return rval

    def getRevision(self):
        o = self.output[len(self.output) - 1]
        for i in range(0, len(o)):
            if o[i] == "revision":
                return int(o[i+1].strip("."))
 
    def MODIFIED(self):
        data=[]
        for d in self.output:
            if d[0] == "U": data.append(d[1])
        return data

    def ADDED(self):
        data=[]
        for d in self.output:
            if d[0] == "A": data.append(d[1])
        return data

    def REMOVED(self):
        data=[]
        for d in self.output:
            if d[0] == "D": data.append(d[1])
        return data
        
    def ALL(self, filter='', exclude=[]):
        return self.MODIFIED() + self.REMOVED() + self.ADDED()

if __name__ == "__main__":    
    r = RepositoryManager()
   
    updatedpspecfiles = r.getChanges(type = "U", filter="pspec.xml")
    newpspecfiles     = r.getChanges(type = "A", filter="pspec.xml")

    if len(updatedpspecfiles + newpspecfiles):
        queue = open(os.path.join(config.workDir, "workQueue"), "a")
        for pspec in updatedpspecfiles + newpspecfiles:
            queue.write("%s\n" % pspec)
        queue.close()  

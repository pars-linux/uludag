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

import os
import re
import sys
from pisi.db.sourcedb import SourceDB
from string import find

import config
import logger
import qmanager

Exclude = ["packages", "pisi-index.xml", "README", "TODO", "useful-scripts"]

class RepoError(Exception):
    pass

class RepositoryManager:
    def __init__(self):

        def update():
            logger.info("Updating local pspec repository '%s'" % (config.localPspecRepo))
            f = os.popen("svn up %s" % config.localPspecRepo)

            out = [o.split() for o in f.readlines()]
            if f.close():
                logger.error("A problem with SVN occurred.")
                raise RepoError("A problem with SVN occurred:\n %s" % (out))
                sys.exit(-1)
            return out

        # __init__ starts here
        self.keys = {"U": self.getModified, "A": self.getAdded, "D": self.getRemoved, "ALL": self.getAll}

        self.oldRevision = self.getCurrentRevision()

        # Update repository
        self.output = update()

        if self.getRevision():
            logger.info("Repository is updated (%d lines extracted): Revision %d." % (len(self.output), self.getRevision()))
        else:
            logger.error("Repository update failed.")
            raise RepoError("Repository update failed.")

    def getCurrentRevision(self):
        # Return the current repository revision
        return int(re.search("Revision: [0-9]*\n", os.popen("svn info %s" % config.localPspecRepo).read()).group().split(":")[-1].strip())

    def getChanges(self, type="ALL", filter='', exclude=Exclude):
        data = self.keys.get(type)()
        if not len(exclude):
            return [x for x in data if find(x, filter) > -1]
        else:
            rval = data
            for i in range(0, len(exclude)):
                rval = [t for t in [x for x in rval if find(x, filter) > -1] if find(t, exclude[i]) == -1]
            return rval


    def getReverseDependencies(self, pspecs):
        # Needs a source repository added to system.

        def getPackageName(pspec):
            # Extracts package name from full path to pspec.xml
            return os.path.basename(pspec.rsplit("/pspec.xml")[0])

        breaksABI = []
        revBuildDeps = []

        sdb = SourceDB()

        for p in pspecs:
            f = os.popen("svn di -r %d:%d %s" % (self.oldRevision, self.getRevision(), p)).read().strip().split("\n")
            if "<Action>revDepUpdates</Action>" in [l for l in f if l.startswith("+")]:
                # Now we have the list of packages which break ABI.
                # We need to find out the reverse build dependencies of these packages.
                #(live555 breaks ABI, vlc and mplayer needs live555 during build)
                breaksABI.append(getPackageName)
                for revdep in sdb.get_rev_deps(p):
                    revBuildDeps.append(os.path.join(config.localPspecRepo, sdb.get_spec(revdep).source.partOf.replace(".", "/") + "/pspec.xml"))

        return (breaksABI, revBuildDeps)


    def getRevision(self):
        return int(self.output[-1][self.output[-1].index("revision")+1].strip("."))

    def getModified(self):
        return [d[1] for d in self.output if d[0] == "U"]

    def getAdded(self):
        return [d[1] for d in self.output if d[0] == "A"]

    def getRemoved(self):
        return [d[1] for d in self.output if d[0] == "D"]

    def getAll(self, filter='', exclude=[]):
        return self.getModified() + self.getRemoved() + self.getAdded()


# Main program

if __name__ == "__main__":
    # Print current workqueue/waitqueue
    print "Current workqueue:\n%s" % ('-'*50)
    print "\n".join(open("/var/pisi/workQueue", "rb").read().split("\n"))

    print "\nCurrent waitqueue:\n%s" % ('-'*50)
    print "\n".join(open("/var/pisi/waitQueue", "rb").read().split("\n"))

    # Create RepositoryManager
    r = RepositoryManager()

    # Get updated and newly added pspec list
    updatedpspecfiles = r.getChanges(type = "U", filter="pspec.xml")
    newpspecfiles = r.getChanges(type = "A", filter="pspec.xml")

    # Print the packages that will be pushed to queue
    if updatedpspecfiles or newpspecfiles:
        print "The following packages will be pushed to buildfarm's workqueue:\n%s" % ('-'*50)
        for p in updatedpspecfiles + newpspecfiles:
            print "  * %s" % p

    # Get 'revDepUpdates' containing package list
    (breaksABI, revDepsToBeRecompiled) = r.getReverseDependencies(updatedpspecfiles)

    # Print the revdeps to be recompiled
    if revDepsToBeRecompiled:
        print "These reverse dependencies will be recompiled because of ABI breakage:\n%s" % ('-'*50)
        for p in revdepupdates:
            print "  * %s" % p

    if len(updatedpspecfiles + newpspecfiles):
        queue = open(os.path.join(config.workDir, "workQueue"), "rb").read().strip().split("\n")
        queue.extend(updatedpspecfiles + newpspecfiles)
        open(os.path.join(config.workDir, "workQueue"), "wb").write("\n".join(list(set(queue)))+"\n")


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
import re
import sys
import pisi
from string import find

import config
import logger

Exclude = ["packages", "pisi-index.xml", "README", "TODO", "useful-scripts"]

class RepoError(Exception):
    pass

class RepositoryManager:
    def __init__(self):

        def update():
            logger.info("\nUpdating pisi-index* files..")
            os.system("/usr/bin/svn up %s/pisi-index*" % config.localPspecRepo)
            logger.info("\nUpdating local pspec repository '%s'" % (config.localPspecRepo))
            f = os.popen("/usr/bin/svn up %s" % config.localPspecRepo)

            out = [o.split() for o in f.readlines()]
            if f.close():
                logger.error("A problem with SVN occurred.")
                raise RepoError("A problem with SVN occurred:\n %s" % (out))
                sys.exit(-1)
            return out

        # __init__ starts here

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
        return int(re.search("Revision: [0-9]*\n", os.popen("/usr/bin/svn info %s" % config.localPspecRepo).read()).group().split(":")[-1].strip())

    def getChanges(self, _type="U", _filter='', _exclude=Exclude):
        data = None
        if _type == "U":
            data = self.getModified()
        elif _type == "A":
            data = self.getAdded()
        elif _type == "D":
            data = self.getRemoved()

        if not len(_exclude):
            return [x for x in data if find(x, _filter) > -1]
        else:
            rval = data
            for i in range(0, len(_exclude)):
                rval = [t for t in [x for x in rval if find(x, _filter) > -1] if find(t, _exclude[i]) == -1]
            return rval

    def getRevision(self):
        return int(self.output[-1][self.output[-1].index("revision")+1].strip("."))

    def getModified(self):
        return [d[1] for d in self.output if d[0] == "U"]

    def getAdded(self):
        return [d[1] for d in self.output if d[0] == "A"]

    def getRemoved(self):
        return [d[1] for d in self.output if d[0] == "D"]

# Main program

if __name__ == "__main__":
    # Print current workqueue/waitqueue
    print "Current workqueue:\n%s" % ('-'*60)
    if os.path.exists(os.path.join(config.workDir, "workQueue")):
        print "\n".join(open("/var/pisi/workQueue", "rb").read().split("\n"))

    print "\nCurrent waitqueue:\n%s" % ('-'*60)
    if os.path.exists(os.path.join(config.workDir, "waitQueue")):
        print "\n".join(open("/var/pisi/waitQueue", "rb").read().split("\n"))

    # Create RepositoryManager
    r = RepositoryManager()

    # Get updated and newly added pspec list
    updatedPspecFiles = r.getChanges(type = "U", filter="pspec.xml")
    newPspecFiles = r.getChanges(type = "A", filter="pspec.xml")

    if not (updatedPspecFiles or newPspecFiles):
        print "\nNo new updates concerning source packages.\nExiting."
        sys.exit(0)

    # Print the packages that will be pushed to queue
    print "\nThe following packages will be pushed to buildfarm's workqueue:\n%s" % ('-'*60)
    for p in updatedPspecFiles + newPspecFiles:
        print "  * %s" % p

    if len(updatedPspecFiles + newPspecFiles):
        queue = []
        if os.path.exists(os.path.join(config.workDir, "workQueue")):
            queue = open(os.path.join(config.workDir, "workQueue"), "rb").read().strip().split("\n")

        # Filter out the packages that shouldn't be build on this architecture
        candidateQueue = updatedPspecFiles + newPspecFiles
        queue.extend(filter(lambda x: pisi.ctx.config.values.get('general', 'architecture') not in
                     pisi.specfile.SpecFile(x).source.excludeArch, candidateQueue))

        print "\nThese packages will not be compiled on this architecture:\n%s" % ('-'*60)
        print "\n".join(list(set(candidateQueue).difference(queue)))

        open(os.path.join(config.workDir, "workQueue"), "wb").write("\n".join([l for l in list(set(queue)) if l])+"\n")

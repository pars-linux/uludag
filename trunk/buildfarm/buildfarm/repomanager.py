#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Please read the COPYING file.
#

import re
import os
import sys

import pisi

from buildfarm import logger
from buildfarm.config import configuration as conf

Exclude = ["packages", "pisi-index.xml", "README", "TODO", "useful-scripts"]

class RepoError(Exception):
    pass

class RepositoryManager:
    def __init__(self):

        def update():
            logger.info("\nUpdating pisi-index* files..")
            os.system("/usr/bin/svn up %s/pisi-index*" % conf.localpspecrepo)
            logger.info("\nUpdating local pspec repository '%s'" % (conf.localpspecrepo))
            f = os.popen("/usr/bin/svn up %s" % conf.localpspecrepo)

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
        return int(re.search("Revision: [0-9]*\n", os.popen("/usr/bin/svn info %s" % conf.localpspecrepo).read()).group().split(":")[-1].strip())

    def getChanges(self, type="ALL", filter='', exclude=Exclude):
        data = self.keys.get(type)()
        if not len(exclude):
            return [x for x in data if x.find(filter) > -1]
        else:
            rval = data
            for i in range(0, len(exclude)):
                rval = [t for t in [x for x in rval if x.find(filter) > -1] if t.find(exclude[i]) == -1]
            return rval

    def getReverseDependencies(self, pspecList):
        # Needs a source repository

        def check():
            rdb = pisi.db.repodb.RepoDB()
            try:
                dbname = rdb.get_source_repos()[0]
                pisi.api.update_repo(dbname)
            except IndexError:
                # No source repo
                return False
            else:
                return True

        def getPackageName(pspec):
            # Extracts package name from full path to pspec.xml
            return os.path.basename(pspec.rsplit("/pspec.xml")[0])


        breaksABI = []
        revBuildDeps = set()

        if not check():
            # No source repository
            print "You should add a source repository for reverse dependency checking. Skipping.."
            return (breaksABI, list(revBuildDeps))

        # Create a source db instance
        sdb = pisi.db.sourcedb.SourceDB()

        # Create a diff output of all the repository
        # This is much more efficient that doing 'svn di' for every changed file.
        # difflist is list of tuples: ('kernel/kernel/pspec.xml', commit_diff)
        print "\nCalling svn diff. This may take a little while depending on the repository state.."
        diffoutput = os.popen("/usr/bin/svn di -r %d:%d %s" % (self.oldRevision, self.getRevision(), " ".join(pspecList))).read().strip()
        print "Parsing svn diff output..",
        difflist = [(pspec.split("\n")[0], "".join([l for l in pspec.split("\n")[4:] if l.startswith("+")])) \
                    for pspec in diffoutput.split("Index: ")[1:]]
        print "Done"

        for pspec, diff in difflist:
            if "<Action>reverseDependencyUpdate</Action>" in diff:
                breaksABI.append(getPackageName(pspec))

        # Now we have the list of packages which break ABI.
        # We need to find out the reverse build dependencies of these packages.
        # e.g. live555 breaks ABI, vlc and mplayer needs live555 during build

        for p in breaksABI:
            # FIXME: We also add the subpackages as we can't know which one needs revdepupdate.
            # This may cause a lot of unneeded updates..
            revdeps = []
            for package in [_p.name for _p in sdb.get_spec(p).packages]:
                srevdeps = sdb.get_rev_deps(package)
                if srevdeps:
                    revdeps.extend([d[0] for d in srevdeps])

            for revdep in set(revdeps):
                # e.g. (revdep, revdepObject) = ('vlc', <pisi.dependency.Dependency object at 0xa3284cc>)
                revBuildDeps.add(os.path.join(conf.localpspecrepo, sdb.get_spec(sdb.pkgtosrc(revdep)).source.partOf.replace(".", "/") + "/%s/pspec.xml" % revdep))

        return (breaksABI, list(revBuildDeps))


    def getRevision(self):
        return int(self.output[-1][self.output[-1].index("revision")+1].strip("."))

    def getModified(self):
        return [d[1] for d in self.output if d[0] == "U"]

    def getAdded(self):
        return [d[1] for d in self.output if d[0] == "A"]

    def getRemoved(self):
        return [d[1] for d in self.output if d[0] == "D"]

    def getAll(self):
        return self.getModified() + self.getRemoved() + self.getAdded()


# Main program

if __name__ == "__main__":
    # Print current workqueue/waitqueue
    print "Current workqueue:\n%s" % ('-'*60)
    if os.path.exists(os.path.join(conf.workdir, "workQueue")):
        print "\n".join(open("/var/pisi/workQueue", "rb").read().split("\n"))

    print "\nCurrent waitqueue:\n%s" % ('-'*60)
    if os.path.exists(os.path.join(conf.workdir, "waitQueue")):
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

    # Get 'reverseDependencyUpdate' containing package list
    # A brand new package can't have this property
    (breaksABI, revDepsToBeRecompiled) = r.getReverseDependencies(updatedPspecFiles)

    # Print the revdeps to be recompiled
    if breaksABI:
        print "\nThese updates broke ABI:\n%s" % ('-'*24)
        for p in breaksABI:
            print "  * %s" % p

        if revDepsToBeRecompiled:
            print "\nThese reverse dependencies will be recompiled because of ABI breakage:\n%s" % ('-'*70)
            for p in revDepsToBeRecompiled:
                print "  * %s" % p
        else:
            # p broke API but no reverse build dependency exists
            print "\nCouldn't find any reverse build dependency in source repository.."

    if len(updatedPspecFiles + newPspecFiles):
        queue = []
        if os.path.exists(os.path.join(conf.workdir, "workQueue")):
            queue = open(os.path.join(conf.workdir, "workQueue"), "rb").read().strip().split("\n")

        queue.extend(updatedPspecFiles + newPspecFiles + revDepsToBeRecompiled)
        open(os.path.join(conf.workdir, "workQueue"), "wb").write("\n".join([l for l in list(set(queue)) if l])+"\n")

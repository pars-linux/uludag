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

import os
os.environ["LC_ALL"] = "C"

import sys
import copy
import shutil
import traceback
import cStringIO
import cPickle

import config
import logger
import mailer
import qmanager
import pisiinterface

from utils import *


def buildPackages():
    qmgr = qmanager.QueueManager()
    queue = copy.copy(qmgr.workQueue)
    packageList = []
    deltaPackageList = []

    if len(queue) == 0:
        logger.info("Work Queue is empty...")
        sys.exit(1)

    # FIXME: Use fcntl.flock
    f = open("/var/run/buildfarm", 'w')
    f.close()

    # Unpickle and load ISO package list here
    try:
        isopackages = cPickle.Unpickler(open("data/packages.db", "rb")).load()
    except:
        logger.error("You have to put packages.db in data/ for delta generation.")
        os.unlink("/var/run/buildfarm")
        sys.exit(1)

    # Compiling current workqueue

    # TODO: Determine the packages to be recompiled for ABI compatibility.
    # We have to parse all pspec.xml's in queue to search for a special <Requires>
    # tag in "latest" <Update> tags.

    logger.raw("QUEUE")
    logger.info("*** Work Queue: %s" % qmgr.workQueue)
    sortedQueue = qmgr.workQueue[:]
    sortedQueue.sort()
    mailer.info("*** I'm starting to compile following packages:\n\n%s" % "\n".join(sortedQueue))
    logger.raw()

    for pspec in queue:
        packagename = os.path.basename(os.path.dirname(pspec))
        build_output = open(os.path.join(config.outputDir, "%s.log" % packagename), "w")
        logger.raw()
        logger.info(
            "*** Compiling source %s (%d of %d)" %
                (
                    packagename,
                    int(queue.index(pspec) + 1),
                    len(queue)
                )
            )

        # This is here because farm captures the build output
        pisi = pisiinterface.PisiApi(stdout = build_output, stderr = build_output, outputDir = config.workDir)
        try:
            try:
                # Build source package
                # Returned values can also contain -dbginfo- packages.
                (newBinaryPackages, oldBinaryPackages) = pisi.build(pspec)

                # Reduce to filenames
                newBinaryPackages = map(lambda x: os.path.basename(x), newBinaryPackages)
                oldBinaryPackages = map(lambda x: os.path.basename(x), oldBinaryPackages)

                # Filter debug packages because we don't need to build delta packages
                # for debug packages
                newDebugPackages = [p for p in newBinaryPackages if isdebug(p)]
                oldDebugPackages = [p for p in oldBinaryPackages if isdebug(p)]

                #print "************* newDebugPackages: %s" % newDebugPackages
                #print "************* oldDebugPackages: %s" % oldDebugPackages

                newBinaryPackages = list(set(newBinaryPackages).difference(newDebugPackages))
                oldBinaryPackages = list(set(oldBinaryPackages).difference(oldDebugPackages))

                #print "************* newBinaryPackages: %s" % newBinaryPackages
                #print "************* oldBinaryPackages: %s" % oldBinaryPackages

                newBinaryPackages.sort()
                oldBinaryPackages.sort()

                # Delta package generation using delta interface
                (deltasToInstall, deltaPackages) = pisi.delta(isopackages, oldBinaryPackages, newBinaryPackages)

                # Reduce to filenames
                deltasToInstall = map(lambda x: os.path.basename(x), deltasToInstall)
                deltaPackages = map(lambda x: os.path.basename(x), deltaPackages)

                # If there exists incremental delta packages, install them.
                if deltasToInstall:
                    packagesToInstall = deltasToInstall[:]
                    if len(newBinaryPackages) > len(oldBinaryPackages):
                        logger.info("*** There are new binaries, the package is probably splitted.")

                        # There exists some first builds, install them because they don't have delta.
                        packagesToInstall.extend(newBinaryPackages[len(oldBinaryPackages):])
                        logger.debug("(splitted package), packagesToInstall: %s" % packagesToInstall)
                else:
                    # No delta, install full packages
                    packagesToInstall = newBinaryPackages[:]

                # Merge the package lists
                deltaPackages = deltaPackages + deltasToInstall
                logger.debug("All delta packages: %s" % deltaPackages)

            except Exception, e:
                # Transfer source package to wait queue in case of a build error
                qmgr.transferToWaitQueue(pspec)
                errmsg = "Error occured for '%s' in BUILD process:\n %s" % (pspec, e)
                logger.error(errmsg)
                mailer.error(errmsg, pspec)
            else:
                try:
                    # If there exists multiple packages, reorder them in order to
                    # correctly install interdependent packages.
                    if len(packagesToInstall) > 1:
                        # packagesToInstall doesn't contain full paths
                        logger.info("*** Reordering packages to satisfy inner runtime dependencies...")
                        packagesToInstall = pisi.getInstallOrder(packagesToInstall)
                        logger.info("*** Installation order is: %s" % packagesToInstall)

                    for p in packagesToInstall:
                        # Install package
                        logger.info("*** Installing: %s" % os.path.join(config.workDir, p))
                        pisi.install(os.path.join(config.workDir, p))
                except Exception, e:
                    # Transfer source package to wait queue in case of an install error
                    qmgr.transferToWaitQueue(pspec)

                    # FIXME: The packages before packagesToInstall[p] are already installed and therefore need to be
                    # uninstalled because p can't be installed.
                    errmsg = "Error occured for '%s' in INSTALL process: %s" % (os.path.join(config.workDir, p), e)
                    if isdelta(p):
                        logger.info("*** Probably %s was not installed on the system and the delta installation failed." % getName(p))
                    logger.error(errmsg)
                    mailer.error(errmsg, pspec)

                    # The package should be removed from the related lists and workdir
                    for pa in deltaPackages+newBinaryPackages:
                        if pa in deltasToInstall:
                            deltasToInstall.remove(pa)
                        else:
                            newBinaryPackages.remove(pa)
                        logger.info("*** (Cleanup) Removing %s from %s" % (pa, config.workDir))
                        removeBinaryPackageFromWorkDir(pa)
                else:
                    qmgr.removeFromWorkQueue(pspec)
                    movePackages(newBinaryPackages, oldBinaryPackages, deltaPackages, newDebugPackages)
                    packageList += (map(lambda x: os.path.basename(x), newBinaryPackages))
                    deltaPackageList += (map(lambda x: os.path.basename(x), deltaPackages))

        finally:
            pass

    logger.raw("QUEUE")
    logger.info("*** Wait Queue: %s" % (qmgr.waitQueue))
    if qmgr.waitQueue:
        mailer.info("Queue finished with problems and those packages couldn't be compiled:\n\n%s\n\n\nNew binary packages are;\n\n%s\n\nnow in repository" % ("\n".join(qmgr.waitQueue), "\n".join(packageList)))
    else:
        mailer.info("Queue finished without a problem!...\n\n\nNew binary packages are:\n\n%s\n\n"
                    "New delta packages are:\n\n%s\n\nnow in repository..." % ("\n".join(packageList), "\n".join(deltaPackageList)))
    logger.raw()
    logger.raw()

    # Save current path
    current = os.getcwd()
    for d in [config.binaryPath, config.testPath, config.debugPath]:
        os.chdir(d)
        logger.info("\n*** Generating PiSi Index in %s:" % d)
        os.system("/usr/bin/pisi index %s . --skip-signing --skip-sources" % config.localPspecRepo)
        logger.info("*** PiSi Index Generated for %s" % d)

    # Go back to the saved directory
    os.chdir(current)

    # Check packages containing binaries and libraries broken by any package update
    print "\n*** Checking binary consistency with revdep-rebuild.."
    os.system("/usr/bin/revdep-rebuild --force")

    # FIXME: Use fcntl.funlock
    os.unlink("/var/run/buildfarm")

def movePackages(newBinaryPackages, oldBinaryPackages, deltaPackages, debugPackages):

    def cleanupStaleDeltaPackages(package):
        # Say that 'package' is kernel-2.6.25.20-114.45.pisi
        # We can remove delta packages going to any build < 45 from both
        # packages/ and packages-test/ because we no longer need them.
        for p in getDeltasNotGoingTo(config.binaryPath, package):
            logger.info("*** Removing stale delta '%s' from '%s'" % (p, config.binaryPath))
            remove(join(config.binaryPath, p))

        for p in getDeltasNotGoingTo(config.testPath, package):
            logger.info("*** Removing stale delta '%s' from '%s'" % (p, config.testPath))
            remove(join(config.testPath, p))

    def removeOldPackage(package):
        logger.info("*** Removing old package '%s' from '%s'" % (package, config.testPath))
        if exists(join(config.testPath, package)):
            # If an old build is found in testPath
            # remove it because the test repo is unique.
            remove(join(config.testPath, package))

        # Cleanup workDir
        if exists(join(config.workDir, package)):
            remove(join(config.workDir, package))

    def moveNewPackage(package):
        logger.info("*** Moving new package '%s'" % package)
        if exists(join(config.workDir, package)):
            copy(join(config.workDir, package), config.binaryPath)
            copy(join(config.workDir, package), config.testPath)
            remove(join(config.workDir, package))

    def moveUnchangedPackage(package):
        logger.info("*** Moving unchanged package %s'" % package)
        if exists(join(config.workDir, package)):
            copy(join(config.workDir, package), config.binaryPath)
            remove(join(config.workDir, package))

    def moveDeltaPackage(package):
        # Move all delta packages into packages/ and packages-test/
        # and clean them from workDir.
        logger.info("*** Moving delta package '%s' to both directories" % package)
        if exists(join(config.workDir, package)):
            copy(join(config.workDir, package), config.binaryPath)
            copy(join(config.workDir, package), config.testPath)
            remove(join(config.workDir, package))

    def moveDebugPackage(package):
        # Move all debug packages into packages-debug/ and clean them
        # from WorkDir.
        logger.info("*** Moving debug package '%s' to packages-debug" % package)
        if exists(join(config.workDir, package)):
            copy(join(config.workDir, package), config.debugPath)
            remove(join(config.workDir, package))

    # Normalize files to full paths
    try:
        newBinaryPackages = set(map(lambda x: os.path.basename(x), newBinaryPackages))
    except AttributeError:
        pass

    try:
        oldBinaryPackages = set(map(lambda x: os.path.basename(x), oldBinaryPackages))
    except AttributeError:
        pass

    unchangedPackages = set(newBinaryPackages).intersection(set(oldBinaryPackages))
    newPackages = set(newBinaryPackages) - set(oldBinaryPackages)
    oldPackages = set(oldBinaryPackages) - set(unchangedPackages)

    logger.info("*** New binary package(s): %s" % newPackages)
    logger.info("*** Old binary package(s): %s" % oldPackages)
    logger.info("*** Unchanged binary package(s): %s" % unchangedPackages)
    logger.info("*** Delta package(s): %s" % deltaPackages)
    logger.info("*** Debug package(s): %s" % debugPackages)

    exists = os.path.exists
    join   = os.path.join
    remove = os.remove
    copy   = shutil.copy


    for package in newPackages:
        if package:
            # Move the new binary package to packages/ and packages-test/
            moveNewPackage(package)

    for package in oldPackages:
        if package:
            # Remove old binary package from packages-test/
            removeOldPackage(package)

    for package in unchangedPackages:
        if package:
            moveUnchangedPackage(package)

    for package in deltaPackages:
        # Move all(3) delta packages to packages/ and packages-test/
        if package:
            moveDeltaPackage(package)

    if deltaPackages:
        for package in newPackages:
            # Remove delta packages going to any build != newPackage's build
            if package:
                cleanupStaleDeltaPackages(package)

    if debugPackages:
        for package in debugPackages:
            # Move debug packages to packages-debug/
            if package:
                moveDebugPackage(package)



def removeBinaryPackageFromWorkDir(package):
    join   = os.path.join
    remove = os.remove
    remove(join(config.workDir, package))

def create_directories():
    directories = [config.workDir,
                   config.testPath,
                   config.binaryPath,
                   config.debugPath,
                   config.localPspecRepo,
                   config.outputDir]

    for d in directories:
        if d and not os.path.isdir(d):
            try:
                os.makedirs(d)
            except OSError:
                raise ("Directory '%s' cannot be created, permission problem?" % d)


def handle_exception(exception, value, tb):
    s = cStringIO.StringIO()
    traceback.print_tb(tb, file = s)
    s.seek(0)

    logger.error(str(exception))
    logger.error(str(value))
    logger.error(s.read())


if __name__ == "__main__":
    sys.excepthook = handle_exception
    create_directories()

    buildPackages()

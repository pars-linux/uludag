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

import os
import sys
import copy
import shutil
import traceback
import cStringIO
import exceptions
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
                (newBinaryPackages, oldBinaryPackages) = pisi.build(pspec)

                # Reduce to filenames
                newBinaryPackages = map(lambda x: os.path.basename(x), newBinaryPackages)
                oldBinaryPackages = map(lambda x: os.path.basename(x), oldBinaryPackages)
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
                        # There exists some first builds, install them
                        # because they dont have delta.
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
                    errmsg = "Error occured for '%s' in INSTALL process: %s" % (os.path.join(config.workDir, p), e)
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
                    movePackages(newBinaryPackages, oldBinaryPackages, deltasToInstall, deltaPackages)
                    packageList += (map(lambda x: os.path.basename(x), newBinaryPackages))
        finally:
            pass

    logger.raw("QUEUE")
    logger.info("*** Wait Queue: %s" % (qmgr.waitQueue))
    if qmgr.waitQueue:
        mailer.info("Queue finished with problems and those packages couldn't be compiled:\n\n%s\n\n\nNew binary packages are;\n\n%s\n\nnow in repository" % ("\n".join(qmgr.waitQueue), "\n".join(packageList)))
    else:
        mailer.info("Queue finished without a problem!...\n\n\nNew binary packages are;\n\n%s\n\nnow in repository..." % "\n".join(packageList))
    logger.raw()
    logger.raw()

    # Save current path
    current = os.getcwd()
    for dir in [config.binaryPath, config.testPath]:
        os.chdir(dir)
        logger.info("\n*** Generating PiSi Index in %s:" % dir)
        os.system("/usr/bin/pisi index %s . --skip-signing --skip-sources" % config.localPspecRepo)
        logger.info("*** PiSi Index Generated for %s" % dir)

    # Go back to the saved directory
    os.chdir(current)

    # Check packages containing binaries and libraries broken by any package update
    print "\n*** Checking binary consistency with revdep-rebuild.."
    os.system("/usr/bin/revdep-rebuild --force")

    # FIXME: Use fcntl.funlock
    os.unlink("/var/run/buildfarm")

def movePackages(newBinaryPackages, oldBinaryPackages, deltasToInstall, deltaPackages):

    def cleanupStaleDeltaPackages(package):
        # Say that 'package' is kernel-2.6.25.20-114.45.pisi
        # We can remove delta packages going to any build < 45 from both
        # packages/ and packages-test/ because we no longer need them.
        build = getBuild(package)
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



def removeBinaryPackageFromWorkDir(package):
    join   = os.path.join
    remove = os.remove
    remove(join(config.workDir, package))

def create_directories():
    directories = [config.workDir,
                   config.testPath,
                   config.binaryPath,
                   config.localPspecRepo,
                   config.outputDir]

    for dir in directories:
        if dir and not os.path.isdir(dir):
            try:
                os.makedirs(dir)
            except OSError:
                raise ("Directory '%s' cannot be created, permission problem?" % dir)


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

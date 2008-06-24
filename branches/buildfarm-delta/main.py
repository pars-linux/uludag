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

""" Standart Python Modules """
import os
import sys
import copy
import shutil
import traceback
import cStringIO
import exceptions
import cPickle
import glob

""" BuildFarm Modules """
import config
import logger
import mailer
import qmanager
import pisiinterface

""" Gettext Support """
import gettext
__trans = gettext.translation("buildfarm", fallback = True)
_  =  __trans.ugettext

def buildPackages():
    qmgr = qmanager.QueueManager()
    queue = copy.copy(qmgr.workQueue)
    packageList = []

    if len(queue) == 0:
        logger.info(_("Work Queue is empty..."))
        sys.exit(1)

    # FIXME: Use fcntl.flock
    f = open("/var/run/buildfarm", 'w')
    f.close()

    # Unpickle and load ISO package list here
    isopackages = cPickle.Unpickler(open("data/packages.db", "rb")).load()

    logger.raw(_("QUEUE"))
    logger.info(_("Work Queue: %s") % (qmgr.workQueue))
    sortedQueue = qmgr.workQueue[:]
    sortedQueue.sort()
    mailer.info(_("I'm starting to compile following packages:\n\n%s") % "\n".join(sortedQueue))
    logger.raw()

    for pspec in queue:
        packagename = os.path.basename(os.path.dirname(pspec))
        build_output = open(os.path.join(config.outputDir, "%s.log" % packagename), "w")
        logger.raw()
        logger.info(
            _("Compiling source %s (%d of %d)") % 
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
                (newBinaryPackages, oldBinaryPackages) = pisi.build(pspec)

                # Delta package generation using delta interface
                (deltasToInstall, deltaPackages) = pisi.delta(isopackages, oldBinaryPackages, newBinaryPackages)

                if deltasToInstall:
                    packagesToInstall = deltasToInstall
                else:
                    packagesToInstall = newBinaryPackages

                # Merge the package lists
                deltaPackages = deltaPackages + deltasToInstall

            except Exception, e:
                qmgr.transferToWaitQueue(pspec)
                errmsg = _("Error occured for '%s' in BUILD process:\n %s") % (pspec, e)
                logger.error(errmsg)
                mailer.error(errmsg, pspec)
            else:
                try:
                    for p in packagesToInstall:
                        logger.info("Installing: %s" % os.path.join(config.workDir, p))
                        pisi.install(os.path.join(config.workDir, p))
                except Exception, e:
                    qmgr.transferToWaitQueue(pspec)
                    errmsg = _("Error occured for '%s' in INSTALL process: %s") % (os.path.join(config.workDir, p), e)
                    logger.error(errmsg)
                    mailer.error(errmsg, pspec)

                    newBinaryPackages.remove(p)
                    removeBinaryPackageFromWorkDir(p)
                else:
                    qmgr.removeFromWorkQueue(pspec)
                    movePackages(newBinaryPackages, oldBinaryPackages, deltasToInstall, deltaPackages)
                    packageList += (map(lambda x: os.path.basename(x), newBinaryPackages))
        finally:
            pass

    logger.raw(_("QUEUE"))
    logger.info(_("Wait Queue: %s") % (qmgr.waitQueue))
    if qmgr.waitQueue:
        mailer.info(_("Queue finished with problems and those packages couldn't be compiled:\n\n%s\n\n\nNew binary packages are;\n\n%s\n\nnow in repository") % ("\n".join(qmgr.waitQueue), "\n".join(packageList)))
    else:
        mailer.info(_("Queue finished without a problem!...\n\n\nNew binary packages are;\n\n%s\n\nnow in repository...") % "\n".join(packageList))
    logger.raw()
    logger.raw()

    # Check packages containing binaries and libraries broken by any package update
    print "\nChecking binary consistency with revdep-rebuild.."
    os.system("/usr/bin/revdep-rebuild --force")

    # Save current path
    current = os.getcwd()

    for dir in [config.binaryPath, config.testPath]:
        os.chdir(dir)
        logger.info(_("\nGenerating PiSi Index in %s:" % dir))
        os.system("/usr/bin/pisi index %s . --skip-signing --skip-sources" % config.localPspecRepo)
        logger.info(_("PiSi Index Generated for %s" % dir))

        # Sweeet november, try to find duplicate packages in dir
        # print "\nDuplicate packages in %s:\n%s" % (dir, '-'*40)
        # os.system("for i in `ls`; do echo ${i/-[0-9]*/}; done | uniq -d")

    # Go back to the saved directory
    os.chdir(current)

    # FIXME: Use fcntl.funlock
    os.unlink("/var/run/buildfarm")

def movePackages(newBinaryPackages, oldBinaryPackages, deltasToInstall, deltaPackages):
    # normalize files to full paths
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

    logger.info(_("*** New binary package(s): %s") % newPackages)
    logger.info(_("*** Old binary package(s): %s") % oldPackages)
    logger.info(_("*** Unchanged binary package(s): %s") % unchangedPackages)
    logger.info(_("*** Delta package(s): %s") % deltaPackages)

    exists = os.path.exists
    join   = os.path.join
    remove = os.remove
    copy   = shutil.copy

    def moveOldPackage(package):
        logger.info(_("*** Removing old package '%s' from %s") % (package, config.testPath))
        if exists(join(config.testPath, package)):
            # If an old build is found in testPath(/packages-test/)
            # remove it because the test repo is unique.
            remove(join(config.testPath, package))

        # Cleanup workDir
        if exists(join(config.workDir, package)):
            remove(join(config.workDir, package))

    def moveNewPackage(package):
        logger.info(_("*** Moving new package '%s'") % (package))
        if exists(join(config.workDir, package)):
            # binaryPath : /var/cache/pisi/packages/
            # testPath : /var/cache/pisi/packages-test/
            copy(join(config.workDir, package), config.binaryPath)
            copy(join(config.workDir, package), config.testPath)
            remove(join(config.workDir, package))

    def moveUnchangedPackage(package):
        logger.info(_("*** Moving unchanged package %s'") % (package))
        if exists(join(config.workDir, package)):
            copy(join(config.workDir, package), config.binaryPath)
            remove(join(config.workDir, package))

    def moveDeltaPackage(package):
        # Move all delta packages into binary path and clean them from workDir
        logger.info(_("*** Moving delta package '%s' to %s") % (package, config.binaryPath))
        if exists(join(config.workDir, package)):
            copy(join(config.workDir, package), config.binaryPath)
            remove(join(config.workDir, package))

    def moveIncrementalDeltaPackage(package):
        # Move incremental delta packages to the test repository.
        # e.g. kernel-88-89-delta.pisi
        for p in glob.glob1(config.testPath, "%s-[0-9]*-[0-9]*.delta.pisi" % os.path.basename(package).rsplit("-", 2)[0]):
            logger.info(_("*** Removing %s from %s" % (p, config.testPath)))
            remove(join(config.testPath, p))

        logger.info(_("*** Moving incremental delta package '%s' to %s") % (package, config.testPath))
        if exists(join(config.workDir, package)):
            copy(join(config.workDir, package), config.testPath)

    for package in newPackages:
        if package:
            moveNewPackage(package)

    for package in oldPackages:
        if package:
            moveOldPackage(package)

    for package in unchangedPackages:
        if package:
            moveUnchangedPackage(package)

    for package in deltasToInstall:
        if package:
            moveIncrementalDeltaPackage(package)

    for package in deltaPackages:
        if package:
            moveDeltaPackage(package)

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
                raise _("Directory '%s' cannot be created, permission problem?") % dir


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

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
import copy
import shutil
import traceback
import cStringIO
import exceptions

""" BuildFarm Modules """
import config
import logger
import mailer
import qmanager
import pisiinterface
import pisi.util

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

    logger.raw(_("QUEUE"))
    logger.info(_("Work Queue: %s") % (qmgr.workQueue))
    sortedQueue = qmgr.workQueue[:]
    sortedQueue.sort()
    mailer.info(_("I'm starting to compile following packages:\n\n%s") % "\n".join(sortedQueue))
    logger.raw()

    for pspec in queue:
        packagename = os.path.basename(os.path.dirname(pspec))
        build_output = open(os.path.join(config.outputDir, "%s.log" % packagename), "w")
        logger.info(
            _("Compiling source %s (%d of %d)") % 
                (
                    packagename,
                    int(queue.index(pspec) + 1),
                    len(queue)
                )
            )
        logger.raw()

        # This is here because farm captures the build output
        pisi = pisiinterface.PisiApi(stdout = build_output, stderr = build_output, outputDir = config.workDir)
        try:
            try:
                (newBinaryPackages, oldBinaryPackages) = pisi.build(pspec)
                print
                print newBinaryPackages, oldBinaryPackages
                print
            except Exception, e:
                qmgr.transferToWaitQueue(pspec)
                errmsg = _("Error occured for '%s' in BUILD process:\n %s") % (pspec, e)
                logger.error(errmsg)
                mailer.error(errmsg, pspec)
            else:
                try:
                    for p in newBinaryPackages:
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
                    movePackages(newBinaryPackages, oldBinaryPackages)
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

    generateIndex(config.binaryPath)
    generateIndex(config.binaryDebugPath)

def generateIndex(repositoryPath = config.binaryPath):
    logger.raw()
    logger.info(_("Generating PiSi Index..."))

    current = os.getcwd()
    os.chdir(repositoryPath)
    os.system("/usr/bin/pisi index %s . --skip-signing --skip-sources" % config.localPspecRepo)
    logger.info(_("PiSi Index generated..."))

    # Check packages containing binaries and libraries broken by any package update
    os.system("/usr/bin/revdep-rebuild --force")
    # FIXME: if there is any broken package,  mail /root/.revdep-rebuild.4_names file

    # Sweeet november, try to find duplicate packages in config.binaryPath
    os.system("for i in `ls`; do echo ${i/-[0-9]*/}; done | uniq -d")

    os.chdir(current)

    # FIXME: Use fcntl.funlock
    os.unlink("/var/run/buildfarm")

def movePackages(newBinaryPackages, oldBinaryPackages):
    # sanitaze input
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

    exists = os.path.exists
    join   = os.path.join
    remove = os.remove
    copy   = shutil.copy

    def moveOldPackage(package, debug = False):
        logger.info(_("*** Old package '%s' is processing") % (package))
        if exists(join(config.binaryPath, package)):
            if debug:
                remove(join(config.binaryDebugPath, package))
            else:
                remove(join(config.binaryPath, package))

        if exists(join(config.workDir, package)):
            remove(join(config.workDir, package))

    def moveNewPackage(package, debug = False):
        logger.info(_("*** New package '%s' is processing") % (package))
        if exists(join(config.workDir, package)):
            if debug:
                copy(join(config.workDir, package), config.binaryDebugPath)
            else:
                copy(join(config.workDir, package), config.binaryPath)
            remove(join(config.workDir, package))

    def moveUnchangedPackage(package, debug = False):
        logger.info(_("*** Unchanged package '%s' is processing") % (package))
        if exists(join(config.workDir, package)):
            if debug:
                copy(join(config.workDir, package), config.binaryDebugPath)
            else:
                copy(join(config.workDir, package), config.binaryPath)
            remove(join(config.workDir, package))

    for package in newPackages:
        if package:
            isDebug = (pisi.util.parse_package_name(package)[0]).endswith("-debug")
            moveNewPackage(package, isDebug)

    for package in oldPackages:
        if package:
            isDebug = (pisi.util.parse_package_name(package)[0]).endswith("-debug")
            moveOldPackage(package, isDebug)

    for package in unchangedPackages:
        if package:
            isDebug = (pisi.util.parse_package_name(package)[0]).endswith("-debug")
            moveUnchangedPackage(package, isDebug)

def removeBinaryPackageFromWorkDir(package):
    join   = os.path.join
    remove = os.remove
    remove(join(config.workDir, package))

def create_directories():
    directories = [config.workDir,
                   config.binaryPath,
                   config.binaryDebugPath,
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

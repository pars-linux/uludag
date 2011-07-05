#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006,2007 TUBITAK/UEKAE
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

from shutil import copy as shutilCopy
from copy import copy as shallowCopy

""" BuildFarm Modules """
import config
import dependency
import logger
import mailer

""" Helpers """
from helpers import pisiinterface
from comar.utility import FileLock

""" Gettext Support """
import gettext
__trans = gettext.translation("buildfarm", fallback = True)
_  =  __trans.ugettext

class QueueManager:

    def __init__(self):

        self.locks = {"waitQueue" : FileLock("%s/.waitqueue.lock" % config.workDir),
                      "workQueue" : FileLock("%s/.workqueue.lock" % config.workDir),
                      "build"     : FileLock("%s/.build.lock" % config.workDir)}

        self.workQueue = []
        self.waitQueue = []

        self.__checkQueues__()

    def __del__(self):
        self.__serialize__(self.waitQueue, "waitQueue")
        self.__serialize__(self.workQueue, "workQueue")

    def __checkQueues__(self):
        # If waitQueue contains some packages, this method
        # moves them to the workQueue and calls dependency resolver on it.
        self.__deserialize__(self.workQueue, "workQueue")
        self.__deserialize__(self.waitQueue, "waitQueue")

        if len(self.waitQueue):
            self.workQueue += self.waitQueue
            self.waitQueue = []

        self.workQueue = dependency.DependencyResolver(self.workQueue).resolveDependencies()
        self.__del__()

    def __serialize__(self, queueName, fileName):
        self.locks[fileName].lock()
        try:
            queue = open(os.path.join(config.workDir, fileName), "w")
        except IOError:
            self.locks[fileName].unlock()
            return

        for pspec in queueName:
            queue.write("%s\n" % pspec)
        queue.close()
        self.locks[fileName].unlock()

    def __deserialize__(self, queueName, fileName):
        self.locks[fileName].lock()
        try:
            queue = open(os.path.join(config.workDir, fileName), "r")
        except IOError:
            self.locks[fileName].unlock()
            return

        for line in queue.readlines():
            if not line.startswith("#"):
                queueName.append(line.strip("\n"))
        queue.close()
        self.locks[fileName].unlock()

    def __initWorkQueueFromFile__(self):
        self.workQueue = []
        self.__deserialize__(self.workQueue, "workQueue")

    def __initWaitQueueFromFile__(self):
        self.waitQueue = []
        self.__deserialize__(self.waitQueue, "waitQueue")

    def __tryToLock__(self, depth):
        # find the caller info
        # if the request to this function from stack depth 'depth'
        # is coming from the xmlrpc client, the method will try to acquire
        # the lock and raise exception if unsuccessful.
        #
        # 0: Acquired the lock (Must release it in the caller)
        # 1: Can't acquire the lock
        # 2: Don't need to acquire the lock (Method is called from this module)
        f = sys._getframe(depth)
        methodName = f.f_code.co_name
        if methodName == "_dispatch":
            try:
                self.locks["build"].lock(timeout=0)
                return 0
            except:
                return 1
        return 2

    # Getter functions can't brake the integrity of the queues.
    def getWorkQueue(self):
        self.__initWorkQueueFromFile__()
        return self.workQueue

    def getWaitQueue(self):
        self.__initWaitQueueFromFile__()
        return self.waitQueue

    def removeFromWaitQueue(self, pspec):
        lock = self.__tryToLock__(2)
        if lock == 1:
            return 1
        self.__initWaitQueueFromFile__()
        if self.waitQueue.__contains__(pspec):
            self.waitQueue.remove(pspec)
            self.__serialize__(self.waitQueue, "waitQueue")
            if lock == 0:
                self.locks['build'].unlock()
            return 0
        if lock == 0:
            self.locks['build'].unlock()
        return 2

    def removeFromWorkQueue(self, pspec):
        lock = self.__tryToLock__(2)
        if lock == 1:
            return 1
        self.__initWorkQueueFromFile__()
        if self.workQueue.__contains__(pspec):
            self.workQueue.remove(pspec)
            self.__serialize__(self.workQueue, "workQueue")
            if lock == 0:
                self.locks['build'].unlock()
            return 0
        if lock == 0:
            self.locks['build'].unlock()
        return 2

    def appendToWorkQueue(self, pspec, checkIfExists=False):
        # 0: Successful
        # 1: Buildfarm is busy
        # 2: Package doesn't exist
        # 3: Package is already in the queue
        lock = self.__tryToLock__(2)
        if lock == 1:
            return 1
        if checkIfExists:
            if not os.path.isfile(os.path.join(config.localPspecRepo, pspec)):
                self.locks['build'].unlock()
                return 2

        self.__initWorkQueueFromFile__()
        if not self.workQueue.__contains__(pspec):
            self.workQueue.append(pspec)
            self.__serialize__(self.workQueue, "workQueue")
            if lock == 0:
                self.locks['build'].unlock()
            return 0
        if lock == 0:
            self.locks['build'].unlock()
        return 3

    # Can't be invoked from clients so doesn't need introspection.
    def appendToWaitQueue(self, pspec):
        self.__initWaitQueueFromFile__()
        if not self.waitQueue.__contains__(pspec):
            self.waitQueue.append(pspec)
            self.__serialize__(self.waitQueue, "waitQueue")
            return True
        return False

    def transferToWorkQueue(self, pspec):
        lock = self.__tryToLock__(2)
        if lock == 1:
            return 1
        self.__initWaitQueueFromFile__()
        if self.waitQueue.__contains__(pspec) and self.appendToWorkQueue(pspec):
            self.removeFromWaitQueue(pspec)
            return 0
        return 2

    def transferToWaitQueue(self, pspec):
        lock = self.__tryToLock__(2)
        if lock == 1:
            return 1
        self.__initWorkQueueFromFile__()
        if self.workQueue.__contains__(pspec) and self.appendToWaitQueue(pspec):
            self.removeFromWorkQueue(pspec)
            if lock == 0:
                self.locks['build'].unlock()
            return 0
        if lock == 0:
            self.locks['build'].unlock()
        return 2

    def buildArchive(self, dirname, filename, d, username=""):

        def extractArchive(filename, d):
            from subprocess import call
            dir = os.path.join(config.remoteWorkDir, username)
            if not os.path.exists(dir):
                os.mkdir(dir)
            os.chdir(dir)
            f = open(filename, "wb")
            f.write(d.data)
            f.close()

            return call(["tar", "xvjf", filename])

        # Returns 0 if successful
        print extractArchive(filename, d)
        getPspecList(dirname)

        return True

    def buildPackages(self):
        # Return values are interpreted by the client
        # 0: Successful
        # 1: Buildfarm is busy
        # 2: Empty work queue
        # 3: Finished with errors

        try:
            self.locks["build"].lock(timeout=0)
        except:
            return 1

        sys.excepthook = self.__handle_exception__

        self.__checkQueues__()
        queue = shallowCopy(self.getWorkQueue())

        if len(queue) == 0:
            logger.info(_("Work queue is empty..."))
            self.locks["build"].unlock()
            return 2

        logger.raw(_("QUEUE"))
        logger.info(_("Work Queue: %s") % (queue))
        sortedQueue = queue[:]
        sortedQueue.sort()
        # mailer.info(_("I'm starting to compile following packages:\n\n%s") % "\n".join(sortedQueue))
        logger.raw()

        for pspec in queue:
            # Gets the packagename, creates a log file
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

            # Initialise PiSi API
            pisi = pisiinterface.PisiApi(config.workDir)
            pisi.init(stdout = build_output, stderr = build_output)
            try:
                try:
                    # Builds pspec and returns a tuple containing 2 lists
                    # that contains new and old package names
                    # e.g. newBinaryPackages=['package-1-2-1.pisi']
                    (newBinaryPackages, oldBinaryPackages) = pisi.build(pspec)

                    # Delta package generation
                    deltaPackages = []
                    if oldBinaryPackages:
                        deltaPackages = pisi.delta(oldBinaryPackages, newBinaryPackages)
                        packagesToInstall = deltaPackages[:]
                    else:
                        packagesToInstall = list(newBinaryPackages)

                    logger.info("packagesToInstall[]: %s" % packagesToInstall)

                except Exception, e:
                    # Build Error
                    # Transfers the pspec to the wait queue and logs the error
                    self.transferToWaitQueue(pspec)
                    errmsg = _("Error occured for '%s' in BUILD process:\n %s") % (pspec, e)
                    logger.error(errmsg)
                    # mailer.error(errmsg, pspec)
                else:
                    try:
                        for p in packagesToInstall:
                            # For every new binary package generated, this snippet
                            # installs them on the system.
                            # TODO: Install delta packages here
                            logger.info(_("Installing: %s" % os.path.join(config.workDir, p)))
                            pisi.install(os.path.join(config.workDir, p))
                    except Exception, e:
                        self.transferToWaitQueue(pspec)
                        errmsg = _("Error occured for '%s' in INSTALL process: %s") % (os.path.join(config.workDir, p), e)
                        logger.error(errmsg)
                        # mailer.error(errmsg, pspec)
                        newBinaryPackages.remove(p)
                        self.__removeBinaryPackageFromWorkDir__(p)
                    else:
                        self.removeFromWorkQueue(pspec)

                        # Move the packages
                        self.__movePackages__(newBinaryPackages, oldBinaryPackages, deltaPackages)
            finally:
                pisi.finalize()

        logger.raw(_("QUEUE"))
        logger.info(_("Wait Queue: %s") % (self.getWaitQueue()))
        logger.info(_("Work Queue: %s") % (self.getWorkQueue()))

        if self.getWaitQueue():
            # mailer.info(_("Queue finished with problems and those packages couldn't be compiled:\n\n%s\n") % "\n".join(self.getWaitQueue()))
            self.locks["build"].unlock()
            return 3
        else:
            self.locks["build"].unlock()
            # mailer.info(_("Queue finished without a problem!..."))
            return 0

    def buildIndex(self):

        try:
            self.locks["build"].lock(timeout=0)
        except:
            return 1

        logger.raw()
        logger.info(_("Generating PiSi Index..."))

        current = os.getcwd()
        os.chdir(config.binaryPath)
        os.system("/usr/bin/pisi index %s %s --skip-signing --skip-sources" % (config.localPspecRepo, config.binaryPath))
        logger.info(_("PiSi Index generated..."))

        #FIXME: will be enabled after some internal tests
        #os.system("rsync -avze ssh --delete . pisi.pardus.org.tr:/var/www/paketler.uludag.org.tr/htdocs/pardus-1.1/")

        # Check packages containing binaries and libraries broken by any package update
        os.system("/usr/bin/revdep-rebuild --force")
        # FIXME: if there is any broken package,  mail /root/.revdep-rebuild.4_names file

        os.chdir(current)

        # FIXME: handle indexing errors

        self.locks["build"].unlock()
        return 0

    def __movePackages__(self, newBinaryPackages, oldBinaryPackages, deltaPackages):

        exists = os.path.exists
        join   = os.path.join
        remove = os.remove
        copy   = shutilCopy

        def __moveOldPackage__(self, package):
            logger.info(_("*** Old package '%s' is processing") % (package))
            if exists(join(config.binaryPath, package)):
                remove(join(config.binaryPath, package))

            if exists(join(config.workDir, package)):
                remove(join(config.workDir, package))

        def __moveNewPackage__(self, package):
            logger.info(_("*** New package '%s' is processing") % (package))
            if exists(join(config.workDir, package)):
                copy(join(config.workDir, package), config.binaryPath)
                remove(join(config.workDir, package))

        def __moveUnchangedPackage__(self, package):
            logger.info(_("*** Unchanged package '%s' is processing") % (package))
            if exists(join(config.workDir, package)):
                copy(join(config.workDir, package), config.binaryPath)
                remove(join(config.workDir, package))

        def __moveDeltaPackage__(self, package):
            logger.info(_("*** Delta package '%s' is processing") % (package))
            if exists(package):
                copy(package, config.deltaPath)
                remove(package)

        unchangedPackages = set(newBinaryPackages).intersection(set(oldBinaryPackages))
        newPackages = set(newBinaryPackages) - set(oldBinaryPackages)
        oldPackages = set(oldBinaryPackages) - set(unchangedPackages)

        logger.info(_("*** New binary package(s): %s") % newPackages)
        logger.info(_("*** Old binary package(s): %s") % oldPackages)
        logger.info(_("*** Unchanged binary package(s): %s") % unchangedPackages)
        logger.info(_("*** Delta package(s) : %s") % deltaPackages)

        for package in newPackages:
            if package:
                __moveNewPackage__(self, package)

        for package in oldPackages:
            if package:
                __moveOldPackage__(self, package)

        for package in unchangedPackages:
            if package:
                __moveUnchangedPackage__(self, package)

        for package in deltaPackages:
            if package:
                __moveDeltaPackage__(self, package)

    def __removeBinaryPackageFromWorkDir__(self, package):
        os.remove(os.path.join(config.workDir, package))

    def __handle_exception__(self, exception, value, tb):
        s = cStringIO.StringIO()
        traceback.print_tb(tb, file = s)
        s.seek(0)

        logger.error(str(exception))
        logger.error(str(value))
        logger.error(s.read())


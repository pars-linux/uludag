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

""" Gettext Support """
import gettext
__trans = gettext.translation("buildfarm", fallback = True)
_  =  __trans.ugettext

class QueueManager:
    def __init__(self):
        self.workQueue = []
        self.waitQueue = []

        self.__deserialize__(self.workQueue, "workQueue")
        self.__deserialize__(self.waitQueue, "waitQueue")

        if len(self.waitQueue):
            self.workQueue += self.waitQueue
            self.waitQueue = []
        else:
            self.waitQueue = dependency.DependencyResolver(self.waitQueue).resolvDependencies()

        self.workQueue = dependency.DependencyResolver(self.workQueue).resolvDependencies()
        self.__serialize__(self.waitQueue, "waitQueue")
        self.__serialize__(self.workQueue, "workQueue")
        
    def __del__(self):
        self.__serialize__(self.waitQueue, "waitQueue")
        self.__serialize__(self.workQueue, "workQueue")

    def __serialize__(self, queueName, fileName):
        try:
            queue = open(os.path.join(config.workDir, fileName), "w")
        except IOError:
            return

        for pspec in queueName:
            queue.write("%s\n" % pspec)
        queue.close()

    def __deserialize__(self, queueName, fileName):
        try:
            queue = open(os.path.join(config.workDir, fileName), "r")
        except IOError:
            return

        for line in queue.readlines():
            if not line.startswith("#"):
                queueName.append(line.strip("\n"))
        queue.close()
    
    def __initWorkQueueFromFile__(self):
        self.workQueue = []
        self.__deserialize__(self.workQueue, "workQueue")
        
    def __initWaitQueueFromFile__(self):
        self.waitQueue = []
        self.__deserialize__(self.waitQueue, "waitQueue")

    def getWorkQueue(self):
        self.__initWorkQueueFromFile__()
        return self.workQueue

    def getWaitQueue(self):
        self.__initWaitQueueFromFile__()
        return self.waitQueue

    def removeFromWaitQueue(self, pspec):
        self.__initWaitQueueFromFile__()
        if self.waitQueue.__contains__(pspec):
            self.waitQueue.remove(pspec)
            self.__serialize__(self.waitQueue, "waitQueue")
            return True
        return False

    def removeFromWorkQueue(self, pspec):
        self.__initWorkQueueFromFile__()
        if self.workQueue.__contains__(pspec):
            self.workQueue.remove(pspec)
            self.__serialize__(self.workQueue, "workQueue")
            return True
        return False

    def appendToWorkQueue(self, pspec):
        self.__initWorkQueueFromFile__()
        if not self.workQueue.__contains__(pspec):
            self.workQueue.append(pspec)
            self.__serialize__(self.workQueue, "workQueue")
            return True
        return False

    def appendToWaitQueue(self, pspec):
        self.__initWaitQueueFromFile__()
        if not self.waitQueue.__contains__(pspec):
            self.waitQueue.append(pspec)
            self.__serialize__(self.waitQueue, "waitQueue")
            return True
        return False

    def transferToWorkQueue(self, pspec):
        if self.appendToWorkQueue(pspec):
            self.removeFromWaitQueue(pspec)
            return True
        return False

    def transferToWaitQueue(self, pspec):
        if self.appendToWaitQueue(pspec):
            self.removeFromWorkQueue(pspec)
            return True
        return False
    
    def buildPackages(self):
        
        sys.excepthook = self.__handle_exception__
        
        def createDirectories():
            directories = [config.workDir,
                           config.binaryPath,
                           config.localPspecRepo,
                           config.outputDir]

            for dir in directories:
                if dir and not os.path.isdir(dir):
                    try:
                        os.makedirs(dir)
                    except OSError:
                        raise _("Directory '%s' cannot be created, permission problem?") % dir
        
        # Make sure that directories exists.
        createDirectories()

        queue = shallowCopy(self.getWorkQueue())
    
        if len(queue) == 0:
            logger.info(_("Both Wait and Work Queues are empty..."))
            return True
    
        logger.raw(_("QUEUE"))
        logger.info(_("Work Queue: %s") % (self.getWorkQueue()))
        sortedQueue = self.getWorkQueue()[:]
        sortedQueue.sort()
        # mailer.info(_("I'm starting to compile following packages:\n\n%s") % "\n".join(sortedQueue))
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
    
            pisi = pisiinterface.PisiApi(config.workDir)
            pisi.init(stdout = build_output, stderr = build_output)
            try:
                try:
                    (newBinaryPackages, oldBinaryPackages) = pisi.build(pspec)
                except Exception, e:
                    self.transferToWaitQueue(pspec)
                    errmsg = _("Error occured for '%s' in BUILD process:\n %s") % (pspec, e)
                    logger.error(errmsg)
                    # mailer.error(errmsg, pspec)
                else:
                    try:
                        for p in newBinaryPackages:
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
                        self.__movePackages__(newBinaryPackages, oldBinaryPackages)
            finally:
                pisi.finalize()
    
        logger.raw(_("QUEUE"))
        logger.info(_("Wait Queue: %s") % (self.getWaitQueue()))
        logger.info(_("Work Queue: %s") % (self.getWorkQueue()))
    
        if self.getWaitQueue():
            # mailer.info(_("Queue finished with problems and those packages couldn't be compiled:\n\n%s\n") % "\n".join(qmgr.getWaitQueue()))
            return self.getWaitQueue()
        else:
            # mailer.info(_("Queue finished without a problem!..."))
            pass
        return True
    
    def buildIndex(self):
        logger.raw()
        logger.info(_("Generating PiSi Index..."))
    
        current = os.getcwd()
        os.chdir(config.binaryPath)
        os.system("/usr/bin/pisi index %s . --skip-signing --skip-sources" % config.localPspecRepo)
        logger.info(_("PiSi Index generated..."))
    
        #FIXME: will be enabled after some internal tests
        #os.system("rsync -avze ssh --delete . pisi.pardus.org.tr:/var/www/paketler.uludag.org.tr/htdocs/pardus-1.1/")
    
        # Check packages containing binaries and libraries broken by any package update
        os.system("/usr/bin/revdep-rebuild --force")
        # FIXME: if there is any broken package,  mail /root/.revdep-rebuild.4_names file
    
        os.chdir(current)
    
        # FIXME: handle indexing errors
        return True
    
    def __movePackages__(self, newBinaryPackages, oldBinaryPackages):
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
    
        for package in newPackages:
            if package:
                __moveNewPackage__(self, package)
    
        for package in oldPackages:
            if package:
                __moveOldPackage__(self, package)
    
        for package in unchangedPackages:
            if package:
                __moveUnchangedPackage__(self, package)
    
    def __removeBinaryPackageFromWorkDir__(self, package):
        join   = os.path.join
        remove = os.remove
        remove(join(config.workDir, package))
    
    def __handle_exception__(self, exception, value, tb):
        s = cStringIO.StringIO()
        traceback.print_tb(tb, file = s)
        s.seek(0)
    
        logger.error(str(exception))
        logger.error(str(value))
        logger.error(s.read())


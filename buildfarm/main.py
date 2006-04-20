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
import copy
import sys
import shutil
import traceback
import exceptions
import cStringIO

sys.path.append(".")
sys.path.append("..")

""" BuildFarm Modules """
import buildfarm.config as config
import buildfarm.logger as logger
import buildfarm.mailer as mailer
import buildfarm.qmanager as qmanager
import buildfarm.pisiinterface as pisiinterface


def main():
    qmgr = qmanager.QueueManager()
    queue = copy.copy(qmgr.workQueue)
    
    logger.raw("QUEUE")
    logger.info("Work Queue: %s" % (qmgr.workQueue))
    logger.raw()
    
    for pspec in queue: 
        packagename=os.path.basename(os.path.dirname(pspec))
        build_output=open(os.path.join(config.outputDir,packagename+".log"), "w")
        logger.info("Compiling source %s (%d of %d)" % (packagename,
                                                        int(queue.index(pspec) + 1),
                                                        len(queue)))
        logger.raw()

        pisi = pisiinterface.PisiApi()
        pisi.init(stdout=build_output, stderr=build_output)
        try:
            (newBinaryPackages, oldBinaryPackages) = pisi.build(pspec)
        except Exception, e:
            qmgr.transferToWaitQueue(pspec)
            errmsg = "'%s' için BUILD işlemi sırasında hata: %s" % (pspec, e)
            logger.error(errmsg)
            mailer.error(errmsg, pspec)
            pisi.finalize()
        else:
            for p in newBinaryPackages:
                logger.info("Installing: %s" % os.path.join(config.workDir, p))
                try:
                    pisi.install(os.path.join(config.workDir, p))
                except Exception, e:
                    logger.error("'%s' için INSTALL işlemi sırasında hata: %s" % (os.path.join(config.workDir, p), e))
                    qmgr.transferToWaitQueue(pspec)
                    newBinaryPackages.remove(p)
                    removeBinaryPackageFromWorkDir(p)
                else:
                    qmgr.removeFromWorkQueue(pspec)
            pisi.finalize()
            movePackages(newBinaryPackages, oldBinaryPackages)
    
    logger.raw("QUEUE")
    logger.info("Wait Queue: %s" % (qmgr.waitQueue))
    logger.raw()
    
    
def movePackages(newBinaryPackages, oldBinaryPackages):
    logger.info("*** Yeni ikili paket(ler): %s" % newBinaryPackages)
    logger.info("*** Eski ikili paket(ler): %s" % oldBinaryPackages)

    exists = os.path.exists
    join   = os.path.join
    remove = os.remove
    copy   = shutil.copy

    def moveOldPackage(package):
        logger.info("*** Eski paket '%s' işleniyor" % (package))
        if exists(join(config.oldBinaryPPath, package)):
            remove(join(config.oldBinaryPPath, package))
        if  exists(join(config.newBinaryPPath, package)):
            remove(join(config.newBinaryPPath, package))
        if exists(join(config.workDir, package)):
            remove(join(config.workDir, package))

    def moveNewPackage(package):
        logger.info("*** Yeni paket '%s' işleniyor" % (package))
        copy(join(config.workDir, package), config.newBinaryPPath)
        remove(join(config.workDir, package))
       
    def moveUnchangedPackage(package):
        logger.info("*** Değişmemiş paket '%s' işleniyor" % (package))
        if exists(join(config.newBinaryPPath, package)):
            remove(join(config.newBinaryPPath, package))
        if exists(join(config.oldBinaryPPath, package)):
            remove(join(config.workDir, package))
        else:
            copy(join(config.workDir, package), config.oldBinaryPPath)
            remove(join(config.workDir, package))
            
            
    if set(newBinaryPackages) == set(oldBinaryPackages):
        map(moveUnchangedPackage,
            [package for package in newBinaryPackages])
    else:
        map(moveNewPackage,
            [package for package in set(newBinaryPackages) - set(oldBinaryPackages)])
        map(moveOldPackage,
            [package for package in set(oldBinaryPackages) - (set(newBinaryPackages) - set(oldBinaryPackages)) if package])


def removeBinaryPackageFromWorkDir(package):
    join   = os.path.join
    remove = os.remove
    remove(join(config.workDir, package))
    

def create_directories():
    directories = [config.workDir, config.newBinaryPPath,
                   config.oldBinaryPPath, config.localPspecRepo,
                   config.outputDir]
    for dir in directories:
        if dir and not os.path.isdir(dir):
            try:
                os.makedirs(dir)
            except OSError:
                raise config.CfgError("'%s' dizini yaratılamadı, izin sorunu olabilir" % (dir))


def handle_exception(exception, value, tb):
    s = cStringIO.StringIO()
    traceback.print_tb(tb, file=s)
    s.seek(0)

    logger.error(str(exception))
    logger.error(str(value))
    logger.error(s.read())
    

if __name__ == "__main__":
    sys.excepthook = handle_exception
    create_directories()
    main()


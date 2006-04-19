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
    logger.info("Depo guncelleniyor (%s)." % config.localPspecRepo)
    
    qmgr = qmanager.QueueManager()
   
    queue = copy.copy(qmgr.workQueue)
    
    logger.raw("QUEUE")
    logger.info("Work Queue: %s" % (qmgr.workQueue))
    logger.raw()
    
    for pspec in queue: 
        logger.info("Compiling (%d of %d)" % (int(queue.index(pspec) + 1), len(queue)))
        logger.raw()
        packagename=os.path.basename(os.path.dirname(pspec))
        try:
            pisi = pisiinterface.PisiApi()
            build_output=open(os.path.join(config.workDir, packagename+".output"), "w")
            pisi.init(stdout=build_output, stderr=build_output)
            (newBinaryPackages, oldBinaryPackages) = pisi.build(pspec)
        except Exception, e:
            qmgr.transferToWaitQueue(pspec)
            errmsg = "'%s' için BUILD işlemi sırasında hata: %s" % (pspec, e)
            logger.error(errmsg)
            mailer.error(errmsg, pspec)
            pisi.finalize()
        else:
            for p in newBinaryPackages:
                try:
                    logger.info("Installing: %s" % os.path.join(config.workDir, p))
                    pisi.install(os.path.join(config.workDir, p))
                except Exception, e:
                    print "HATA: %s" % e
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
        map(lambda package: moveUnchangedPackage(package), [package for package in newBinaryPackages])
    else:
        map(lambda package: moveNewPackage(package), [package for package in set(newBinaryPackages) - set(oldBinaryPackages)])
        map(lambda package: moveOldPackage(package), [package for package in set(oldBinaryPackages) - (set(newBinaryPackages) - set(oldBinaryPackages)) if package])


def removeBinaryPackageFromWorkDir(package):
    join   = os.path.join
    remove = os.remove

    remove(join(config.workDir, package))
    


def create_directories():
    for dir in config.workDir, config.newBinaryPPath, config.oldBinaryPPath, config.localPspecRepo:
        if dir and not os.path.isdir(dir):
            try:
                os.makedirs(dir)
            except OSError:
                raise config.CfgError("'%s' dizini yaratılamadı, izin sorunu olabilir" % (dir))



def handle_exception(exception, value, tb):
    print exception, value
    traceback.print_tb(tb)
    


if __name__ == "__main__":
    sys.excepthook = handle_exception
    
    create_directories()

    main()


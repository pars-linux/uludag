#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009-2010, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import os
import time
import piksemel
import tarfile

from shutil import rmtree

import pisi

from PyQt4.QtCore import QObject, SIGNAL
from PyKDE4.kdecore import i18n

from pisi.db.packagedb import PackageDB

import backend

working_path = os.getenv("HOME") + "/offline"
pkgs_path = working_path + "/packages"

class Singleton(object):
    def __new__(type):
        if not '_the_instance' in type.__dict__:
            type._the_instance = object.__new__(type)
        return type._the_instance

class Offline(Singleton):
    def __init__(self):
        pass

    def saveProcess(self, packages, operation):
        """
        This function saves the done process to the process file
        with its process number. It gets the list of packages and
        operation type as parameter. Operation type can be just
        'install' or 'remove'.
        """
        self.__create(packages, operation)
        self.__write()

    def __create(self, packages, operation):

        if operation not in ["install", "remove"]:
            raise Exception("Unknown package operation")

        opno = self._get_latest()
        self.doc_path = "%s_%s.xml" % (opno, operation)
        self.filename = working_path + "/" + self.doc_path

        year, month, day, hour, minute = time.localtime()[0:5]

        self.op_type = operation
        self.op_date = "%s-%02d-%02d" % (year, month, day)
        self.op_time = "%02d:%02d" % (hour, minute)
        self.op_no = opno
        self.pkgs = packages

    def __write(self):

        iface = backend.pm.Iface()

        self.doc = piksemel.newDocument("PISI-Offline")

        newOp = self.doc.insertTag("Operation")
        newOp.setAttribute("Type", self.op_type)
        newOp.setAttribute("Date", self.op_date)
        newOp.setAttribute("Time", self.op_time)

        Packages = newOp.insertTag("Packages")
        if self.op_type == "install":
            for pkg in self.pkgs:
                iface.fetch([pkg], pkgs_path)
                Packages.insertTag("PackageURI").insertData(iface.getPackageURI(pkg))
        else:
            for pkg in self.pkgs:
                Packages.insertTag("Package").insertData(pkg)

        try:
            f = open(self.filename, "w")
            f.write(self.doc.toPrettyString())
            f.close()
            return True
        except:
            print "Dosyaya yazılamadı!"

    def _get_latest(self):

        self.__checkDir()

        files = filter(lambda h:h.endswith(".xml"), os.listdir(working_path))
        if not files:
            return "001"

        files.sort(lambda x,y:int(x.split("_")[0]) - int(y.split("_")[0]))
        no, opxml = files[-1].split("_")
        return "%03d" % (int(no) + 1)

    def __checkDir(self):
        # This function checks if the working path exists or not.
        try:
            os.mkdir(working_path)
            os.mkdir(pkgs_path)

        except OSError:
            pass


class OfflineManager(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.setExceptionHandler(self.exceptionHandler)
        self.setActionHandler(self.handler)

    def setActionHandler(self, handler):
        backend.pm.Iface().setHandler(handler)

    def setExceptionHandler(self, handler):
        backend.pm.Iface().setExceptionHandler(handler)

    def __removeDir(self):
        # This function removes if the working path exists.
        try:
            rmtree(working_path)
        except OSError:
            pass

    def writeCatalog(self, filename):
        """
        This function writes the catalog file to the given
        path. It gets the full filename of catalog file
        like '/home/user/a.tar' as a parameter.
        This function should be call after all install and remove
        processes done on online machine.
        """
        os.chdir(os.getenv("HOME"))
        tar = tarfile.open(filename, "w")
        tar.add("offline")
        tar.close()

        self.__removeDir()
        print "Catalog file writed."


    ### Below codes are about importing and exporting index

    def importIndex(self, filename):
        """
        This function imports the index file of offline machine
        and change the mode of 'Package Manager' as offline.
        It gets the full filename of index file like
        '/home/user/pisi-installed.xml' as a parameter.
        """
        f = open("/tmp/offline-pm.data", "w")
        f.write(filename)
        f.close

    def updateExportingProgress(self):
        """
        This function calculates and sends the percent of exporting
        process.
        """
        try:
            percent = (self.packageNo * 100) / self.totalPackages
        except ZeroDivisionError:
            percent = 0

        self.emit(SIGNAL("exportingProgress(int)"), percent)

    def exportIndex(self, filename):
        """
        This function exports the index (list of installed packages)
        of offline machine to the given path. It gets the full
        filename of index file like '/home/user/pisi-installed.xml'
        as a parameter.
        """
        index = pisi.index.Index()

        iface = backend.pm.Iface()
        source = iface.source  # store current source
        iface.setSource(None)  # set source None
        
        list_installed = iface.getPackageList()  # get installed package list
        self.totalPackages = list_installed.__len__()
        self.packageNo = 0
        
        for name in list_installed:
            index.packages.append(iface.getPackage(name))
            self.packageNo += 1
            self.updateExportingProgress()

        # these are unnecessary for offline index
        index.components = None
        index.groups = None
        index.distribution = None

        index.write(filename, sha1sum=False, compress=pisi.file.File.bz2, sign=None)

        print "Index file exported."

        iface.setSource(source)  # restore source


    ### Below codes are about doing offline jobs (install or remove pkgs)

    def startProcesses(self, filename):
        """
        This function reads the catalog file, handles
        the process files and do all install and remove
        operations on offline machine. It gets the full
        filename of catalog file like '/home/user/a.tar'
        as parameter.
        """
        self.__removeDir()

        self.__openArchive(filename)
        self.__handleProcesses()

    def __openArchive(self, filename):
        tar = tarfile.open(filename)
        tar.extractall(os.getenv("HOME"))
        tar.close()

    def __handleProcesses(self):

        self.operationPool = []

        files = filter(lambda x:x.endswith(".xml"), os.listdir(working_path))
        list = []

        for file in files:
            list.append([file, (file.split("_")[1]).split(".")[0]])

        list.sort()

        for p in range(0, list.__len__()):

            op_number = list[p][0]
            op_type = list[p][1]

            doc = piksemel.parse(working_path + "/" + op_number)
            parent = doc.getTag("Operation")

            for i in parent.tags("Packages"):
                packages = []

                # find a better way to split install and remove functions
                if op_type == "install":
                    for x in i.tags("PackageURI"):
                        packages.append(pkgs_path + "/" + str(x.firstChild().data()))
                else:
                    for x in i.tags("Package"):
                        packages.append(str(x.firstChild().data()))

            self.operationPool.append([op_type, packages])

        self.applyProcess()


    # Below codes applies the processes (instal or remove)

    def applyProcess(self):
        self.totalProcesses = self.operationPool.__len__()
        self.processNo = 0
        self.signalCounter = 0
        self.handlePool()

    def handlePool(self):
        self.updateTotalProcessPercent()
        self.processNo += 1

        try:
            operation = self.operationPool[0][0]
            packages = self.operationPool[0][1]

            self.operationPool.pop(0)

            self._startOperation(packages, operation)

        except IndexError:
            self.emit(SIGNAL("finished()"))

    def _startOperation(self, packages, operation):
        self.totalPackages = packages.__len__()
        self.packageNo = 0
        
        if operation == "install":
            backend.pm.Iface().installPackages(packages)

        elif operation == "remove":
            backend.pm.Iface().removePackages(packages)

        else:
            raise Exception("Unknown package operation")

    def exceptionHandler(self, exception):
        self.emit(SIGNAL("exception(QString)"), str(exception))

    def handler(self, package, signal, args):
        print "SIGNAL SIGNAL :: " , signal
        print "ARGS :: ARGS :: " , args
        if signal == "status":
            signal = str(args[0])
            args = args[1:]

            packageName = args[0]
            if signal == "installing":
                self.emit(SIGNAL("operationChanged(QString)"), i18n("Installing %s" % packageName))
                
            elif signal == "removing":
                self.emit(SIGNAL("operationChanged(QString)"), i18n("Removing %s" % packageName))
                # FIXME: "Removing %s" does not exists in PO files  !!!

            elif signal in ["installed", "removed"]:
                self.packageNo += 1
                self.updateCurrentProcessPercent()
        
        elif signal == "finished":
            if self.signalCounter == 1:
                self.handlePool()
                self.signalCounter = 0
            else:
                self.signalCounter += 1


    def updateTotalProcessPercent(self):
        """
        This function calculates and send the percent of total
        process. Total process includes all of install or remove
        processes in a offline catalog file.
        """
        try:
            percent = (self.processNo * 100) / self.totalProcesses
        except ZeroDivisionError:
            percent = 0

        self.emit(SIGNAL("totalProgress(int)"), percent)

    def updateCurrentProcessPercent(self):
        """
        This function calculates and sends the percent of current
        process. Current processes can be install or remove.
        """
        try:
            percent = (self.packageNo * 100) / self.totalPackages
        except ZeroDivisionError:
            percent = 0

        self.emit(SIGNAL("currentProgress(int)"), percent)

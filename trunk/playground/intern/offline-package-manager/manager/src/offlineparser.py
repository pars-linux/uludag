#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import os
import piksemel
import tarfile

from time import localtime
from shutil import rmtree

import backend

working_path = os.getenv("HOME") + "/offline"
pkgs_path = working_path + "/packages"

class OfflineParser:
    def __init__(self):
        pass

    def saveOperation(self, packages, operation):
        self.__create(packages, operation)
        self.__write()

    def __create(self, packages, operation):
        if operation not in ["install", "remove"]:
            raise Exception("Unknown package operation")

        self.op_no = self._get_latest()
        self.doc_name = "%s_%s.xml" % (self.op_no, operation)
        self.filename = working_path + "/" + self.doc_name

        year, month, day, hour, minute = localtime()[0:5]

        self.op_type = operation
        self.op_date = "%s-%02d-%02d" % (year, month, day)
        self.op_time = "%02d:%02d" % (hour, minute)
        self.pkgs = packages

    def __write(self):
        self.doc = piksemel.newDocument("PISI-Offline")

        newOp = self.doc.insertTag("Operation")
        newOp.setAttribute("Type", self.op_type)
        newOp.setAttribute("Date", self.op_date)
        newOp.setAttribute("Time", self.op_time)

        Packages = newOp.insertTag("Packages")
        if self.op_type == "install":
            for pkg in self.pkgs:
                backend.pm.Iface().fetch([pkg], pkgs_path)
                Packages.insertTag("PackageURI").insertData(backend.pm.Iface().getPackageURI(pkg))
        else:
            for pkg in self.pkgs:
                Packages.insertTag("Package").insertData(pkg)

        try:
            f = open(self.filename, "w")
            f.write(self.doc.toPrettyString())
            f.close()
            return True
        except:
            raise Exception("Operation file could not written!")

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

    def __removeDir(self):
        # This function removes if the working path exists.
        try:
            rmtree(working_path)
        except OSError:
            pass

    def saveArchive(self, filename):
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
        
        print "Session file is written."

    def extractArchive(self, filename):
        self.__removeDir()

        tar = tarfile.open(filename)
        tar.extractall(os.getenv("HOME"))
        tar.close()

    def parseOperations(self):
        operations = []
        operationList = []

        files = filter(lambda x:x.endswith(".xml"), os.listdir(working_path))
        for file in files:
            operationList.append([file, (file.split("_")[1]).split(".")[0]])
        operationList.sort()

        for operation in range(0, len(operationList)):
            op_file = operationList[operation][0]
            op_type = operationList[operation][1]

            doc = piksemel.parse(working_path + "/" + op_file)
            parent = doc.getTag("Operation")

            for i in parent.tags("Packages"):
                packages = []

                if op_type == "install":
                    for x in i.tags("PackageURI"):
                        packages.append(pkgs_path + "/" + str(x.firstChild().data()))
                else:
                    for x in i.tags("Package"):
                        packages.append(str(x.firstChild().data()))

            operations.append([op_type, packages])

        return operations

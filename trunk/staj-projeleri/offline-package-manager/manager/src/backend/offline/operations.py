#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# This module makes some operations for offline part of package manager

import os
import time
import piksemel
import tarfile

import pisi # !! Change this !! This module just needs db.installdb.fetch function.
# and pisi.api.install is necessary.

import gettext
__trans = gettext.translation('pisi', fallback=True)
_ = __trans.ugettext

from pisi.db.packagedb import PackageDB


class Operations:

    def __init__(self):
        self.path = os.getenv("HOME") + "/offlinePISI"
        self.pkgs_path = self.path + "/packages"
        self.pdb = PackageDB()

    def checkDir(self):
        # This function checks if the working path exists or not.
        try:
            os.mkdir(self.path)
            os.mkdir(self.pkgs_path)

        except OSError:
            pass

    def create(self, packages, operation):

        if operation not in ["install", "remove"]:
            raise Exception("Unknown package operation")

        opno = self._get_latest()
        self.doc_path = "%s_%s.xml" % (opno, operation)
        self.filename = self.path + "/" + self.doc_path

        year, month, day, hour, minute = time.localtime()[0:5]

        self.op_type = operation
        self.op_date = "%s-%02d-%02d" % (year, month, day)
        self.op_time = "%02d:%02d" % (hour, minute)
        self.op_no = opno
        self.pkgs = packages

        self.write()

    def write(self):

        self.doc = piksemel.newDocument("PISI-Offline")

        newOp = self.doc.insertTag("Operation")
        newOp.setAttribute("Type", self.op_type)
        newOp.setAttribute("Date", self.op_date)
        newOp.setAttribute("Time", self.op_time)

        if self.op_type == "install":
            pisi.api.fetch(self.pkgs, self.pkgs_path)

        Packages = newOp.insertTag("Packages")
        for pkg in self.pkgs:
            Packages.insertTag("URI").insertData(self.pdb.get_package(pkg).packageURI)

        try:
            f = open(self.filename, "w")
            f.write(self.doc.toPrettyString())
            f.close()
            return True
        except:
            print "Dosyaya yazılamadı!"

    def _get_latest(self):

        self.checkDir()

        print "hello get_latest"

        files = filter(lambda h:h.endswith(".xml"), os.listdir(self.path))
        if not files:
            return "001"

        files.sort(lambda x,y:int(x.split("_")[0]) - int(y.split("_")[0]))
        no, opxml = files[-1].split("_")
        return "%03d" % (int(no) + 1)

    def closeOfflineMode(self, filename):
        # This function make a tar file from offline PISI files
        os.chdir(os.getenv("HOME"))
        tar = tarfile.open(str(filename), "w")
        tar.add("offlinePISI")
        tar.close()

    ### Below codes are about doing offline jobs (install or remove pkgs)

    def startOperations(self, filename):
        self.openArchive(filename)
        self.handleOperation()

    def openArchive(self, filename):
        tar = tarfile.open(filename)
        tar.extractall(os.getenv("HOME"))
        tar.close()

    def handleOperation(self):

        files = filter(lambda x:x.endswith(".xml"), os.listdir(self.path))
        list = []

        for file in files:
            list.append([file, (file.split("_")[1]).split(".")[0]])

        list.sort()

        for p in range(0, list.__len__()):

            doc = piksemel.parse(self.path + "/" + list[p][0])
            parent = doc.getTag("Operation")

            for i in parent.tags("Packages"):
                packages = []

                for x in i.tags("URI"):
                    packages.append(x.firstChild().data())

                self.doOperation(packages, list[p][1])


    def doOperation(self, packages, operation):

        if operation == "install":
            self.link.System.Manager["pisi"].installPackage(packages, async=self.handler, timeout=2**16-1)
            pisi.api.install(packages)
            print "Paketler başarı ile kuruldu."

        elif operation == "remove":
            pisi.api.remove(packages)
            print "Paketler başarı ile kaldırıldı."

        else:
            raise Exception("Unknown package operation")

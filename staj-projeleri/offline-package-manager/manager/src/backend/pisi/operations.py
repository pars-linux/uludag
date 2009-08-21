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

import pisi # !! Change this !! This module just needs db.installdb.fetch function.

import gettext
__trans = gettext.translation('pisi', fallback=True)
_ = __trans.ugettext


class Operations:

    def __init__(self):
        self.path = os.getenv("HOME") + "/offlinePISI"
        self.pkgs_path = self.path + "/packages"

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

        opno = self._get_lastest()
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

        # Put the constant header
        xmlHeader =  '''<?xml version="1.0" encoding="utf-8"?>
'''
        self.doc = piksemel.newDocument("PISI-Offline-Operations")
        self.doc.setAttribute("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        self.doc.setAttribute("xsi:noNamespaceSchemaLocation","Offline-PISI.xsd")

        newOp = self.doc.insertTag("Operation")

        info = newOp.insertTag("Info")
        info.setAttribute("Number", self.op_no)
        info.setAttribute("Type", self.op_type)
        info.setAttribute("Date", self.op_date)
        info.setAttribute("Time", self.op_time)

        if self.op_type == "install":
            pisi.api.fetch(self.pkgs, self.pkgs_path)

        Packages = newOp.insertTag("Packages")
        for pkg in self.pkgs:
            Packages.insertTag("Name").insertData(pkg)

        try:
            f = open(self.filename, "w")
            f.write(xmlHeader + self.doc.toPrettyString())
            f.close()
            return True
        except:
            print "Dosyaya yazılamadı!"

    def _get_lastest(self):

        self.checkDir()

        files = filter(lambda h:h.endswith(".xml"), os.listdir(self.path))
        if not files:
            return "001"

        files.sort(lambda x,y:int(x.split("_")[0]) - int(y.split("_")[0]))
        no, opxml = files[-1].split("_")
        return "%03d" % (int(no) + 1)

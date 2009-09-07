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

''' This module makes some operations for offline part of package manager'''

import os
import time
import piksemel
import tarfile

import comar

import pisi

import gettext
__trans = gettext.translation('pisi', fallback=True)
_ = __trans.ugettext

from pisi.db.packagedb import PackageDB

import backend

class Singleton(object):
    def __new__(type):
        if not '_the_instance' in type.__dict__:
            type._the_instance = object.__new__(type)
        return type._the_instance

class Operations(Singleton):

    def __init__(self):
        self.path = os.getenv("HOME") + "/offlinePISI"
        self.pkgs_path = self.path + "/packages"
        self.pdb = PackageDB()

    def __checkDir(self):
        # This function checks if the working path exists or not.
        try:
            os.mkdir(self.path)
            os.mkdir(self.pkgs_path)

        except OSError:
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
        self.filename = self.path + "/" + self.doc_path

        year, month, day, hour, minute = time.localtime()[0:5]

        self.op_type = operation
        self.op_date = "%s-%02d-%02d" % (year, month, day)
        self.op_time = "%02d:%02d" % (hour, minute)
        self.op_no = opno
        self.pkgs = packages

    def __write(self):

        self.doc = piksemel.newDocument("PISI-Offline")

        newOp = self.doc.insertTag("Operation")
        newOp.setAttribute("Type", self.op_type)
        newOp.setAttribute("Date", self.op_date)
        newOp.setAttribute("Time", self.op_time)

        if self.op_type == "install":
            pisi.api.fetch(self.pkgs, self.pkgs_path)

        Packages = newOp.insertTag("Packages")
        if self.op_type == "install":
            for pkg in self.pkgs:
                Packages.insertTag("PackageURI").insertData(self.pdb.get_package(pkg).packageURI)
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

        files = filter(lambda h:h.endswith(".xml"), os.listdir(self.path))
        if not files:
            return "001"

        files.sort(lambda x,y:int(x.split("_")[0]) - int(y.split("_")[0]))
        no, opxml = files[-1].split("_")
        return "%03d" % (int(no) + 1)

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
        tar.add("offlinePISI")
        tar.close()

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

    def exportIndex(self, filename):
        """
        This function exports the index (list of installed packages)
        of offline machine to the given path. It gets the full
        filename of index file like '/home/user/pisi-installed.xml'
        as a parameter.
        """
        idb = pisi.db.installdb.InstallDB()
        index = pisi.index.Index()

        for name in idb.list_installed():
            index.packages.append(idb.get_package(name))

        self.__getComponents()
        self.__getGroups()
        self.__getDistro()

        index.add_components("/tmp/components.xml")
        index.add_groups("/tmp/groups.xml")
        index.add_distro("/tmp/distribution.xml")

        index.write(filename, sha1sum=True, compress=pisi.file.File.bz2, sign=None)

        print "Index file exported."

    # clean extra information in groups, components and distro (return empty formatted data)
    def __getGroups(self):
        gdb = pisi.db.groupdb.GroupDB()

        doc = piksemel.newDocument("PISI")
        newGroup = doc.insertTag("Groups")
        for grp in gdb.list_groups():
            group = newGroup.insertTag("Group")
            group.insertTag("Name").insertData(grp)

            g = gdb.get_group(grp)
            for l in g.localName.keys():
                ln = group.insertTag("LocalName")
                ln.setAttribute("xml:lang", l)
                ln.insertData(g.localName[l])

        f = open("/tmp/groups.xml", "w")
        f.write(doc.toPrettyString())
        f.close()

    def __getComponents(self):
        cdb = pisi.db.componentdb.ComponentDB()

        doc = piksemel.newDocument("PISI")
        newComponent = doc.insertTag("Components")

        for cpt in cdb.list_components():
            comp = newComponent.insertTag("Component")
            comp.insertTag("Name").insertData(cpt)

            c = cdb.get_component(cpt)
            i = comp.insertTag("LocalName")
            i.setAttribute("xml:lang", c.localName.items()[0][0])
            i.insertData(c.localName.items()[0][1])

            i = comp.insertTag("Summary")
            i.setAttribute("xml:lang", c.summary.items()[0][0])
            i.insertData(c.localName.items()[0][1])

            i = comp.insertTag("Description")
            i.setAttribute("xml:lang", c.description.items()[0][0])
            i.insertData(c.description.items()[0][1])
            comp.insertTag("Group").insertData(c.group)

        f = open("/tmp/components.xml", "w")
        f.write(doc.toPrettyString())
        f.close()

    def __getDistro(self):
        info = dict(pisi.context.config.values.general.items)

        doc = piksemel.newDocument("PISI")
        doc.insertTag("SourceName").insertData(info["distribution"])
        doc.insertTag("Version").insertData(info["distribution_release"])

        d = doc.insertTag("Description")
        d.setAttribute("xml:lang", "en")
        d.insertData("Pardus-2009 Repository")

        doc.insertTag("Type").insertData("Core")

        f = open("/tmp/distribution.xml", "w")
        f.write(doc.toPrettyString())
        f.close()

    ### Below codes are about doing offline jobs (install or remove pkgs)

    def startProcesses(self, filename):
        """
        This function reads the catalog file, handles
        the process files and do all install and remove
        operations on offline machine. It gets the full
        filename of catalog file like '/home/user/a.tar'
        as parameter.
        """
        self.__openArchive(filename)
        self.__handleProcesses()

    def __openArchive(self, filename):
        tar = tarfile.open(filename)
        tar.extractall(os.getenv("HOME"))
        tar.close()

    def __handleProcesses(self):

        doOperations = DoOperations()
        operationPool = []

        files = filter(lambda x:x.endswith(".xml"), os.listdir(self.path))
        list = []

        for file in files:
            list.append([file, (file.split("_")[1]).split(".")[0]])

        list.sort()

        for p in range(0, list.__len__()):

            op_number = list[p][0]
            op_type = list[p][1]

            doc = piksemel.parse(self.path + "/" + op_number)
            parent = doc.getTag("Operation")

            for i in parent.tags("Packages"):
                packages = []

                # find a better way to split install and remove functions
                if op_type == "install":
                    for x in i.tags("PackageURI"):
                        packages.append(self.pkgs_path + "/" + str(x.firstChild().data()))
                else:
                    for x in i.tags("Package"):
                        packages.append(str(x.firstChild().data()))

            operationPool.append([op_type, packages])

        doOperations.handlePool(operationPool)

class DoOperations(Singleton):
    def __init__(self):
        if not self.initialized():
            self.initComar()
            self.signalCounter = 0

    def initialized(self):
        return "link" in self.__dict__

    def initComar(self):
        self.link = comar.Link()
        self.link.setLocale()
        self.link.listenSignals("System.Manager", self.signalHandler)

    def setHandler(self, handler):
        self.link.listenSignals("System.Manager", handler)

    def setExceptionHandler(self, handler):
        self.exceptionHandler = handler

    def signalHandler(self, package, signal, args):
        if signal == "finished":
            if self.signalCounter == 1:
                self.handlePool(self.operationPool)
                self.signalCounter = 0
            else:
                self.signalCounter += 1

    def handlePool(self, operationPool):
        try:
            operation = operationPool[0][0]
            packages = operationPool[0][1]

            operationPool.pop(0)

            self.operationPool = operationPool

            self._doOperation(packages, operation)

        except IndexError:
            pass

    def _doOperation(self, packages, operation):

        if operation == "install":
            backend.pm.Iface().installPackages(packages)

        elif operation == "remove":
            backend.pm.Iface().removePackages(packages)

        else:
            raise Exception("Unknown package operation")

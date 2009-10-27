#!/usr/bin/python
# -*- coding: utf-8 -*-

import pisi
import os
import sys
import shutil

class RepoUtils:
    def __init__(self, work_dir, repo_uri):
        self.work_dir = work_dir
        self.repo_uri = repo_uri
        
        self.handler = pisi
        
        self.options = self.handler.config.Options()

        self.addTmpRepo()

        print self.handler.config.config.destdir
        
        self.cdb = self.handler.db.componentdb.ComponentDB()
        self.pdb = self.handler.db.packagedb.PackageDB()

    def setOptions(self):
        print "Setting new options...\n%s" % self.options.__dict__
        self.handler.api.set_options(self.options)

    def addTmpRepo(self):
        print "Creatinf work directory..."
        
        try:
            if not os.path.exists(self.work_dir):
                os.mkdir(self.work_dir)
        except OSError, e:
            if e.errno == 13:
                print "Permission denied for this operation"
                sys.exit(0)

        self.options.destdir = self.work_dir
        self.setOptions()
        
        print "Adding temprorary repository to fetch packages..."

        if "tmpRepo" in self.handler.api.list_repos():
            self.handler.api.remove_repo("tmpRepo")

        self.handler.api.add_repo("tmpRepo", self.repo_uri)
        self.handler.api.update_repo("tmpRepo")

    def getPackageList(self):
        # list = {"component":[pack1, pack2, ..., packn]}
        packageList = {}

        componentList = self.cdb.list_components("tmpRepo")
        for component in componentList:
            packageList[component] = self.cdb.get_packages(component)

        return packageList

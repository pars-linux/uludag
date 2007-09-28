# -*- coding: utf-8 -*-
#
# Copyright (C) 2005 - 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

"""package database
interface for update/query to local package repository

we basically store everything in PackageInfo class
yes, we are cheap
"""

import gettext
__trans = gettext.translation('pisi', fallback=True)
_ = __trans.ugettext

import piksemel

import pisi.db
import pisi.metadata
import pisi.dependency
import pisi.db.itembyrepo

class PackageDB(object):

    def __init__(self):

        self.__package_nodes = {} # Packages
        self.__revdeps = {}       # Reverse dependencies 
        self.__obsoletes = {}     # Obsoletes
        self.__replaces = {}      # Replaces

        repodb = pisi.db.repodb.RepoDB()

        for repo in repodb.list_repos():
            doc = repodb.get_repo_doc(repo)
            self.__package_nodes[repo] = self.__generate_packages(doc)
            self.__revdeps[repo] = self.__generate_revdeps(doc)
            self.__obsoletes[repo] = self.__generate_obsoletes(doc)
            self.__replaces[repo] = self.__generate_replaces(doc)

        self.pdb = pisi.db.itembyrepo.ItemByRepo(self.__package_nodes)
        self.rvdb = pisi.db.itembyrepo.ItemByRepo(self.__revdeps)
        self.odb = pisi.db.itembyrepo.ItemByRepo(self.__obsoletes)
        self.rpdb = pisi.db.itembyrepo.ItemByRepo(self.__replaces)

    def __generate_replaces(self, doc):
        return [x.getTagData("Name") for x in doc.tags("Package") if x.getTagData("Replaces")]
        
    def __generate_obsoletes(self, doc):
        distribution = doc.getTag("Distribution")
        obsoletes = distribution and distribution.getTag("Obsoletes")

        if not obsoletes:
            return []

        return map(lambda x: x.firstChild().data(), obsoletes.tags("Package"))
        
    def __generate_packages(self, doc):
        return dict(map(lambda x: (x.getTagData("Name"), x.toString()), doc.tags("Package")))

    def __generate_revdeps(self, doc):
        revdeps = {}
        for node in doc.tags("Package"):
            name = node.getTagData('Name')
            deps = node.getTag('RuntimeDependencies')
            if deps:
                for dep in deps.tags("Dependency"):
                    revdeps.setdefault(dep.firstChild().data(), set()).add((name, dep))
        return revdeps

    def has_package(self, name, repo=None):
        return self.pdb.has_item(name, repo)

    def get_package(self, name, repo=None):
        pkg, repo = self.get_package_repo(name, repo)
        return pkg

    def get_version(self, name, repo):
        if not self.has_package(name, repo):
            raise Exception(_('Package %s not found.') % name)
            
        pkg_doc = piksemel.parseString(self.__package_nodes[repo][name])
        history = pkg_doc.getTag("History")
        build = pkg_doc.getTagData("Build")
        version = history.getTag("Update").getTagData("Version")
        release = history.getTag("Update").getAttribute("release")

        return version, release, build and int(build)

    def get_package_repo(self, name, repo=None):
        pkg, repo = self.pdb.get_item_repo(name, repo)
        package = pisi.metadata.Package()
        package.parse(pkg)
        return package, repo

    def which_repo(self, name):
        return self.pdb.which_repo(name)

    def get_obsoletes(self, repo=None):
        obsoletes = []
        map(lambda x:obsoletes.extend(x), self.odb.get_item_values(repo))
        return obsoletes
    
    def get_rev_deps(self, name, repo=None):
        try:
            rvdb = self.rvdb.get_item(name, repo)
        except Exception: #FIXME: what exception could we catch here, replace with that.
            return []

        rev_deps = []
        for pkg, dep in rvdb:
            dependency = pisi.dependency.Dependency()
            dependency.package = pkg
            if dep.attributes():
                dependency.__dict__[dep.attributes()[0]] = dep.getAttribute(dep.attributes()[0])
            rev_deps.append((pkg, dependency))
        return rev_deps

    # replacesdb holds the info about the replaced packages (ex. gaim -> pidgin)
    def get_replaces(self, repo):
        pairs = {}

        for pkg_name in self.__replaces[repo]:
            replaces = self.get_package(pkg_name, repo).replaces
            for r in replaces:
                if pisi.replace.installed_package_replaced(r):
                    pairs[r.package] = pkg_name

        return pairs

    def list_packages(self, repo):
        return self.pdb.get_item_keys(repo)

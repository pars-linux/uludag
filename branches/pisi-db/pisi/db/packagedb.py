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
            del doc

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
                    revdeps.setdefault(dep.firstChild().data(), set()).add(name)
        return revdeps
    
    def has_package(self, name, repo):
        return self.__package_nodes.has_key(repo) and self.__package_nodes[repo].has_key(name)

    def get_package(self, name, repo):
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
        del pkg_doc

        return version, release, build and int(build)

    def get_package_repo(self, name, repo):
        if self.__package_nodes.has_key(repo):
            if self.__package_nodes[repo].has_key(name):
                pkg = pisi.metadata.Package()
                pkg.parse(self.__package_nodes[repo][name])
                return pkg, repo

        raise Exception(_('Package %s not found.') % name)

    def which_repo(self, name):
        for repo in self.__package_nodes.keys():
            if self.__package_nodes[repo].has_key(name):
                return repo

    def get_obsoletes(self, repo):
        if not self.__obsoletes.has_key(repo):
            raise Exception(_('Repository %s does not exits') % repo)

        return self.__obsoletes[repo]
    
    def get_rev_deps(self, name, repo):
        if not self.__revdeps.has_key(repo):
            raise Exception(_('Repository %s does not exits') % repo)

        if self.__revdeps[repo].has_key(name):
            return list(self.__revdeps[repo][name])
        else:
            return []

    # replacesdb holds the info about the replaced packages (ex. gaim -> pidgin)
    def get_replaces(self, repo):
        pairs = {}
        for pkg_name in self.__replaces[repo]:
            replaces = self.get_package(pkg_name, repo).replaces
            for r in replaces:
                if pisi.replace.installed_package_replaced(r):
                    pairs[r.package] = pkg_name

        return pairs

    def get_deps(self, name, repo):
        raise Exception(_('Not implemented'))

    def list_packages(self, repo):
        if self.__package_nodes.has_key(repo):
            return self.__package_nodes[repo].keys()

        raise Exception(_('Repository %s does not exists.') % repo)

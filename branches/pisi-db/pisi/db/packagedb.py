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

        self.package_nodes = {}
        self.revdeps = {}
        repodb = pisi.db.repodb.RepoDB()

        for repo in repodb.list_repos():
            doc = repodb.get_repo_doc(repo)
            self.package_nodes[repo] = self.__generate_packages(doc)
            self.revdeps[repo] = self.__generate_revdeps(doc)
            del doc

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
        return self.package_nodes.has_key(repo) and self.package_nodes[repo].has_key(name)

    def get_package(self, name, repo):
        pkg, repo = self.get_package_repo(name, repo)
        return pkg

    def get_package_repo(self, name, repo):
        if self.package_nodes.has_key(repo):
            if self.package_nodes[repo].has_key(name):
                pkg = pisi.metadata.Package()
                pkg.parse(self.package_nodes[repo][name])
                return pkg, repo

        raise Exception(_('Package %s not found.') % name)

    def which_repo(self, name):
        for repo in self.package_nodes.keys():
            if self.package_nodes[repo].has_key(name):
                return repo

    def get_obsoletes(self, repo=None):
        raise Exception(_('Not implemented'))
    
    def get_replaces(self, repo):
        raise Exception(_('Not implemented'))
    
    def get_rev_deps(self, name, repo):
        if not self.revdeps.has_key(repo):
            raise Exception(_('Repository %s does not exits') % repo)

        if self.revdeps[repo].has_key(name):
            return list(self.revdeps[repo][name])
        else:
            return []

    def get_deps(self, name, repo):
        raise Exception(_('Not implemented'))

    def list_packages(self, repo):
        if self.package_nodes.has_key(repo):
            return self.package_nodes[repo].keys()

        raise Exception(_('Repository %s does not exists.') % repo)

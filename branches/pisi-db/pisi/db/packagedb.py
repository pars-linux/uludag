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
        repodb = pisi.db.repodb.RepoDB()

        for repo in repodb.list_repos():
            doc = repodb.get_repo_doc(repo)
            self.package_nodes[repo] = dict(map(lambda x: (x.getTagData("Name"), x), doc.tags("Package")))
    
    def has_package(self, name, repo):
        return self.package_map.has_key(repo) and self.package_map[repo].has_key(name)

    def get_package(self, name, repo):
        pkg, repo = self.get_package_repo(name, repo)
        return pkg

    def get_package_repo(self, name, repo):
        if self.package_map.has_key(repo):
            if self.package_map[repo].has_key(name):
                pkg = pisi.metadata.Package()
                pkg.parse(self.package_map[repo][name].toString())
                return pkg, repo

        raise Exception(_('Package %s not found.') % name)

    def which_repo(self, name):
        for repo in self.package_map.keys():
            if self.package_map[repo].has_key(name):
                return repo

    def get_obsoletes(self, repo=None):
        raise Exception(_('Not implemented'))
    
    def get_replaces(self, repo):
        raise Exception(_('Not implemented'))
    
    def get_rev_deps(self, name, repo):
        raise Exception(_('Not implemented'))

    def get_deps(self, name, repo):
        raise Exception(_('Not implemented'))

    def list_packages(self, repo):
        raise Exception(_('Not implemented'))

def init():
    return PackageDB()

def finalize():
    pass

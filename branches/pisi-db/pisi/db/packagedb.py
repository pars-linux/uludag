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

import pisi
import pisi.specfile
import pisi.metadata
import pisi.context as ctx

import piksemel

class Error(pisi.Error):
    pass

class NotfoundError(pisi.Error):
    def __init__(self, pkg):
        pisi.Error.__init__("Package %s not found" % pkg)
        self.pkg = pkg

class PackageMap:
    def __init__(self):
        self.package_map = {}
        for repo in ctx.repodb.list():
            doc = piksemel.parse(ctx.repodb.get_local_index(repo)[:-4])
            self.package_map[repo] = dict(map(lambda x: (x.getTagData("Name"), x), doc.tags("Package")))

    def has_package(self, name, repo=None):
        if repo:
            return self.package_map.has_key(repo) and self.package_map[repo].has_key(name)
        else:
            for repo in self.package_map.keys():
                if self.package_map[repo].has_key(name):
                    return True

    def which_repo(self, name):
        for repo in self.package_map.keys():
            if self.package_map[repo].has_key(name):
                return repo

    def get_package_list(self, repo=None):
        if repo:
            if self.package_map.has_key(repo):
                return self.package_map[repo].keys()
        else:
            packages = []
            for repo in self.package_map.keys():
                packages.extend(self.package_map[repo].keys())
            return packages

    def get_package(self, name, repo=None):
        pkg = pisi.metadata.Package()
        if repo:
            if self.package_map.has_key(repo):
                if self.package_map[repo].has_key(name):
                    xml = self.package_map[repo][name].toString()
                    pkg.parse(xml)
                    return pkg, repo
        else:
            for repo in self.package_map.keys():
                if self.package_map[repo].has_key(name):
                    xml = self.package_map[repo][name].toString()
                    pkg.parse(xml)
                    return pkg, repo

        raise Error(_('Package %s not found') % name)

class PackageDB(object):
    """PackageDB class provides an interface to the package database
    using shelf objects"""

    def __init__(self):
        # package, revdep, obsoleted, replaces
        self.package_map = PackageMap()
            
    def close(self):
        pass

    def destroy(self):
        pass
    
    def has_package(self, name, repo=None):
        return self.package_map.has_package(name, repo)

    def get_package(self, name, repo=None):
        pkg, repo = self.package_map.get_package(name, repo)
        return pkg

    def get_package_repo(self, name, repo=None):
        return self.package_map.get_package(name, repo)

    def which_repo(self, name):
        return self.package_map.which_repo(name)

    def get_obsoletes(self, repo=None):
        return []
    
    # replacesdb holds the info about the replaced packages (ex. gaim -> pidgin)
    def get_replaces(self, repo = None):
        pairs = {}
        return pairs
    
    def get_rev_deps(self, name, repo = None):
        return []

    def get_deps(self, name, repo = None):
        pkg, repo = self.package_map.get_package(name, repo)
        return pkg.packageDependencies

    def list_packages(self, repo=None):
        return self.package_map.get_package_list(repo)

    def add_obsoletes(self, obsoletes, repo):
        pass

    def add_package(self, package_info, repo):
        pass

    def clear(self):
        pass

    def remove_package(self, name, repo = None):
        pass
        
    def remove_repo(self, repo):
        pass

def remove_tracking_package(name):
    pass

pkgdb = None

def init():
    global pkgdb

    if pkgdb is not None:
        return pkgdb

    pkgdb = PackageDB()
    return pkgdb

def finalize():
    global pkgdb

    if pkgdb is not None:
        pkgdb.close()
        pkgdb = None

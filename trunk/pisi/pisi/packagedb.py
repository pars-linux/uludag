# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# package database
# interface for update/query to local package repository

# Authors:  Eray Ozkural <eray@uludag.org.tr>
#           Baris Metin <baris@uludag.org.tr>

# we basically store everything in PackageInfo class
# yes, we are cheap

import bsddb.dbshelve as shelve
import os, fcntl
from bsddb import db

import gettext
__trans = gettext.translation('pisi', fallback=True)
_ = __trans.ugettext

import pisi
import pisi.util as util
import pisi.context as ctx
import pisi.lockeddbshelve as shelve

class Error(pisi.Error):
    pass

class PackageDB(object):
    """PackageDB class provides an interface to the package database with
    a delegated dbshelve object"""
    def __init__(self, id):
        self.d = shelve.LockedDBShelf('package-%s' % id )
        self.dr = shelve.LockedDBShelf('revdep-%s' % id )

    def close(self):
        self.d.close()
        self.dr.close()

    def has_package(self, name):
        name = str(name)
        return self.d.has_key(name)

    def get_package(self, name):
        name = str(name)
        return self.d[name]

    def get_rev_deps(self, name):
        name = str(name)
        if self.dr.has_key(name):
            return self.dr[name]
        else:
            return []

    def list_packages(self):
        list = []
        for (pkg, x) in self.d.iteritems():
            list.append(pkg)
        return list

    #TODO: list_upgrades?

    def add_package(self, package_info):
        name = str(package_info.name)
        self.d[name] = package_info
        for dep in package_info.runtimeDeps:
            dep_name = str(dep.package)
            if self.dr.has_key(dep_name):
                self.dr[dep_name].append( (name, dep) )
            else:
                self.dr[dep_name] = [ (name, dep) ]

    def clear(self):
        self.d.clear()

    def remove_package(self, name):
        name = str(name)
        del self.d[name]


packagedbs = {}

def add_db(name):
    packagedbs[name] = PackageDB('repo-' + name)

def get_db(name):
    return packagedbs[name]

def remove_db(name):
    del packagedbs[name]
    #erase database file
    
def has_package(name):
    repo = which_repo(name)
    if repo or thirdparty_packagedb.has_package(name) or inst_packagedb.has_package(name):
        return True
    return False

def which_repo(name):
    import pisi.repodb
    for repo in pisi.repodb.db.list():
        if get_db(repo).has_package(name):
            return repo
    return None

def get_package(name):
    repo = which_repo(name)
    if repo:
        return get_db(repo).get_package(name)
    if thirdparty_packagedb.has_package(name):
        return thirdparty_packagedb.get_package(name)
    if inst_packagedb.has_package(name):
        return inst_packagedb.get_package(name)
    raise Error(_('get_package: package %s not found') % name)

def get_rev_deps(name):
    repo = which_repo(name)
    if repo:
        return get_db(repo).get_rev_deps(name)
    if thirdparty_packagedb.has_package(name):
        return thirdparty_packagedb.get_rev_deps(name)    
    if inst_packagedb.has_package(name):
        return inst_packagedb.get_rev_deps(name)

    return None

def remove_package(name):
    # remove the guy from the tracking databases
    inst_packagedb.remove_package(name)
    if thirdparty_packagedb.has_package(name):
        thirdparty_packagedb.remove_package(name)

# tracking databases for non-repository information

thirdparty_packagedb = inst_packagedb = None

def init_db():   
    if not pisi.packagedb.thirdparty_packagedb:
        pisi.packagedb.thirdparty_packagedb = PackageDB('thirdparty')
    if not pisi.packagedb.inst_packagedb:
        pisi.packagedb.inst_packagedb = PackageDB('installed')

def finalize_db():
    if pisi.packagedb.thirdparty_packagedb:
        pisi.packagedb.thirdparty_packagedb.close()
    if pisi.packagedb.inst_packagedb:
        pisi.packagedb.inst_packagedb.close()
    if pisi.packagedb.packagedbs:
        pisi.packagedb.packagedbs.close()


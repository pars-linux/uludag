#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2008 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file

import sys

import pisi

class RepoError:
    pass

def get_install_order(packages):
    base = pisi.api.get_base_upgrade_order(packages)
    return pisi.api.get_install_order(set(base+packages))

def get_remove_order(packages):
    return pisi.api.get_remove_order(packages)

def get_upgrade_order(packages):
    base = pisi.api.get_base_upgrade_order(packages)
    return pisi.api.get_upgrade_order(set(base+packages))

def get_union_component_packages(name, walk=True):
    return pisi.db.componentdb.ComponentDB().get_union_packages(name, walk)

def get_union_component(name):
    return pisi.db.componentdb.ComponentDB().get_union_component(name)

def get_components():
    return pisi.db.componentdb.ComponentDB().list_components()

def get_installed_package(package):
    try:
        return pisi.db.installdb.InstallDB().get_package(package)
    except pisi.db.repodb.RepoError:
        raise RepoError

def get_repo_package(package):
    return pisi.db.packagedb.PackageDB().get_package(package)

def get_repo_and_package(package):
    return pisi.db.packagedb.PackageDB().get_package_repo(package)

def humanize(size):
    return pisi.util.human_readable_size(size)

def get_upgradable_packages():
    try:
        return pisi.api.list_upgradable()
    except pisi.db.repodb.RepoError:
        raise RepoError

def get_installed_packages():
    return list(pisi.api.list_installed())

def parse_package_name(name):
    return pisi.util.parse_package_name(name)

def read_config(name):
    return pisi.configfile.ConfigurationFile(name)

def is_component_visible(name):
    cdb = pisi.db.componentdb.ComponentDB()
    return cdb.get_component(name).visibleTo == 'user'

def reloadPisi():
    for module in sys.modules.keys():
        if module.startswith("pisi."):
            """removal from sys.modules forces reload via import"""
            del sys.modules[module]

    reload(pisi)

def get_not_installed_packages():
    return list((set(pisi.api.list_available()) - set(pisi.api.list_installed())) - set(pisi.api.list_replaces().values()))

def get_repositories():
    return pisi.db.repodb.RepoDB().list_repos()

def get_package_repository(package):
    return pisi.db.packagedb.PackageDB().which_repo(package)

def get_repository_url(name):
    return pisi.db.repodb.RepoDB().get_repo(name).indexuri.get_uri()

def get_conflicts(packages):
    return pisi.api.get_conflicts(packages)

def get_package(package, installed=False):
    pkg = None
    if installed:
        pkg = get_installed_package(package)
        pkg.size = pkg.installedSize
    else:
        try:
            pkg = get_repo_package(package)
        except Exception, e: # Repo Item not Found
            # Handle replaced and obsolete packages
            replaced = pisi.db.packagedb.PackageDB().get_replaces()
            if replaced.has_key(package):
                pkg = get_repo_package(replaced[package])
            else:
                raise e

        pkg.size = pkg.packageSize

    try:
        pkg.repo = get_package_repository(package)
    except Exception, e:
        pkg.repo = "N/A"

    return pkg

def search_in_installed(terms):
    return pisi.api.search_installed(terms)

def search_in_repos(terms):
    installdb = pisi.db.installdb.InstallDB()
    # search in repos but filter installed ones
    return filter(lambda x:not installdb.has_package(x), pisi.api.search_package(terms))

def search_in_upgradables(terms):
    return list(set(get_upgradable_packages()).intersection(pisi.api.search_package(terms)))

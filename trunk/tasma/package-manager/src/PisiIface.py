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

import pisi

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
    return pisi.db.installdb.InstallDB().get_package(package)

def get_repo_package(package):
    return pisi.db.packagedb.PackageDB().get_package(package)

def get_repo_and_package(package):
    return pisi.db.packagedb.PackageDB().get_package_repo(package)

def humanize(size):
    return pisi.util.human_readable_size(size)

def get_upgradable_packages():
    return pisi.api.list_upgradable()

def get_installed_packages():
    return list(pisi.api.list_installed())

def parse_package_name(name):
    return pisi.util.parse_package_name(name)

def read_config(name):
    return pisi.configfile.ConfigurationFile(name)

def is_component_visible(name):
    cdb = pisi.db.componentdb.ComponentDB()
    return cdb.get_component(name).visibleTo == 'user'

def reloadPisi(self):
    for module in sys.modules.keys():
        if module.startswith("pisi."):
            """removal from sys.modules forces reload via import"""
            del sys.modules[module]

    reload(pisi)

def get_not_installed_packages():
    return list((set(pisi.api.list_available()) - set(pisi.api.list_installed())) - set(pisi.api.list_replaces().values()))

def get_repositories():
    return pisi.db.repodb.RepoDB().list_repos()

def get_repository_url(name):
    return pisi.db.repodb.RepoDB().get_repo(name).indexuri.get_uri()

def get_conflicts(packages):
    return pisi.api.get_conflicts(packages)

def get_package(package, installed=False):
    if installed:
        return get_installed_package(package)
    else:
        return get_repo_package(package)

def search_package(terms, installed=False):
    if installed:
        return pisi.api.search_installed(terms)
    else:
        return pisi.api.serach_package(terms)


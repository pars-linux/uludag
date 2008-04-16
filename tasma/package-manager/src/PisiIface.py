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

def get_installed_package(package):
    return pisi.db.installdb.InstallDB().get_package(package)

def get_repo_package(package):
    return pisi.db.packagedb.PackageDB().get_package(package)

def humanize(size):
    return pisi.util.human_readable_size(size)

def get_upgradable_packages():
    return pisi.api.list_upgradable()

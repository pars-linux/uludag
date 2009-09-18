#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

from pardus import strutils

import pisi

class Iface:

    def __init__(self):
        pass

    def upgrade(self, packages, ignore_comar=False):
        if ignore_comar:
            os.system("pisi up -y --ignore-comar %s" % strutils.strlist(packages))
        else:
            os.system("pisi up -y %s" % strutils.strlist(packages))

    def install(self, packages=None, component=None):
        pkgs = cmps = ""

        if packages:
            pkgs = strutils.strlist(packages)

        if component:
            cmps = " -c %s" % component

        os.system("pisi install -y %s %s" % (pkgs, cmps))

    def configure_pending(self, packages):
        if packages:
            os.system("pisi cp -y %s" % strutils.strlist(packages))
        else:
            os.system("pisi cp -y")

    def component_packages(self, components):
        componentdb = pisi.db.componentdb.ComponentDB()
        packages = []
        if components:
            for name in components:
            if componentdb.has_component(name):
                packages.extend(componentdb.get_union_packages(name, walk=True))
        return packages

    def remove_repos(self):
        for repo in pisi.api.list_repos():
            pisi.api.remove_repo(repo)

    def add_repo(name, url):
        pisi.api.add_repo(name, url)

    def download(packages):
        pisi.api.fetch(packages, pisi.ctx.config.cached_packages_dir())


#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2010 TUBITAK/UEKAE
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Please read the COPYING file.
#

import os
import glob

import pisi.api
import pisi.config
from pisi.operations.delta import create_delta_package

from buildfarm import cli, logger, utils
from buildfarm.config import configuration as conf


class PisiApi:
    def __init__(self, stdout=None, stderr=None, outputDir = conf.workdir):
        self.options = pisi.config.Options()

        # Override these so that pisi searches for .pisi files in the right locations
        self.options.output_dir = outputDir
        self.options.debug_packages_dir = utils.get_debug_packages_directory()
        self.options.compiled_packages_dir = utils.get_compiled_packages_directory()

        self.options.yes_all = True
        self.options.ignore_file_conflicts = True
        self.options.ignore_package_conflicts = True
        self.options.debug = True
        self.options.verbose = True
        self.options.ignore_check = conf.ignorecheck
        self.options.ignore_sandbox = False

        # Set API options
        pisi.api.set_options(self.options)

        # Set IO streams
        pisi.api.set_io_streams(stdout=stdout, stderr=stderr)

        pisi.api.set_userinterface(cli.CLI(stdout))

        self.builder = None

    def get_new_packages(self):
        return self.builder.new_packages

    def get_new_debug_packages(self):
        return self.builder.new_debug_packages

    def get_delta_package_map(self):
        # NOTE: Returns a dict
        return self.builder.delta_map

    def close(self):
        pisi.api.ctx.ui.prepareLogs()

    def build(self, pspec):
        if not os.path.exists(pspec):
            logger.error("'%s' does not exist!" % pspec)
            raise ("'%s' does not exist!" % pspec)

        logger.info("BUILD called for %s" % pspec)

        if conf.sandboxblacklist and \
                utils.get_package_name_from_path(pspec) in conf.sandboxblacklist:
            logger.info("Disabling sandbox for %s" % pspec)
            pisi.api.ctx.set_option("ignore_sandbox", True)

        self.builder = pisi.operations.build.Builder(pspec)
        self.builder.build()

        logger.info("Created package(s): %s" % self.builder.new_packages)


    def get_install_order(self, packages):
        """ Get installation order for pisi packages. """
        import pisi.pgraph as pgraph

        # d_t: dict assigning package names to metadata's
        d_t = {}

        # dfn: dict assigning package names to package paths
        dfn = {}
        for p in packages:
            package = pisi.package.Package(os.path.join(conf.workdir, p))
            package.read()
            name = str(package.metadata.package.name)
            d_t[name] = package.metadata.package
            dfn[name] = p

        class PackageDB:
            def get_package(self, key, repo = None):
                return d_t[str(key)]

        packagedb = PackageDB()

        A = d_t.keys()
        G_f = pgraph.PGraph(packagedb)

        for x in A:
            G_f.add_package(x)

        B = A
        while len(B) > 0:
            Bp = set()
            for x in B:
                pkg = packagedb.get_package(x)
                for dep in pkg.runtimeDependencies():
                    if dep.satisfied_by_dict_repo(d_t):
                        if not dep.package in G_f.vertices():
                            Bp.add(str(dep.package))
                        G_f.add_dep(x, dep)
            B = Bp

        order = G_f.topological_sort()
        order.reverse()

        return [dfn[p] for p in order]

    def install(self, p):
        a = []
        a.append(p)
        pisi.api.install(a, ignore_file_conflicts=self.options.ignore_file_conflicts,
                            ignore_package_conflicts=self.options.ignore_package_conflicts,
                            reinstall=True)


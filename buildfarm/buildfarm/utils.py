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

# Various helper functions for pisi packages

import os
import glob

from buildfarm.config import configuration as conf

import pisi.util
import pisi.context as ctx

def print_header(msg):
    print "\n%s\n%s\n" % (msg, '-'*len(msg))

def create_directories():
    directories = [
                    conf.workdir,
                    conf.buildfarmdir,
                    conf.repositorydir,
                    conf.logdir,
                    get_compiled_packages_directory(),
                    get_debug_packages_directory(),
                    get_local_repository_url(),
                    get_package_log_directory(),
                  ]

    for directory in directories:
        if directory and not os.path.isdir(directory):
            try:
                os.makedirs(directory)
            except OSError:
                print "Directory %s cannot be created." % directory

def get_local_repository_url():
    return os.path.join(conf.repositorydir,
                        conf.release,
                        conf.subrepository)

def get_remote_repository_url():
    return os.path.join(conf.scmrepositorybaseurl,
                        conf.release,
                        conf.subrepository)

def get_package_log_directory():
    return os.path.join(conf.logdir,
                        conf.release,
                        conf.subrepository,
                        conf.architecture)

def get_debug_packages_directory():
    return "%s-debug" % get_compiled_packages_directory()

def get_compiled_packages_directory():
    return os.path.join(conf.binarypath,
                        conf.release,
                        conf.subrepository,
                        conf.architecture)

def get_expected_file_name(spec):
    last_update = spec.history[0]

    # e.g. kernel-2.6.32.24-143-p11-x86_64.pisi if the last update's
    # version is 2.6.32.24 and the release is 143.
    return pisi.util.package_filename(spec.packages[0].name,
                                      last_update.version,
                                      last_update.release)

def get_package_name(pkg):
    return pisi.util.split_package_filename(pkg)[0]

def get_package_name_from_path(pkg):
    return os.path.basename(os.path.dirname(pkg))

def get_package_component_path(pkg):
    """Extracts system/base/gettext from full path."""
    return os.path.dirname(pkg).partition("%s/" % \
            get_local_repository_url())[-1]

def delete_pisi_files_from(directory):
    """Deletes all .pisi files found in directory."""
    for pisi in glob.glob("%s/*%s" % (directory.rstrip("/"),
                                      ctx.const.package_suffix)):
        try:
            print pisi
            os.unlink(pisi)
        except OSError:
            pass

def is_arch_excluded(spec):
    """Returns True if the given pspec.xml shouldn't be built
    on the current architecture."""
    return ctx.config.values.get("general", "architecture") \
            in spec.source.excludeArch

def is_delta_package(pkg):
    return pkg.endswith(ctx.const.delta_package_suffix)

def is_debug_package(pkg):
    package_name = get_package_name(pkg)
    return package_name.endswith(ctx.const.debug_name_suffix)

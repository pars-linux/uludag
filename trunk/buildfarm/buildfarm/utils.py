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
import pisi.api

from buildfarm.config import configuration as conf
constants = pisi.api.ctx.const

def create_directories():
    directories = [
                    conf.workdir,
                    conf.testpath,
                    conf.deltapath,
                    conf.debugpath,
                    conf.outputdir,
                    conf.binarypath,
                    conf.repositorydir,
                    get_local_pspec_repository(),
                  ]

    for directory in directories:
        if directory and not os.path.isdir(directory):
            try:
                os.makedirs(directory)
            except OSError:
                raise ("Directory '%s' cannot be created." % directory)

def get_pardus_release():
    if os.path.exists("/etc/pardus-release"):
        return open("/etc/pardus-release", "r").read().strip()

def get_local_repository_url():
    return os.path.join(conf.repositorydir, conf.release, conf.subrepository)

def get_remote_repository_url():
    return os.path.join(conf.scmrepositorybaseurl, conf.release, conf.subrepository)

def get_build_no(p):
    return int(p.rstrip(constants.package_suffix).rsplit("-", 3)[3])

def get_package_name(p):
    return p.rstrip(constants.package_suffix).rsplit("-", 3)[0]

def get_package_name_from_path(p):
    return os.path.basename(os.path.dirname(p))

def is_delta_package(p):
    return p.endswith(constants.delta_package_suffix)

def is_debug_package(p):
    return constants.debug_name_suffix in p

def get_delta_packages(path, name, target=None):
    if target and isinstance(target, int):
        # Return delta packages goint to target
        pattern = "%s-[0-9]*-%d%s" % (name, target, constants.delta_package_suffix)
    else:
        # Return all delta packages
        pattern = "%s-[0-9]*-[0-9]*%s" % constants.delta_package_suffix
    return glob.glob1(path, pattern)

def get_deltas_not_going_to(path, package):
    # e.g. package <- kernel-2.6.25.20-114-45.pisi
    # Returns the list of delta packages in 'path' for 'package' going from any
    # build to any build other than 45.
    # return -> ['kernel-41-42-delta.pisi', 'kernel-41-44.delta-pisi', etc]
    name = get_package_name(package)
    target_build = get_build_no(package)
    return list(set(get_delta_packages(path, name)).difference(get_delta_packages(path, name, target_build)))


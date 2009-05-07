#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Please read the COPYING file.

# Various helper functions for pisi packages

import glob

def getBuild(p):
    return int(p.rstrip(".pisi").rsplit("-", 3)[3])

def getName(p):
    return p.rstrip(".pisi").rsplit("-", 3)[0]

def isdelta(p):
    return p.endswith(".delta.pisi")

def isdebug(p):
    return "-dbginfo-" in p

def getDeltaPackages(path, name, target=None):
    if target and isinstance(target, int):
        # Return delta packages goint to target
        pattern = "%s-[0-9]*-%d.delta.pisi" % (name, target)
    else:
        # Return all delta packages
        pattern = "%s-[0-9]*-[0-9]*.delta.pisi" % name
    return glob.glob1(path, pattern)

def getDeltasNotGoingTo(path, package):
    # e.g. package <- kernel-2.6.25.20-114-45.pisi
    # Returns the list of delta packages in 'path' for 'package' going from any
    # build to any build other than 45.
    # return -> ['kernel-41-42-delta.pisi', 'kernel-41-44.delta-pisi', etc]
    name = getName(package)
    targetBuild = getBuild(package)
    return list(set(getDeltaPackages(path, name)).difference(getDeltaPackages(path, name, targetBuild)))


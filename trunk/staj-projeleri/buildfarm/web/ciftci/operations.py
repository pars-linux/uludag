#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, TUBITAK/UEKAE
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Please read the COPYING file.

# module for getting the runtime dependencies of a binary pisi package
# through metadata.xml

import pisi
import os
import fnmatch

def getPisiList(path):
    # Generates a list which includes a dictionary for each package
    return [{'name':p} for p in os.listdir(path) if p.endswith(".pisi")]

def getRuntimeDeps(p):
    metadata = (pisi.package.Package(p)).get_metadata()
    return metadata.package.runtimeDependencies()

def isDepExists(path, name, versionFrom):
    # Searchs for the given name in the path
    if fnmatch.filter(os.listdir(path), name+'*'):
        return True
    else:
        return False

def movePackage(name, sourcePath, destPath):
    fileName = name + ".pisi"
    try:
        os.rename(os.path.join(sourcePath, fileName),\
                  os.path.join(destPath, fileName))
    except OSError:
        return False

    return True

def getPisiPackages(path):
    pisi_list = getPisiList(path)

    for ps in pisi_list:
        ps["deplist"] = []
        for m in getRuntimeDeps(os.path.join(path, ps["name"])):
            ps["deplist"].append({ "name": m.package,
                                   "versionFrom" : m.versionFrom,
                                   "exists" : isDepExists(path, m.package, m.versionFrom) })
    return pisi_list

def old_getPisiDict(path):
    # Returns a dictionary which contains the runtime dependencies
    # of the packages
    d = {}
    for ps in getPisiList(path):
        # ps is a dictionary which has only 'name' key
        d[ps["name"]] = map(lambda x: x.package, getRuntimeDeps(os.path.join(path, ps["name"])))

    return d

def old_getPisiPackages(path):
    pisi_list = getPisiList(path)
    dep_dict = old_getPisiDict(path)

    for p in pisi_list:
        if dep_dict[p["name"]]:
            p["deplist"] = dep_dict[p["name"]]

    return pisi_list


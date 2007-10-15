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

def getDifferences(sourcePath, destPath):
    # Returns the pisi packages which are in source but not in dest
    pisi_list = [{'name':p} for p in os.listdir(sourcePath) \
                if not os.path.exists(os.path.join(destPath, p)) and p.endswith(".pisi")]

    for ps in pisi_list:
        ps["deplist"] = []
        for m in getRuntimeDeps(os.path.join(sourcePath, ps["name"])):
            ps["deplist"].append({ "name": m.package,
                                   "versionFrom" : m.versionFrom,
                                   "exists" : isDepExists(sourcePath, m.package, m.versionFrom) })
    return pisi_list

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
    pisi_list =  [{'name':p} for p in os.listdir(path) if p.endswith(".pisi")]

    for ps in pisi_list:
        ps["deplist"] = []
        for m in getRuntimeDeps(os.path.join(path, ps["name"])):
            ps["deplist"].append({ "name": m.package,
                                   "versionFrom" : m.versionFrom,
                                   "exists" : isDepExists(path, m.package, m.versionFrom) })
    return pisi_list


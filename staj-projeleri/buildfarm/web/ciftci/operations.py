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

def getPisiList(path):
    pisi_list = []
    for l in os.listdir(path):
        if os.path.splitext(l)[1] == '.pisi':
            pisi_list.append({"package_name":l})
    return pisi_list

def getRuntimeDeps(p):
    metadata = (pisi.package.Package(p)).get_metadata()
    return metadata.package.runtimeDependencies()

def getPisiDict(path):
    # Returns a dictionary which contains the runtime dependencies
    # of the packages
    d = _d = {}
    for ps in getPisiList(path):
        _d[ps["package_name"]] = getRuntimeDeps(os.path.join(path, ps["package_name"]))
        d[ps["package_name"]] = map(lambda x: x.package, _d[ps["package_name"]])

    return d

def output(d):
    for x in d:
        print "package : %s" % x
        if d[x]:
            for dep in d[x]:
                print "\t=> %s versionFrom : %s" % (dep.package, str(dep.versionFrom))



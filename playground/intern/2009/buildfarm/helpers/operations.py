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

stablePath = "/home/ozan/uludag/trunk/staj-projeleri/buildfarm/pardus-2007"
testPath = "/home/ozan/uludag/trunk/staj-projeleri/buildfarm/pardus-2007-test"

def getPisiList(path):
    return [l for l in os.listdir(path) if os.path.splitext(l)[1] == '.pisi']

def getRuntimeDeps(p):
    metadata = (pisi.package.Package(p)).get_metadata()
    return metadata.package.runtimeDependencies()

def getPisiDict(path):
    # Returns a dictionary which contains the runtime dependencies
    # of the packages
    d = {}
    for ps in getPisiList(path):
        d[ps] = getRuntimeDeps(os.path.join(path, ps))

    return d

def output(d):
    for x in d:
        print "package : %s" % x
        if d[x]:
            for dep in d[x]:
                print "\t=> %s versionFrom : %s" % (dep.package, str(dep.versionFrom))



# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# dependency analyzer

# Author:  Eray Ozkural <eray@uludag.org.tr>

from installdb import installdb
import packagedb
from ui import ui
from version import Version
from xmlext import *
from xmlfile import XmlFile
from util import Checks

class DepInfo:
    def __init__(self, node = None):
        if node:
            self.package = getNodeText(node).strip()
            self.versionFrom = getNodeAttribute(node, "versionFrom")
            self.versionTo = getNodeAttribute(node, "versionTo")
            self.releaseFrom = getNodeAttribute(node, "releaseFrom")
            self.releaseTo = getNodeAttribute(node, "releaseTo")
        else:
            self.versionFrom = self.versionTo = None
            self.releaseFrom = self.releaseFrom = None

    def elt(self, xml):
        node = xml.newNode("Dependency")
        xml.addText(node, self.package)
        if self.versionFrom:
            node.setAttribute("versionFrom", self.versionFrom)
        if self.versionTo:
            node.setAttribute("versionTo", self.versionTo)
        if self.releaseFrom:
            node.setAttribute("releaseFrom", self.versionFrom)
        if self.releaseTo:
            node.setAttribute("releaseTo", self.versionTo)
        return node

    def has_errors(self):
        if not self.package:
            return [ "Dependency should have a package string" ]
        return None

    def satisfies(self, pkg_name, version, release):
        """determine if a package ver. satisfies given dependency spec"""
        ret = True
        from version import Version
        if self.versionFrom:
            ret &= Version(version) >= Version(self.versionFrom)
        if self.versionTo:
            ret &= Version(version) <= Version(self.versionTo)        
        if self.releaseFrom:
            ret &= Version(release) <= Version(self.releaseFrom)        
        if self.releaseTo:
            ret &= Version(release) <= Version(self.releaseTo)       
        return ret
        
    def __str__(self):
        s = self.package
        if self.versionFrom:
            s += 'ver >= ' + self.versionFrom
        if self.versionTo:
            s += 'ver <= ' + self.versionTo
        if self.releaseFrom:
            s += 'rel >= ' + self.releaseFrom
        if self.releaseTo:
            s += 'rel <= ' + self.releaseTo
        return s

def dictSatisfiesDep(dict, depinfo):
    """determine if a package in a dictionary satisfies given dependency spec"""
    pkg_name = depinfo.package
    if not dict.has_key(pkg_name):
        return False
    else:
        pkg = dict[pkg_name]
        (version, release) = (pkg.version, pkg.release)
        return depinfo.satisfies(pkg_name, version, release)

def installedSatisfiesDep(depinfo):
    """determine if a package in *repository* satisfies given
dependency spec"""
    pkg_name = depinfo.package
    if not installdb.is_installed(pkg_name):
        return False
    else:
        pkg = packagedb.inst_packagedb.get_package(pkg_name)
        (version, release) = (pkg.version, pkg.release)
        return depinfo.satisfies(pkg_name, version, release)

def repoSatisfiesDep(depinfo):
    """determine if a package in *repository* satisfies given
dependency spec"""
    pkg_name = depinfo.package
    if not packagedb.has_package(pkg_name):
        return False
    else:
        pkg = packagedb.get_package(pkg_name)
        (version, release) = (pkg.version, pkg.release)
        return depinfo.satisfies(pkg_name, version, release)

def satisfiesDeps(pkg, deps, sat = installedSatisfiesDep):
    for dep in deps:
        if not sat(dep):
            ui.error('Package %s does not satisfy dependency %s\n' %
                     (pkg,dep))
            return False
    return True

def satisfiesRuntimeDeps(pkg):
    deps = packagedb.get_package(pkg).runtimeDeps
    return satisfiesDeps(pkg, deps)

def installable(pkg):
    """calculate if pkg is installable currently 
    which means it has to satisfy both install and runtime dependencies"""
    if not packagedb.has_package(pkg):
        ui.info("Package " + pkg + " is not present in the package database\n");
        return False
    elif satisfiesRuntimeDeps(pkg):
        return True
    else:
        #ui.info("package " + pkg + " does not satisfy dependencies\n");
        return False


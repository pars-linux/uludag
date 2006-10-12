#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import os
import sys
import urllib2
import piksemel

def fetch_uri(base_uri, cache_dir, filename, console=None):
    # Dont cache for local repos
    # Check that local file isnt older or has missing parts
    path = os.path.join(cache_dir, filename)
    if not os.path.exists(path):
        if console:
            console.started("Fetching '%s'..." % filename)
        conn = urllib2.urlopen(os.path.join(base_uri, filename))
        output = file(path, "w")
        total_size = int(conn.info()['Content-Length'])
        size = 0
        while size < total_size:
            data = conn.read(4096)
            output.write(data)
            size += len(data)
            if console:
                console.progress("Downloaded %d of %d bytes" % (size, total_size), 100 * size / total_size)
        output.close()
        conn.close()
        if console:
            console.finished()
    return path


class Package:
    def __init__(self, node):
        self.node = node
        self.name = node.getTagData('Name')
        self.icon = node.getTagData('Icon')
        if not self.icon:
            self.icon = 'package'
        self.homepage = node.getTag('Source').getTagData('Homepage')
        self.version = node.getTag('History').getTag('Update').getTagData('Version')
        self.release = node.getTag('History').getTag('Update').getAttribute('release')
        self.build = node.getTagData('Build')
        self.size = int(node.getTagData('PackageSize'))
        self.inst_size = int(node.getTagData('InstalledSize'))
        self.uri = node.getTagData('PackageURI')
        self.component = node.getTagData('PartOf')
        self.summary = node.getTagData('Summary')
        self.description = node.getTagData('Description')
        deps = node.getTag('RuntimeDependencies')
        if deps:
            self.depends = map(lambda x: x.firstChild().data(), deps.tags('Dependency'))
        else:
            self.depends = []
        self.revdeps = []
        # Keep more info: licenses, packager name
    
    def __str__(self):
        return """Package: %s (%s)
Version %s, release %s, build %s
Size: %d, installed %d
Part of: %s
Dependencies: %s
Reverse dependencies: %s
Summary: %s""" % (
            self.name, self.uri,
            self.version, self.release, self.build,
            self.size, self.inst_size,
            self.component,
            ", ".join(self.depends),
            ", ".join(self.revdeps),
            self.summary
        )


class Component:
    def __init__(self, node):
        self.node = node
        self.name = node.getTagData('Name')
        self.packages = []
    
    def __str__(self):
        return "Component: %s\nPackages: %s" % (self.name, ", ".join(self.packages))


class Repository:
    def __init__(self, uri, cache_dir):
        self.index_name = os.path.basename(uri)
        self.base_uri = os.path.dirname(uri)
        self.cache_dir = cache_dir
        self.size = 0
        self.inst_size = 0
        self.packages = {}
        self.components = {}
        self.distribution = None
    
    def parse_index(self, console=None):
        path = fetch_uri(self.base_uri, self.cache_dir, self.index_name, console)
        if path.endswith(".bz2"):
            import bz2
            data = file(path).read()
            data = bz2.decompress(data)
            doc = piksemel.parseString(data)
        else:
            doc = piksemel.parse(path)
        self.distribution = doc.getTag('Distribution')
        for tag in doc.tags('Package'):
            p = Package(tag)
            self.packages[p.name] = p
            self.size += p.size
            self.inst_size += p.inst_size
        for tag in doc.tags('Component'):
            c = Component(tag)
            self.components[c.name] = c
        for name in self.packages:
            p = self.packages[name]
            for name2 in p.depends:
                if self.packages.has_key(name2):
                    self.packages[name2].revdeps.append(p.name)
                else:
                    print "Error: package %s depends on non existing package %s" % (p.name, name2)
            if self.components.has_key(p.component):
                self.components[p.component].packages.append(p.name)
        for name in self.packages:
            p = self.packages[name]
            for dep in p.depends:
                if dep in p.revdeps:
                    print "Error: cyclic dependency between %s and %s" % (name, dep)
    
    def make_index(self, package_list):
        doc = piksemel.newDocument("PISI")
        doc.insertNode(self.distribution)
        for name in package_list:
            doc.insertNode(self.packages[name].node)
        for name in self.components:
            doc.insertNode(self.components[name].node)
        return doc.toPrettyString()
    
    def make_local_repo(self, path, package_list):
        for name in package_list:
            p = self.packages[name]
            cached = fetch_uri(self.base_uri, self.cache_dir, p.uri)
            os.link(cached, os.path.join(path, os.path.basename(cached)))
        index = self.make_index(package_list)
        import bz2
        data = bz2.compress(index)
        import sha
        f = file(os.path.join(path, "pisi-index.xml.bz2"), "w")
        f.write(data)
        f.close()
        f = file(os.path.join(path, "pisi-index.xml.bz2.sha1sum"), "w")
        s = sha.new()
        s.update(data)
        f.write(s.hexdigest())
        f.close()
    
    def full_deps(self, package_name):
        deps = set()
        deps.add(package_name)
        def collect(name):
            p = self.packages[name]
            for item in p.depends:
                deps.add(item)
                collect(item)
        collect(package_name)
        if self.components.has_key("system.base"):
            for item in self.components["system.base"].packages:
                deps.add(item)
                collect(item)
        return deps
    
    def __str__(self):
        return """Repository: %s
Number of packages: %d
Total package size: %d
Total installed size: %d""" % (
            self.base_uri,
            len(self.packages),
            self.size,
            self.inst_size
        )

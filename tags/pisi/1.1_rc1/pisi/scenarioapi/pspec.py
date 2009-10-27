# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
# Authors:  Faik Uygur <faik@pardus.org.tr>

from pisi.specfile import SpecFile, Package, Update, Path
from pisi.dependency import Dependency
from pisi.pxml.autoxml import LocalText

class Pspec:
    def __init__(self, pkgname, filepath):
        self.pspec = SpecFile()
        self.package = Package()
        self.update = Update()
        self.filepath = filepath
        self.name = pkgname

    @staticmethod
    def read(filepath):
        spec = SpecFile()
        spec.read(filepath)
        tmp = Pspec(spec.source.name, filepath)

        tmp.pspec.source.packager = spec.source.packager
        tmp.pspec.source.homepage = spec.source.homepage
        tmp.pspec.source.archive = spec.source.archive
        tmp.pspec.source.name = spec.source.name
        tmp.pspec.source.license = spec.source.license
        tmp.pspec.source.partOf = spec.source.partOf
        tmp.pspec.source.summary = spec.source.summary
        tmp.pspec.source.description = spec.source.description

        for pkg in spec.packages:
            p = Package()
            p.name = pkg.name
            p.files = pkg.files
            p.conflicts = pkg.conflicts
            p.packageDependencies = pkg.packageDependencies
            tmp.pspec.packages.append(p)

        tmp.pspec.history = spec.history
        return tmp

    def add_dependencies(self, dependencies):
        # special case of given one dependency package
        # with depedency versioning info [**kw, name]
        # [{"versionFrom":"0.4.2"}, "udev"]
        if type(dependencies[0]) == dict:
            dep = Dependency()
            (kw, dep.package) = dependencies
            dep.__dict__[kw.keys()[0]] = kw.values()[0]
            self.package.packageDependencies.append(dep)
            return

        for depname in dependencies:
            dep = Dependency()
            dep.package = depname
            self.package.packageDependencies.append(dep)

    def remove_dependencies(self, dependencies):
        for depname in dependencies:
            for dep in self.package.packageDependencies:
                if dep.package == depname:
                    self.package.packageDependencies.remove(dep)

    def add_conflicts(self, conflicts):
        for con in conflicts:
            self.package.conflicts.append(con)

    def remove_conflicts(self, conflicts):
        for con in conflicts:
            self.package.conflicts.remove(con)

    def update_history(self, date, version):
        new = Update()
        new.name = self.update.name
        new.email = self.update.email
        new.date = date
        new.version = version
        new.release = str(int(self.update.release) + 1)
        self.update = new
        self.pspec.history.append(self.update)
        self.pspec.history.reverse()
        self.write()

    def set_source(self, homepage, summary, description, license, partOf):
        self.pspec.source.name = self.name
        self.pspec.source.homepage = homepage
        self.pspec.source.license = license
        self.pspec.source.partOf = partOf
        self.pspec.source.summary = LocalText("Summary")
        self.pspec.source.description = LocalText("Description")
        self.pspec.source.summary["en"] = summary
        self.pspec.source.description["en"] = description

    def set_packager(self, name, email):
        self.pspec.source.packager.name = unicode(name)
        self.pspec.source.packager.email = email
        self.update.name = unicode(name)
        self.update.email = email

    def set_archive(self, sha1sum, type, uri):
        self.pspec.source.archive.sha1sum = sha1sum
        self.pspec.source.archive.type = type
        self.pspec.source.archive.uri = uri

    def add_file_path(self, path, type):
        p = Path()
        p.path = path
        p.fileType = type
        self.pspec.packages[0].files.append(p)

    def set_package(self, dependencies, conflicts):
        self.package.name = self.name
        self.package.conflicts = conflicts

        if dependencies:
            for depname in dependencies:
                dep = Dependency()
                dep.package = depname
                self.package.packageDependencies.append(dep)

        self.pspec.packages.append(self.package)

    def set_history(self, date, version, comment = "No Comment", release = "1"):
        self.update.date = date
        self.update.version = version
        self.update.comment = comment
        self.update.release = release
        self.pspec.history.append(self.update)

    def write(self):
        self.pspec.write(self.filepath)

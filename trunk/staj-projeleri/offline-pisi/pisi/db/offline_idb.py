# -*- coding: utf-8 -*-
#
# Copyright (C) 2005 - 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
#
# installation database
#

import re
import gzip
import gettext
__trans = gettext.translation('pisi', fallback=True)
_ = __trans.ugettext

import piksemel

#PISI
import pisi.metadata
import pisi.dependency

class Offline_InstallDB():

    def __init__(self):
        self.pdb = pisi.db.packagedb.PackageDB()

        #index_xml = "/home/volkan/index/pardus-2009/pisi-installed.xml"
        f = open("/tmp/offline-pm.data", "r")
        index_xml = f.read()
        f.close()
        doc = piksemel.parse(index_xml)

        self.installed_db = self.__generate_installed_pkgs(doc)
        self.rev_deps_db = self.__generate_revdeps(doc)

    def __generate_installed_pkgs(self, doc):
        return dict(map(lambda x: (x.getTagData("Name"), gzip.zlib.compress(x.toString())), doc.tags("Package")))

    def __generate_revdeps(self, doc):
        revdeps = {}
        for node in doc.tags("Package"):
            name = node.getTagData('Name')
            deps = node.getTag('RuntimeDependencies')
            if deps:
                for dep in deps.tags("Dependency"):
                    revdeps.setdefault(dep.firstChild().data(), set()).add((name, dep.toString()))
        return revdeps

    def __add_to_revdeps(self, package, revdeps):
        data = gzip.zlib.decompress(self.installed_db[package])
        doc = piksemel.parseString(data)
        name = doc.getTag('Name')
        deps = doc.getTag('RuntimeDependencies')

        if deps:
            for dep in deps.tags("Dependency"):
                revdeps.setdefault(dep.firstChild().data(), set()).add((name, dep.toString()))

    def get_package(self, name):
        pkg = self.package_data(name)
        package = pisi.metadata.Package()
        package.parse(pkg)
        return package

    def list_installed(self):
        return self.installed_db.keys()

    def has_package(self, package):
        return self.installed_db.has_key(package)

    def __get_version(self, pkg):
        return pkg.version, pkg.release, pkg.build and int(pkg.build)

    def __get_distro_release(self, pkg):
        return pkg.distribution, pkg.distributionRelease

    def get_version_and_distro_release(self, package):
        pkg = self.get_package(package)
        return self.__get_version(pkg) + self.__get_distro_release(pkg)

    def get_version(self, package):
        pkg = self.get_package(package)
        return pkg.version, pkg.release, pkg.build

    def get_files(self, package):
        # return empty
        files = pisi.files.Files()
        return files

    def get_isa_packages(self, isa):
        # DENENMEDI
        risa = '<IsA>%s</IsA>' % isa
        packages = []
        for name in self.list_installed():
            xml = self.package_data(name)
            if re.compile(risa).search(xml):
                packages.append(name)
        return packages

    def get_rev_deps(self, name):

        rev_deps = []

        if self.rev_deps_db.has_key(name):
            for pkg, dep in self.rev_deps_db[name]:
                node = piksemel.parseString(dep)
                dependency = pisi.dependency.Dependency()
                dependency.package = node.firstChild().data()
                if node.attributes():
                    attr = node.attributes()[0]
                    dependency.__dict__[attr] = node.getAttribute(attr)
                rev_deps.append((pkg, dependency))

        return rev_deps

    def search_package(self, terms, lang=None):
        resum = '<Summary xml:lang=.(%s|en).>.*?%s.*?</Summary>'
        redesc = '<Description xml:lang=.(%s|en).>.*?%s.*?</Description>'
        if not lang:
            lang = pisi.pxml.autoxml.LocalText.get_lang()
        found = []
        for name in self.list_installed():
            xml = gzip.zlib.decompress(self.installed_db[name])
            if terms == filter(lambda term: re.compile(term, re.I).search(name) or \
                                            re.compile(resum % (lang, term), re.I).search(xml) or \
                                            re.compile(redesc % (lang, term), re.I).search(xml), terms):
                found.append(name)
        return found

    def add_package(self, name):
        pkg = self.pdb.pdb.get_item(name)
        self.installed_db.setdefault(name, gzip.zlib.compress(pkg))
        self.__add_to_revdeps(name, self.rev_deps_db)

    def remove_package(self, package_name):
        if self.installed_db.has_key(package_name):
            del self.installed_db[package_name]

    def package_data(self, package):
        if self.installed_db.has_key(package):
            pkg = gzip.zlib.decompress(self.installed_db[package])
            return pkg

        raise Exception(_('Package %s is not installed') % package)

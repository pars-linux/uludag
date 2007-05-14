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

"""
Metadata module provides access to metadata.xml. metadata.xml is
generated during the build process of a package and used in the
installation. Package repository also uses metadata.xml for building
a package index.
"""

import gettext
__trans = gettext.translation('pisi', fallback=True)
_ = __trans.ugettext

import pisi.context as ctx
import pisi.specfile as specfile
import autoxml
import pisi.util as util


class Delta(autoxml.AutoXML):
    buildFrom = autoxml.Attribute("buildFrom", autoxml.optional)
    packageURI = autoxml.Tag("PackageURI", autoxml.optional)
    packageSize = autoxml.Tag("PackageSize", autoxml.optional)
    packageHash = autoxml.Tag("SHA1Sum", autoxml.optional)
    
    def validate(self, ctx):
        self.packageSize = long(self.packageSize)


class Source(autoxml.AutoXML):
    name = autoxml.Tag("Name")
    homepage = autoxml.Tag("Homepage", autoxml.optional)
    packager = autoxml.Tag("Packager", specfile.Packager)


class Package(specfile.Package):
    build = autoxml.Tag("Build", autoxml.optional)
    distribution = autoxml.Tag("Distribution")
    distributionRelease = autoxml.Tag("DistributionRelease")
    architecture = autoxml.Tag("Architecture")
    installedSize = autoxml.Tag("InstalledSize")
    packageSize = autoxml.Tag("PackageSize", autoxml.optional)
    packageHash = autoxml.Tag("SHA1Sum", autoxml.optional)
    packageURI = autoxml.Tag("PackageURI", autoxml.optional)
    deltaPackages = autoxml.Tag("DeltaPackages", autoxml.optional)
    packageFormat = autoxml.Tag("PackageFormat", autoxml.optional)
    source = autoxml.Tag("Source", autoxml.optional, Source)

    def get_delta(self, buildFrom):
        for delta in self.deltaPackages:
            if delta.buildFrom == str(buildFrom):
                return delta
        else:
            return None

    def validate(self, ctx):
        self.build = int(self.build)
        self.installedSize = long(self.installedSize)
        self.packageSize = long(self.packageSize)
        
        self.version = self.history[0].version
        self.release = self.history[0].release

    def __str__(self):
        s = specfile.Package.__str__(self)
        s += _('Distribution: %s, Dist. Release: %s\n') % \
              (self.distribution, self.distributionRelease)
        s += _('Architecture: %s, Installed Size: %s') % \
            (self.architecture, self.installedSize)
        return s


class MetaData((autoxml.AutoXML)):
    """Package metadata. Metadata is composed of Specfile and various
    other information. A metadata has two parts, Source and Package."""
    
    source = autoxml.Tag("Source", Source)
    package = autoxml.Tag("Package", Package)
    #t_History = [ [Update], autoxml.mandatory]

    def from_spec(self, src, pkg, history):
        # this just copies fields, it doesn't fix every necessary field
        self.source.name = src.name
        self.source.homepage = src.homepage
        self.source.packager = src.packager
        self.package.source = self.source # FIXME: I know that replication sucks here, but this is the easiest for now-- exa
        self.package.name = pkg.name
        self.package.summary = pkg.summary
        self.package.description = pkg.description
        self.package.icon = pkg.icon
        # merge pkg.isA with src.isA
        pkg.isA.extend(src.isA)
        self.package.isA = pkg.isA
        self.package.partOf = pkg.partOf
        self.package.license = pkg.license
        self.package.packageDependencies = pkg.packageDependencies
        self.package.componentDependencies = pkg.componentDependencies
        self.package.files = pkg.files
        # FIXME: no need to copy full history with comments
        self.package.history = history
        self.package.conflicts = pkg.conflicts
        self.package.providesComar = pkg.providesComar
        #self.package.requiresComar = pkg.requiresComar
        self.package.additionalFiles = pkg.additionalFiles

        # FIXME: right way to do it?
        self.source.version = src.version
        self.source.release = src.release
        self.package.version = src.version
        self.package.release = src.release

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
 Specfile module is our handler for PSPEC files. PSPEC (PiSi SPEC)
 files are specification files for PiSi source packages. This module
 provides read and write routines for PSPEC files.
"""

import gettext
__trans = gettext.translation('pisi', fallback=True)
_ = __trans.ugettext

# standard python modules
import os.path

# pisi modules
import autoxml
import pisi.context as ctx
import pisi.dependency
import pisi.conflict
import pisi.component as component
import pisi.util as util


class Error(pisi.Error):
    pass

class Packager(autoxml.AutoXML):
    name  = autoxml.Tag("Name")
    email = autoxml.Tag("Email")

    def __str__(self):
        s = "%s <%s>" % (self.name, self.email)
        return s


class AdditionalFile(autoxml.AutoXML):
    filename   = autoxml.CharacterData()
    target     = autoxml.Attribute("target")
    owner      = autoxml.Attribute("owner", autoxml.optional)
    group      = autoxml.Attribute("group", autoxml.optional)
    permission = autoxml.Attribute("permission", autoxml.optional)

    def __str__(self):
        s = "%s -> %s " % (self.filename, self.target)
        if self.permission:
            s += '(%s)' % self.permission
        return s

class Patch(autoxml.AutoXML):
    filename    = autoxml.CharacterData()
    compression = autoxml.Attribute("compressionType", autoxml.optional)
    level       = autoxml.Attribute("level", autoxml.optional)
    target      = autoxml.Attribute("target", autoxml.optional)
    
    def validate(self, ctx):
        if self.level:
            self.level = int(self.level)
        else:
            self.level = 0

    def __str__(self):
        s = self.filename
        if self.compressionType:
            s += ' (' + self.compressionType + ')'
        if self.level:
            s += ' level:' + self.level
        return s


class Update(autoxml.AutoXML):
    release = autoxml.Attribute("release")
    type    = autoxml.Attribute("type", autoxml.optional, ("security", "bug"))
    date    = autoxml.Tag("Date")
    version = autoxml.Tag("Version")
    name    = autoxml.Tag("Name")
    email   = autoxml.Tag("Email")
    comment = autoxml.Tag("Comment")

    def __str__(self):
        s = self.date
        s += ", ver=" + self.version
        s += ", rel=" + self.release
        if self.type:
            s += ", type=" + self.type
        return s


class Path(autoxml.AutoXML):
    filetypes = (
        "executable",
        "library",
        "data",
        "config",
        "doc",
        "man",
        "info",
        "localedata",
        "header",
    )
    path      = autoxml.CharacterData()
    filetype  = autoxml.Attribute("fileType", filetypes)
    permanent = autoxml.Attribute("permanent", autoxml.optional, ("true", "false"))

    def __str__(self):
        s = self.path
        s += ", type=" + self.fileType
        return s


class ComarProvide(autoxml.AutoXML):
    om     = autoxml.CharacterData()
    script = autoxml.Attribute("script")

    def __str__(self):
        # FIXME: descriptive enough?
        s = self.script
        s += ' (' + self.om + ')'
        return s

class Archive(autoxml.AutoXML):
    uri     = autoxml.CharacterData()
    type    = autoxml.Attribute("type")
    sha1sum = autoxml.Attribute("sha1sum")

    def validate(self, ctx):
        self.name = os.path.basename(self.uri)

    def __str__(self):
        s = _('URI: %s, type: %s, sha1sum: %s') % (self.uri, self.type, self.sha1sum)
        return s


class Source(autoxml.AutoXML):
    name        = autoxml.Tag("Name")
    homepage    = autoxml.Tag("Homepage")
    packager    = autoxml.Tag("Packager", Packager)
    summary     = autoxml.TagLocalized("Summary")
    description = autoxml.TagLocalized("Description", autoxml.optional)
    isa         = autoxml.Tag("IsA", autoxml.optional, autoxml.multiple)
    partOf      = autoxml.Tag("PartOf", autoxml.optional)
    icon        = autoxml.Tag("Icon", autoxml.optional)
    license     = autoxml.Tag("License", autoxml.multiple)
    archive     = autoxml.Tag("Archive", Archive)
    patches     = autoxml.TagCollection("Patches", "Patch", Patch, autoxml.optional)
    build_deps  = autoxml.TagCollection("BuildDependencies","Dependency", pisi.dependency.Dependency, autoxml.optional)
    # Following are found in the index, not in pspecs
    version     = autoxml.Tag("Version", autoxml.optional)
    release     = autoxml.Tag("Release", autoxml.optional)
    sourceURI   = autoxml.Tag("SourceURI", autoxml.optional)


class RuntimeDeps(autoxml.AutoXML):
    packages   = autoxml.Tag("Dependency", pisi.dependency.Dependency, autoxml.optional, autoxml.multiple)
    components = autoxml.Tag("Component", pisi.component.Component, autoxml.optional, autoxml.multiple)


class Package(autoxml.AutoXML):
    name           = autoxml.Tag("Name")
    summary        = autoxml.TagLocalized("Summary", autoxml.optional)
    description    = autoxml.TagLocalized("Description", autoxml.optional)
    isa            = autoxml.Tag("IsA", autoxml.optional, autoxml.multiple)
    partof         = autoxml.Tag("PartOf", autoxml.optional)
    icon           = autoxml.Tag("Icon", autoxml.optional)
    license        = autoxml.Tag("License", autoxml.optional, autoxml.multiple)
    runtime_deps   = autoxml.Tag("RuntimeDependencies", RuntimeDeps, autoxml.optional)
    files          = autoxml.TagCollection("Files", "Path", Path)
    conflicts      = autoxml.TagCollection("Conflicts", "Package", autoxml.optional)
    provides       = autoxml.TagCollection("Provides", "COMAR", ComarProvide, autoxml.optional)
    additionals    = autoxml.TagCollection("AdditionalFiles",
                                   "AdditionalFile", AdditionalFile, autoxml.optional)
    history        = autoxml.TagCollection("History", "Update", Update, autoxml.optional)

    # FIXME: needed in build process, to distinguish dynamically generated debug packages.
    # find a better way to do this.
    debug_package = False

    def runtimeDependencies(self):
        deps = self.packageDependencies
        deps += [ ctx.componentdb.get_component[x].packages for x in self.componentDependencies ]
        return deps

    def pkg_dir(self):
        packageDir = self.name + '-' \
                     + self.version + '-' \
                     + self.release

        return util.join_path( ctx.config.lib_dir(), 'package', packageDir)

    def installable(self):
        """calculate if pkg is installable currently"""
        deps = self.runtimeDependencies()
        return pisi.dependency.satisfies_dependencies(self.name, deps)

    def __str__(self):
        if self.build:
            build = self.build
        else:
            build = '--'
        s = _('Name: %s, version: %s, release: %s, build %s\n') % (
              self.name, self.version, self.release, build)
        s += _('Summary: %s\n') % unicode(self.summary)
        s += _('Description: %s\n') % unicode(self.description)
        s += _('Component: %s\n') % unicode(self.partOf)
        s += _('Provides: ')
        for x in self.providesComar:
           s += x.om + ' '
        s += '\n'
        s += _('Dependencies: ')
        for x in self.componentDependencies:
           s += x.package + ' '
        for x in self.packageDependencies:
           s += x.package + ' '
        return s + '\n'


class SpecFile(autoxml.AutoXML):
    source   = autoxml.Tag("Source", Source)
    packages = autoxml.Tag("Package", Package, autoxml.multiple)
    history  = autoxml.TagCollection("History", "Update", Update)
    
    # FIXME: autoxml!!!!!!!!!!
    #t_Components = [ [component.Component], autoxml.optional, "Component"]

    def getSourceVersion(self):
        return self.history[0].version

    def getSourceRelease(self):
        return self.history[0].release

    def dirtyWorkAround(self):
        #TODO: Description should be mandatory. Remove this code when repo is ready.
        #http://liste.pardus.org.tr/gelistirici/2006-September/002332.html
        self.source.description = autoxml.LocalText("Description")
        self.source.description["en"] = self.source.summary["en"]

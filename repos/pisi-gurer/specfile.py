#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

from xmlutil import *
from dependency import DepInfo

class PackagerInfo:
    
    xmldefs = [
        [ TEXT, SINGLE, "Name", "name" ],
        [ TEXT, SINGLE, "Email", "email" ]
    ]
    
    def __init__(self, node = None):
        pass
    
    def __str__(self):
        s = " ".join(self.name, self.email)
        return s


class AdditionalFileInfo:
    
    xmldefs = [
        [ TEXT, SINGLE, "", "filename" ],
        [ ATTRIBUTE, 0, "", "target", "target" ],
        [ ATTRIBUTE, OPTIONAL, "", "permission", "permission" ]
    ]
    
    def __init__(self, node = None):
        pass
    
    def __str__(self):
        s = "->".join(self.filename, self.target)
        s += s + '(' + self.permission + ')'
        return s


class PatchInfo:
    
    xmldefs = [
        [ TEXT, SINGLE, "", "filename" ],
        [ ATTRIBUTE, OPTIONAL, "", "compressionType", "compressionType" ],
        [ ATTRIBUTE, OPTIONAL, "", "level", "level" ],
        [ ATTRIBUTE, OPTIONAL, "", "target", "target" ],
    ]
    
    def __init__(self, node = None):
        pass
    
    def __str__(self):
        s = self.filename
        s += ' (' + self.compressionType + ')'
        s += ' level:' + self.level
        return s


class UpdateInfo:
    
    xmldefs = [
        [ TEXT, SINGLE, "Date", "date" ],
        [ TEXT, SINGLE, "Version", "version" ],
        [ TEXT, SINGLE, "Release", "release" ],
        [ TEXT, SINGLE | OPTIONAL, "type", "Type" ]
    ]
    
    def __init__(self, node = None):
        pass
    
    def __str__(self):
        s = self.date
        s += ", ver=" + self.version
        s += ", rel=" + self.release
        s += ", type=" + self.type
        return s


class PathInfo:
    """A structure to hold path information."""
    
    xmldefs = [
        [ TEXT, SINGLE, "", "pathname" ],
        [ ATTRIBUTE, 0, "", "fileType", "fileType" ]
    ]
    
    def __init__(self, node=None):
        pass
    
    def __str__(self):
        s = self.pathname
        s += ", type=" + self.fileType
        return s


class ComarProvide:
    
    xmldefs = [
        [ TEXT, SINGLE, "", "om" ],
        [ ATTRIBUTE, OPTIONAL, "", "script", "script" ]
    ]
    
    def __init__(self, node = None):
        pass
    
    def __str__(self):
        s = self.script
        s += ' (' + self.om + ')'
        return s


class SourceInfo:
    """A structure to hold information about package source."""
    
    xmldefs = [
        [ TEXT, SINGLE, "Name", "name" ],
        [ TEXT, SINGLE, "Homepage", "homepage" ],
        [ LOCALTEXT, 0, "Summary", "summary" ],
        [ LOCALTEXT, 0, "Description", "description" ],
        [ TEXT, MULTIPLE, "License", "license" ],
        [ TEXT, SINGLE | OPTIONAL, "PartOf", "partof" ],
        [ TEXT, MULTIPLE | OPTIONAL, "IsA", "isa" ],
        [ TEXT, SINGLE, "Archive", "archiveUri" ],
        [ ATTRIBUTE, SINGLE, "Archive", "type", "archiveType" ],
        [ ATTRIBUTE, SINGLE, "Archive", "sha1sum", "archiveSHA1" ],
        [ CLASS, SINGLE, "Packager", PackagerInfo, "packager" ],
        [ CLASS, MULTIPLE | OPTIONAL, "Patches/Patch", PatchInfo, "patches" ],
        [ CLASS, MULTIPLE | OPTIONAL, "BuildDependencies/Dependency", DepInfo, "buildDeps" ],
        [ CLASS, MULTIPLE, "History/Update", UpdateInfo, "history" ]
    ]
    
    def __init__(self, node=None):
        pass


class PackageInfo:
    """blah"""
    
    xmldefs = [
        [ TEXT, SINGLE, "Name", "name" ],
        [ LOCALTEXT, OPTIONAL, "Summary", "summary" ],
        [ LOCALTEXT, OPTIONAL, "Description", "description" ],
        [ TEXT, MULTIPLE | OPTIONAL, "IsA", "isa" ],
        [ TEXT, SINGLE | OPTIONAL, "PartOf", "partof" ],
        [ TEXT, MULTIPLE | OPTIONAL, "License", "license" ],
        [ CLASS, MULTIPLE, "Files/Path", PathInfo, "paths" ],
        [ CLASS, MULTIPLE | OPTIONAL, "RuntimeDependencies/Dependency", DepInfo, "runtimeDeps" ],
        [ TEXT, MULTIPLE | OPTIONAL, "Conflicts/Package", "conflics" ],
        [ CLASS, MULTIPLE | OPTIONAL, "History/Update", UpdateInfo, "history" ],
        [ CLASS, MULTIPLE | OPTIONAL, "Provides/COMAR", ComarProvide, "providesComar" ],
        [ CLASS, MULTIPLE | OPTIONAL, "Requires/COMAR", ComarProvide, "requiresComar" ],
        [ CLASS, MULTIPLE | OPTIONAL, "AdditionalFiles/AdditionalFile", AdditionalFileInfo, "additionalFiles" ]
    ]
    
    def __init__(self, node=None):
        pass
    
    def __str__(self):
        s = 'Name: ' + self.name
        s += '\nSummary: ' + self.summary
        s += '\nDescription: ' + self.description
        return s
    
    def pkg_dir(self):
        packageDir = self.name + '-' \
                     + self.version + '-' \
                     + self.release

        return join( config.lib_dir(), packageDir)


class SpecFile:
    """Pisi spec file (pspec.xml) class."""
    
    xmldefs = [
        [ ROOT, "PISI" ],
        [ CLASS, SINGLE, "Source", SourceInfo, "source" ],
        [ CLASS, MULTIPLE, "Package", PackageInfo, "packages" ]
    ]
    
    def __init__(self, fileName=None):
        readXmlFile(self, fileName)
        self.source.version = self.source.history[0].version
        self.source.release = self.source.history[0].release
        self.merge_tags()
        self.override_tags()
    
    def override_tags(self):
        """Override tags from Source in Packages. Some tags in Packages
        overrides the tags from Source. There is a more detailed
        description in documents."""
    
        for pkg in self.packages:
            
            if not pkg.summary:
                pkg.summary = self.source.summary
            
            if not pkg.description:
                pkg.description = self.source.description
            
            if not pkg.partof:
                pkg.partof = self.source.partof
            
            if not pkg.license:
                pkg.license = self.source.license
    
    def merge_tags(self):
        """Merge tags from Source in Packages. Some tags in Packages merged
        with the tags from Source. There is a more detailed
        description in documents."""
        
        if self.source.isa:
            for pkg in self.packages:
                if pkg.isa:
                    pkg.isa.append(self.source. isa)
                else:
                    pkg.isa = self.source.isa





def test():
    try:
        a = SpecFile("pspec.xml")
    except XmlError, inst:
        print "Error:\n", str(inst)
        return
    print a.source.name
    print a.source.isa
    print a.source.partof
    print a.packages[0].name
    print a.packages[0].isa
    print a.packages[0].partof
    for p in a.packages[0].paths:
        print p.fileType, p.pathname

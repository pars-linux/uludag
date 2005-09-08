#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

pspec_tags = [
    "PISI",
    "Source",
    "Package",
    "Name",
    "Homepage",
    "Packager",
    "Email",
    "License",
    "IsA",
    "PartOf",
    "Summary",
    "Description",
    "Patches",
    "Patch",
    "AdditionalFiles",
    "AdditionalFile",
    "BuildDependencies",
    "Dependency",
    "History",
    "Update",
    "Date",
    "Version",
    "Release",
    "RuntimeDependencies",
    "Files",
    "Path"
]

pspec_attributes = [
    "xml:lang",
    "type",
    "sha1sum",
    "version",
    "versionFrom",
    "versionTo",
    "compressionType",
    "level",
    "fileType"
]

pspec_filetypes = [
    "doc",
    "executable",
    "data",
    "library",
    "header",
    "man",
    "config",
    "other",
    "localedata",
    "info"
]

pspec_xml = u"""<?xml version="1.0" encoding="utf-8" standalone="no"?>
<!DOCTYPE PISI SYSTEM "http://www.uludag.org.tr/projeler/pisi/pisi-spec.dtd">

<PISI>
    <Source>
        <Name>%(PACKAGE)s</Name>
        <Homepage>http://uludag.org.tr</Homepage>
        <Packager>
            <Name>%(NAME)s</Name>
            <Email>%(EMAIL)s</Email>
        </Packager>
        <License>GPL-2</License>
        <IsA></IsA>
        <PartOf></PartOf>
        <Summary xml:lang="en">An application</Summary>
        <Description xml:lang="en">An application</Description>
        <Archive type="tarbz" sha1sum="12">http://uludag.org.tr/nothing.tar.bz2</Archive>
        <Patches>
        </Patches>
        <BuildDependencies>
        </BuildDependencies>
        <History>
            <Update>
                <Date>%(DATE)s</Date>
                <Version>1.0</Version>
                <Release>1</Release>
            </Update>
        </History>
    </Source>

    <Package>
        <Name>%(PACKAGE)s</Name>
        <Files>
            <Path fileType="data">/</Path>
        </Files>
   </Package>
</PISI>
"""

actions_py = u"""#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright © 2005  TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.
#
# %(NAME)s <%(EMAIL)s>

from pisi.actionsapi import autotools
from pisi.actionsapi import shelltools
from pisi.actionsapi import pisitools

def setup():
    autotools.configure("--with-something")

def build():
    autotools.make()

def install():
    autotools.install()
    pisitools.dodoc("ChangeLog", "AUTHORS", "INSTALL*", "NEWS", "README*")

"""

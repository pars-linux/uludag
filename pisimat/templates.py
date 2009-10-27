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
    "Comment",
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
    "fileType",
    "release"
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
    "info",
    "all"
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
        <Summary>An application</Summary>
        <Description>An application</Description>
        <Archive type="tarbz" sha1sum="12">http://uludag.org.tr/nothing.tar.bz2</Archive>
        <Patches>
        </Patches>
        <BuildDependencies>
        </BuildDependencies>
    </Source>

    <Package>
        <Name>%(PACKAGE)s</Name>
        <RuntimeDependencies>
        </RuntimeDependencies>
        <Files>
            <Path fileType="data">/</Path>
        </Files>
   </Package>

   <History>
        <Update release="1">
            <Date>%(DATE)s</Date>
            <Version>1.0</Version>
            <Comment>First release.</Comment>
            <Name>%(NAME)s</Name>
            <Email>%(EMAIL)s</Email>
        </Update>
    </History>
</PISI>
"""

pspec_release = """
        <Update release="%(RELEASE)s">
            <Date>%(DATE)s</Date>
            <Version>%(VERSION)s</Version>
            <Comment>Update</Comment>
            <Name>%(NAME)s</Name>
            <Email>%(EMAIL)s</Email>
        </Update>"""

actions_api = [
    # get
    "get.curDIR",
    "get.curKERNEL",
    "get.ENV",
    "get.pkgDIR",
    "get.workDIR",
    "get.installDIR",
    "get.srcNAME",
    "get.srcVERSION",
    "get.srcRELEASE",
    "get.srcTAG",
    "get.srcDIR",
    "get.HOST",
    "get.CHOST",
    "get.CFLAGS",
    "get.CXXFLAGS",
    "get.LDFLAGS",
    "get.docDIR",
    "get.sbinDIR",
    "get.infoDIR",
    "get.manDIR",
    "get.dataDIR",
    "get.confDIR",
    "get.localstateDIR",
    "get.defaultprefixDIR",
    "get.kdeDIR",
    "get.qtDIR",
    "get.qtLIBDIR",
    "get.existBinary",
    "get.getBinutilsInfo",
    "get.AR",
    "get.AS",
    "get.CC",
    "get.CXX",
    "get.LD",
    "get.NM",
    "get.RANLIB",
    "get.F77",
    "get.GCJ",
    # pisitools
    "pisitools.dobin",
    "pisitools.dodir",
    "pisitools.dodoc",
    "pisitools.doexe",
    "pisitools.dohard",
    "pisitools.dohtml",
    "pisitools.doinfo",
    "pisitools.dolib",
    "pisitools.dolib_a",
    "pisitools.dolib_so",
    "pisitools.doman",
    "pisitools.domo",
    "pisitools.domove",
    "pisitools.rename",
    "pisitools.dosed",
    "pisitools.dosbin",
    "pisitools.dosym",
    "pisitools.insinto",
    "pisitools.newdoc",
    "pisitools.newman",
    "pisitools.remove",
    "pisitools.removeDir",
    # libtools
    "libtools.preplib",
    "libtools.gnuconfig_update",
    "libtools.libtoolize",
    "libtools.gen_usr_ldscript",
    # shelltools
    "shelltools.can_access_file",
    "shelltools.can_access_directory",
    "shelltools.makedirs",
    "shelltools.echo",
    "shelltools.chmod",
    "shelltools.chown",
    "shelltools.sym",
    "shelltools.unlink",
    "shelltools.unlinkDir",
    "shelltools.move",
    "shelltools.copy",
    "shelltools.copytree",
    "shelltools.touch",
    "shelltools.cd",
    "shelltools.ls",
    "shelltools.export",
    "shelltools.isLink",
    "shelltools.isFile",
    "shelltools.isDirectory",
    "shelltools.realPath",
    "shelltools.baseName",
    "shelltools.dirName",
    "shelltools.system",
    # pythonmodules
    "pythonmodules.compile",
    "pythonmodules.install",
    "pythonmodules.run",
    # perlmodules
    "perlmodules.configure",
    "perlmodules.make",
    "perlmodules.install",
    # kde
    "kde.configure",
    "kde.make",
    "kde.install",
    # scons
    "scons.make",
    "scons.install"
]

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

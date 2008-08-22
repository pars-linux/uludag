# -*- coding: utf-8 -*-

pspecTemplate = u"""<?xml version="1.0" encoding="utf-8" standalone="no"?>
<!DOCTYPE PISI SYSTEM "http://www.uludag.org.tr/projeler/pisi/pisi-spec.dtd">

<PISI>
    <Source>
        <Name>%(package)s</Name>
        <Homepage>%(homepage)s</Homepage>
        <Packager>
            <Name>%(packagername)s</Name>
            <Email>%(packageremail)s</Email>
        </Packager>
        <License>%(license)s</License>
        <IsA>%(isa)s</IsA>
	<PartOf>%(partof)s</PartOf>
        <Summary>%(summary)s</Summary>
        <Archive type="%(archivetype)s" sha1sum="%(archivesha1)s">%(archiveuri)s</Archive>
    </Source>
    <Package>
        <Name>%(package)s</Name>
        <Files>
            <Path fileType="data">/</Path>
        </Files>
    </Package>
    <History>
        <Update release="1">
            <Date>%(date)s</Date>
            <Version>%(version)s</Version>
            <Comment>First release.</Comment>
            <Name>%(packagername)s</Name>
            <Email>%(packageremail)s</Email>
        </Update>
    </History>
</PISI>
"""

actionspyTemplate = u"""#!/usr/bin/python
# -*- coding: utf-8 -*-·
#
# Copyright 2005 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.
#
# %(packagername)s %(packageremail)s

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    pass

def build():
    pass

def install():
    pass

"""

translationTemplate = u"""<?xml version="1.0" ?>
<PISI>
    <Source>
        <Name>%(source)s</Name>
        <Summary xml:lang="%(lang)s">%(summary)s</Summary>
    </Source>
</PISI>
"""

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

import os
import sys
import piksemel as iks
from pisi import zipfileext

files = {}

def pisi_paks(path):
    paks = []
    for root, dirs, files in os.walk(path):
        for fn in files:
            if fn.endswith(".pisi"):
                paks.append(os.path.join(root, fn))
    return paks

def parse_paks():
    for pisi in pisi_paks(sys.argv[1]):
        zip = zipfileext.ZipFileExt(pisi, "r")
        data = zip.read("metadata.xml")
        doc = iks.parseString(data)
        name = doc.getTag("Package").getTagData("Name")
        data = zip.read("files.xml")
        doc = iks.parseString(data)
        for fi in doc.tags("File"):
            path = fi.getTagData("Path")
            if files.has_key(path):
                print "Package '%s' and '%s' has same file\n  %s\n" % (files[path], name, path)
            else:
                files[path] = name

parse_paks()


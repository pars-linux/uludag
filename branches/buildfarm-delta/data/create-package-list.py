#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2008 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

import sys
import bz2

import piksemel

def parseRepoIndex(index):
    """Method for parsing repo index into a comma separated file containing only
    package name, version and release information."""

    if index.endswith("bz2"):
        doc = piksemel.parseString(bz2.decompress(file(index).read()))
    else:
        doc = piksemel.parse(index)

    return [p.getTagData("PackageURI") for p in doc.tags("Package")]

if __name__ == "__main__":
    print "\n".join(parseRepoIndex(sys.argv[1]))


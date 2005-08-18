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

class PathInfo:
    """A structure to hold path information."""
    
    xmldefs = [
        [ TEXT, SINGLE, "", "pathname" ],
        [ ATTRIBUTE, 0, "", "fileType", "fileType" ]
    ]
    
    def __init__(self, node=None):
        pass


class SourceInfo:
    """A structure to hold information about package source."""
    
    xmldefs = [
        [ TEXT, SINGLE, "Name", "name" ],
        [ TEXT, SINGLE, "Homepage", "homepage" ],
        [ TEXT, SINGLE, "Summary", "summary" ],
        [ TEXT, SINGLE, "Description", "description" ],
        [ TEXT, MULTIPLE, "License", "license" ],
        [ TEXT, SINGLE | OPTIONAL, "PartOf", "partof" ],
        [ TEXT, MULTIPLE | OPTIONAL, "IsA", "isa" ],
        [ TEXT, SINGLE, "Archive", "archiveUri" ],
        [ ATTRIBUTE, SINGLE, "Archive", "type", "archiveType" ],
        [ ATTRIBUTE, SINGLE, "Archive", "sha1sum", "archiveSHA1" ]
    ]
    
    def __init__(self, node=None):
        pass


class PackageInfo:
    """blah"""
    
    xmldefs = [
        [ TEXT, SINGLE, "Name", "name" ],
        [ TEXT, SINGLE | OPTIONAL, "Summary", "summary" ],
        [ TEXT, SINGLE | OPTIONAL, "Description", "description" ],
        [ TEXT, MULTIPLE | OPTIONAL, "IsA", "isa" ],
        [ TEXT, SINGLE | OPTIONAL, "PartOf", "partof" ],
        [ TEXT, MULTIPLE | OPTIONAL, "License", "license" ],
        [ CLASS, MULTIPLE, "Files/Path", PathInfo, "paths" ],
    ]
    
    def __init__(self, node=None):
        pass
 

class SpecFile:
    """Pisi spec file (pspec.xml) class."""
    
    xmldefs = [
        [ ROOT, "PISI" ],
        [ CLASS, SINGLE, "Source", SourceInfo, "source" ],
        [ CLASS, MULTIPLE, "Package", PackageInfo, "packages" ]
    ]
    
    def __init__(self, fileName=None):
        readXmlFile(self, fileName)


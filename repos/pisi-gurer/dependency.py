# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

from xmlutil import *

class DepInfo:
    
    xmldefs = [
        [ TEXT, SINGLE, "", "package" ],
        [ ATTRIBUTE, OPTIONAL, "", "versionFrom", "versionFrom" ],
        [ ATTRIBUTE, OPTIONAL, "", "versionTo", "versionTo" ],
        [ ATTRIBUTE, OPTIONAL, "", "releaseFrom", "releaseFrom" ],
        [ ATTRIBUTE, OPTIONAL, "", "releaseTo", "releaseTo" ],
    ]
    
    def __init__(self, node = None):
        pass
    
    def __str__(self):
        s = self.package
        if self.versionFrom:
            s += 'ver >= ' + self.versionFrom
        if self.versionTo:
            s += 'ver <= ' + self.versionTo
        if self.releaseFrom:
            s += 'rel >= ' + self.releaseFrom
        if self.releaseTo:
            s += 'rel <= ' + self.releaseTo
        return s

#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.

from qt import *
from kdecore import *
from khtml import *

import ConfigParser


programs = None
config = ConfigParser.SafeConfigParser()

def loadIcon(name, group=KIcon.Desktop, size=16):
    return KGlobal.iconLoader().loadIcon(name, group, size)

def loadIconSet(name, group=KIcon.Toolbar):
    return KGlobal.iconLoader().loadIconSet(name, group)

def getPrograms():
    if not programs:
        programs = []
        # FIXME: COMAR might be used to get the list
    return programs
    
def parseConfig():
    # FIXME: use a variable for "home" path
    config.read("/home/bertan/.proxy/config")
    

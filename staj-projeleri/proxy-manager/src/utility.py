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

from firefox import Firefox
from amsn import AMSN
from aria2 import Aria2
from kde import KDE
from gftp import Gftp

programs = None
config = ConfigParser.SafeConfigParser()
configPath = "config_files/config"
modules = []

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
    config.read(configPath)

def createModules():
    modules.append(Firefox())
    modules.append(AMSN())
    modules.append(Aria2())
    modules.append(KDE())
    modules.append(Gftp())

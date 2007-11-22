#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, 2006 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

import os
from kdecore import KGlobal, KIcon

def loadIcon(name, group=KIcon.Desktop):
    return KGlobal.iconLoader().loadIcon(name, group)

def getIconPath(icon, group=KIcon.Desktop):
    packageIconPath = KGlobal.iconLoader().iconPath("package", group)
    if not icon:
        return packageIconPath

    iconPath = KGlobal.iconLoader().iconPath(icon, group, True)
    # icon metadata may exist in the package but the pixmap may not 
    # exists on the system yet for any to be installed package.
    if not iconPath:
        return packageIconPath
    else:
        return iconPath

def loadIconSet(name, group=KIcon.Toolbar):
    return KGlobal.iconLoader().loadIconSet(name, group, 0, False)

def getIconSize():
    KGlobal.config().setGroup("DesktopIcons")
    return KGlobal.config().readNumEntry("Size", 48)

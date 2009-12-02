#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2008, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

import locale

from qt import *
from kdecore import *
from kdeui import *

def I18N_NOOP(str):
    return str

def getIcon(name, group=KIcon.Toolbar):
    return KGlobal.iconLoader().loadIcon(name, group)

def getIconSet(name, group=KIcon.Toolbar):
    return KGlobal.iconLoader().loadIconSet(name, group)

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

def getOutputName(output):
    if output == "default":
        return i18n("Default Output")
    elif output == "auto":
        return i18n("Automatic")

    outputNames = (
            (i18n("Laptop Panel (%1)"),     ["lvds"]),
            (i18n("Analog Output (%1)"),    ["crt", "vga"]),
            (i18n("Digital Output (%1)"),   ["dfp", "dvi", "hdmi", "tmds"]),
            (i18n("TV Output (%1)"),        ["s-video", "composite", "component", "tv"])
            )

    locale.setlocale(locale.LC_ALL, "en_US")
    outputlower = output.lower()
    for item in outputNames:
        for name in item[1]:
            if outputlower.startswith(name):
                return item[0].arg(output)

    return output

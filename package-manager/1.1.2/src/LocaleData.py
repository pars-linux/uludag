#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file

import locale
from kdecore import KGlobal

locales = {
    "tr" : "tr_TR.UTF8",
    "en_US" : "en_US.UTF-8",
    "nl" : "nl_NL.UTF-8",
    "de" : "de_DE.UTF-8",
    "fr" : "fr_FR.UTF-8",
    "it" : "it_IT.UTF-8",
    }

def getKDELocale():
    return str(KGlobal.locale().language())

# package-manager uses KDE locale info, pisi.api uses system locale info. We need 
# to map KDE locale info to system locale info to make dynamic KDE system language 
# changes from Tasma visible to package-manager.
def setSystemLocale():
    kdeLocale = getKDELocale()

    if locales.has_key(kdeLocale):
        systemlocale = locales[kdeLocale]
    else:
        systemlocale = "en_US.UTF-8"

    locale.setlocale(locale.LC_ALL, systemlocale)

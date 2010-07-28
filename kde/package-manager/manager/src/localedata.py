#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file

import locale
from os import getenv
from os import path
import context as ctx

locales = {
    "tr" : "tr_TR.UTF8",
    "en_US" : "en_US.UTF-8",
    "nl" : "nl_NL.UTF-8",
    "de" : "de_DE.UTF-8",
    "fr" : "fr_FR.UTF-8",
    "it" : "it_IT.UTF-8",
    "es" : "es_ES.UTF-8",
    "sv" : "sv_SE.UTF-8",
    }

def getKDELocale():
    """ Get KDE Locale from current user settings """
    return ctx.Pds.settings('Locale/Language', '').split(':')[0]

def getAppLocale():
    """ Get App Locale from Application settings """
    cf = path.join(ctx.Pds.config_path, 'share/config/package-managerrc')
    if path.exists(cf):
        cc = ctx.Pds.parse(cf, force=True)
        appLocale = cc.value('Locale/Language').toString()
        if appLocale:
            appLocale = str(appLocale).split(':')[0]
            if locales.has_key(appLocale):
                return appLocale
    return

def setSystemLocale(justGet = False):
    """
     Package-manager uses KDE locale info, pisi.api uses system locale info.
     We need to map KDE locale info to system locale info to make dynamic KDE
     system language changes from Tasma visible to package-manager
    """
    kdeLocale = getKDELocale()
    appLocale = getAppLocale()

    if locales.has_key(appLocale):
        systemlocale = locales[appLocale]
    elif locales.has_key(kdeLocale):
        systemlocale = locales[kdeLocale]
    else:
        # POSIX Standard
        for var in ('LC_ALL', 'LC_CTYPE', 'LANG', 'LANGUAGE'):
            systemlocale = getenv(var)
            if systemlocale:
                break
        else:
            systemlocale = locales['en_US']

    if justGet:
        return systemlocale.split('.')[0][:2]

    try:
        locale.setlocale(locale.LC_ALL, systemlocale)
    except:
        locale.setlocale(locale.LC_ALL, locales['en_US'])

    ctx.Pds.updatei18n(systemlocale.split('.')[0])

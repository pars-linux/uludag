#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

import locale
import string

from kdecore import *


def I18N_NOOP(str):
    return str

def getIconSet(name, group=KIcon.Toolbar):
    return KGlobal.iconLoader().loadIconSet(name, group)

def languageCode():
    lang = locale.setlocale(locale.LC_MESSAGES)
    if "_" in lang:
        return lang.split("_")[0]
    return "en"

nickmap = {
    u"ğ": u"g",
    u"ü": u"u",
    u"ş": u"s",
    u"ı": u"i",
    u"ö": u"o",
    u"ç": u"c",
}

def nickGuess(name, nicklist):
    def convert(name):
        text = ""
        for c in name:
            if c in string.ascii_letters:
                text += c
            else:
                c = nickmap.get(c, None)
                if c:
                    text += c
        return text
    
    if name == "":
        return ""
    
    text = unicode(name).lower().split()
    
    # First guess: name
    ret = convert(text[0])
    if not ret in nicklist:
        return ret
    
    # Second guess: nsurname
    if len(text) > 1:
        ret = convert(text[0][0]) + convert(text[1])
        if not ret in nicklist:
            return ret
    
    # Third guess: namesurname
    if len(text) > 1:
        ret = convert(text[0]) + convert(text[1])
        if not ret in nicklist:
            return ret
    
    # Last guess: nameN
    i = 2
    while True:
        ret = convert(text[0]) + unicode(i)
        if not ret in nicklist:
            return ret
        i += 1

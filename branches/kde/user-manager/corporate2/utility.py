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
import os
import string
import sys

from qt import *
from kdecore import *
from khtml import *

import dbus

def I18N_NOOP(str):
    return str

def getIconSet(name, group=KIcon.Toolbar):
    return KGlobal.iconLoader().loadIconSet(name, group)

def getIcon(name, group=KIcon.Small):
    return KGlobal.iconLoader().loadIcon(name, group)

class HelpDialog(QDialog):
    def __init__(self, name, title, parent=None):
        QDialog.__init__(self, parent)
        self.setCaption(title)
        self.layout = QGridLayout(self)
        self.htmlPart = KHTMLPart(self)
        self.resize(500, 600)
        self.layout.addWidget(self.htmlPart.view(), 1, 1)
        
        lang = locale.setlocale(locale.LC_MESSAGES)
        if "_" in lang:
            lang = lang.split("_", 1)[0]
        url = locate("data", "%s/help/%s/main_help.html" % (name, lang))
        if not os.path.exists(url):
            url = locate("data", "%s/help/en/main_help.html" % name)
        self.htmlPart.openURL(KURL(url))


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

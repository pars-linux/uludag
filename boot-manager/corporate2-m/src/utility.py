#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

from qt import *
from kdecore import *
from kdeui import *
from khtml import *

import locale
import os

def I18N_NOOP(str):
    return str

def getIconSet(name, group=KIcon.Toolbar):
    return KGlobal.iconLoader().loadIconSet(name, group)

class HelpDialog(QDialog):
    def __init__(self, name, title, parent=None):
        QDialog.__init__(self, parent)
        self.setCaption(title)
        self.layout = QGridLayout(self)
        self.htmlPart = KHTMLPart(self)
        self.resize(500, 600)
        self.layout.addWidget(self.htmlPart.view(), 1, 1)

        lang = locale.setlocale(locale.LC_MESSAGES)
        if '_' in lang:
            lang = lang.split('_', 1)[0]
        url = locate('data', '%s/help/%s/main_help.html' % (name, lang))
        if not os.path.exists(url):
            url = locate('data', '%s/help/en/main_help.html' % name)
        self.htmlPart.openURL(KURL(url))

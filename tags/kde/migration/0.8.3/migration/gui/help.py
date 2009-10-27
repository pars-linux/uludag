#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

import os
import locale

# KDE-Qt Modules
from qt import *
from kdecore import *
from kdeui import *
from khtml import *

class HelpDialog(QDialog):
    def __init__(self, name, title, parent=None):
        QDialog.__init__(self, parent)
        self.resize(500, 600)
        self.setCaption(title)
        self.layout = QGridLayout(self)
        self.htmlPart = KHTMLPart(self)
        self.layout.addWidget(self.htmlPart.view(), 1, 1)
        
        lang = locale.setlocale(locale.LC_MESSAGES)
        if "_" in lang:
            lang = lang.split("_", 1)[0]
            url = locate("appdata", "help/%s/main_help.html" % lang)
        if not os.path.exists(url):
            url = locate("appdata", "help/en/main_help.html")
        self.htmlPart.openURL(KURL(url))

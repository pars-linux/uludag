#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import os
import locale
from qt import *
from kdecore import *
from khtml import *


class Edit(QHBox):
    def __init__(self, parent, is_password=False):
        QHBox.__init__(self, parent)
        
        self.edit = QLineEdit(self)
        self.setStretchFactor(self.edit, 3)
        if is_password:
            self.edit.setEchoMode(QLineEdit.Password)
        
        self.layout().insertStretch(-1, 2)


class HLine(QHBox):
    def __init__(self, title, parent):
        QHBox.__init__(self, parent)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        
        line = QFrame(self)
        line.setFrameStyle(line.HLine | line.Sunken)
        line.setFixedWidth(48)
        
        text = QLabel(" %s " % unicode(title), self)
        
        line = QFrame(self)
        line.setFrameStyle(line.HLine | line.Sunken)
        self.setStretchFactor(line, 8)


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

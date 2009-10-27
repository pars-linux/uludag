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
from qt import *
from kdecore import *
from khtml import *

from icons import getIconSet

class HelpDialog(QDialog):
    def __init__(self, name, title, parent=None):
        QDialog.__init__(self, parent)
        self.setCaption(title)
        self.layout = QGridLayout(self)
        self.htmlPart = KHTMLPart(self)
        self.resize(500, 600)
        self.layout.addWidget(self.htmlPart.view(), 1, 1)

        lang = str(KGlobal().locale().language())
        if "_" in lang:
            lang = lang.split("_", 1)[0]
        url = locate("data", "%s/help/%s/main_help.html" % (name, lang))
        if not os.path.exists(url):
            url = locate("data", "%s/help/en/main_help.html" % name)
        self.htmlPart.openURL(KURL(url))
        self.show()

    def closeEvent(self, event):
        QDialog.closeEvent(self, event)


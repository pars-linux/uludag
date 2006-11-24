# -*- coding: utf-8 -*-
#
# Copyright (C) 2005,2006 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

import os
from qt import *
from kdecore import locate, i18n, KURL
from khtml import KHTMLPart

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self,parent)
        self.setCaption(i18n("Package Manager Help"))
        self.layout = QGridLayout(self)
        self.htmlPart = KHTMLPart(self)
        self.resize(500,600)
        self.layout.addWidget(self.htmlPart.view(),1,1)

        if os.environ['LANG'].startswith('tr_TR'):
            self.htmlPart.openURL(KURL(locate("data","package-manager/help/tr/main_help.html")))
        else:
            self.htmlPart.openURL(KURL(locate("data","package-manager/help/en/main_help.html")))

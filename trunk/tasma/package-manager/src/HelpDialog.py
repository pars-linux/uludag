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
from LocaleData import getKDELocale

(MAINAPP, PREFERENCES) = (1, 2)

help_files = {
    MAINAPP:"main_help.html",
    PREFERENCES:"preferences_help.html"
    }

class HelpDialog(QDialog):
    def __init__(self, parent, help):
        QDialog.__init__(self, parent)
        self.setCaption(i18n("Package Manager Help"))
        self.layout = QGridLayout(self)
        self.htmlPart = KHTMLPart(self)
        self.resize(500,600)
        self.layout.addWidget(self.htmlPart.view(),1,1)

        locale = getKDELocale()
        if locale in ["tr", "es", "en", "fr", "nl"]:
            self.htmlPart.openURL(KURL(locate("data","package-manager/help/%s/%s" % (locale, help_files[help]))))
        else:
            self.htmlPart.openURL(KURL(locate("data","package-manager/help/en/%s" % help_files[help])))

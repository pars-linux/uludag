# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

import os

from PyQt4 import QtGui
from PyQt4 import QtWebKit
from PyQt4.QtCore import QUrl

from localedata import *
from context import *

(MAINAPP, PREFERENCES) = (1, 2)

help_files = {
    MAINAPP:"main_help.html",
    PREFERENCES:"preferences_help.html"
    }

class HelpDialog(QtGui.QDialog):
    def __init__(self, parent, help):
        QtGui.QDialog.__init__(self, parent)
        self.setModal(True)
        self.setWindowTitle(i18n("Package Manager Help"))
        self.layout = QtGui.QGridLayout(self)
        self.htmlPart = QtWebKit.QWebView(self)
        self.resize(700,500)
        self.layout.addWidget(self.htmlPart,1,1)

        locale = getKDELocale()

        if locale in ["tr", "es", "en", "fr", "nl", "de", "sv"]:
            self.htmlPart.load(QUrl("/usr/share/package-manager/help/%s/%s" % (locale, help_files[help])))
        else:
            self.htmlPart.load(QUrl("/usr/share/package-manager/help/en/%s" % help_files[help]))

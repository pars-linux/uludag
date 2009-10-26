#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# Qt
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QDialog, QListWidgetItem

# PyKDE
from PyKDE4.kdeui import KIcon
from PyKDE4.kdecore import i18n

# UI
from gui.ui.languages import Ui_LanguagesDialog

LANGUAGES = {
    "ca_ES": "Catalan",
    "de_DE": "Deutsch",
    "en_US": "English",
    "es_ES": "Spanish",
    "fr_FR": "French",
    "it_IT": "Italian",
    "nl_NL": "Dutch",
    "pl_PL": "Polish",
    "pt_BR": "Brazilian Portuguese",
    "sv_SE": "Svenska",
    "tr_TR": "Turkish",
}


class LanguageWidgetItem(QListWidgetItem):
    def __init__(self, code, label):
        QListWidgetItem.__init__(self)
        self.code = code
        self.label = label
        self.setText(label)


class LanguagesDialog(QDialog, Ui_LanguagesDialog):
    def __init__(self, parent, languages=[]):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        # Selected languages
        self.languages = languages

        # Ok/cancel buttons
        self.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        self.connect(self.buttonBox, SIGNAL("rejected()"), self.reject)

        # Go go go!
        self.initialize()

    def accept(self):
        self.languages = []
        selected = self.selectorLanguages.selectedListWidget()
        for index in xrange(selected.count()):
            item = selected.item(index)
            self.languages.append(item.code)
        QDialog.accept(self)

    def initialize(self):
        selected = self.selectorLanguages.selectedListWidget()
        available = self.selectorLanguages.availableListWidget()
        for code in self.languages:
            item = LanguageWidgetItem(code, LANGUAGES[code])
            selected.addItem(item)
        for code, label in LANGUAGES.iteritems():
            if code not in self.languages:
                item = LanguageWidgetItem(code, label)
                available.addItem(item)

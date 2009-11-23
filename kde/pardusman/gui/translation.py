#!/usr/bin/python
# -*- coding: utf-8 -*-
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
from PyQt4.QtCore import SIGNAL, Qt
from PyQt4.QtGui import QDialog

from gui.languages import LANGUAGES

# UI
from gui.ui.translations import Ui_TranslationsDialog

import gettext
_ = lambda x:gettext.ldgettext("pardusman", x)

class TranslationDialog(QDialog, Ui_TranslationsDialog):
    def __init__(self, parent, description, collection):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        # Selection may be collection or tmpLanguageSelection
        self.description = description
        if collection.descriptionSelection:
            self.translations = collection.descriptionSelection.translations
        else:
            self.translations = {}

        self.languages = collection.languageSelection.languages

        #self.languages = languageSelection.languages
        #if collection.descriptionSelection.translations:
        #    self.translations = collection.descriptionSelection.translations

        # Ok/cancel buttons
        self.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        self.connect(self.buttonBox, SIGNAL("rejected()"), self.reject)

        # Filter combo
        self.connect(self.comboLanguages, SIGNAL("currentIndexChanged(int)"), self.slotComboLanguageFilter)

        self.connect(self.pushSave, SIGNAL("clicked()"), self.slotSaveTranslation)
        self.connect(self.pushClear, SIGNAL("clicked)"), self.slotClearTranslation)

        self.initialize()

    def initialize(self):
        self.labelDescription.setText(self.description)
        for code in self.languages:
            self.comboLanguages.addItem(LANGUAGES[code])

    def slotSaveTranslation(self):
        index = self.comboLanguages.currentIndex()
        self.translations[self.languages[index]] = unicode(self.textTranslation.toPlainText())

    def slotClearTranslation(self):
        self.labelDescription.setText(None)

    def slotComboLanguageFilter(self, index):
        if self.translations.has_key(self.languages[index]):
            self.textTranslation.setPlainText(self.translations[self.languages[index]])

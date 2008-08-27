# -*- coding: utf-8 -*-
#
# Copyright (C) 2008, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

from qt import *
from kdecore import *
from kdeui import *
import kdedesigner
from pardus import localedata
import subprocess

from screens.Screen import ScreenWidget
from screens.languagedlg import LanguageWidget

class Widget(LanguageWidget, ScreenWidget):

    # title and description at the top of the dialog window
    title = i18n("Language Settings")
    desc = i18n("Configure your language")

    def __init__(self, *args):
        apply(LanguageWidget.__init__, (self, ) + args)

        # set images
        self.pix_language.setPixmap(QPixmap(locate("data", "kaptan/pics/languages.png")))
        self.setPaletteBackgroundPixmap(QPixmap(locate("data", "kaptan/pics/middleWithCorner.png")))

        # set texts
        self.setCaption(i18n("Language"))
        #self.languageLabel.setText(i18n("<p align=\"left\">You can configure your language from here.</p>"))

        # set signals
        self.listLanguage.connect(self.listLanguage, SIGNAL("selectionChanged()"), self.setLanguage)

    def installPackages(self):
        pass

    def setLanguage(self):
        pass

    def shown(self):
        pass

    def execute(self):
        pass

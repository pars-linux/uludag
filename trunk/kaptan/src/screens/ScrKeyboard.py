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

from screens.Screen import ScreenWidget
from screens.keyboarddlg import KeyboardWidget

class Widget(KeyboardWidget, ScreenWidget):

    # title and description at the top of the dialog window
    title = i18n("Keyboard Settings")
    desc = i18n("Configure your keyboard")

    def __init__(self, *args):
        apply(KeyboardWidget.__init__, (self, ) + args)

        # set images
        self.pix_keyboard.setPixmap(QPixmap(locate("data", "kaptan/pics/keyboards.png")))
        self.setPaletteBackgroundPixmap(QPixmap(locate("data", "kaptan/pics/middleWithCorner.png")))

        # set texts
        self.setCaption(i18n("Keyboard"))
        self.keyboardLabel.setText(i18n("<p align=\"left\">You can configure your keyboard from here.</p>"))

        # set signals
        self.listKeyboard.connect(self.listKeyboard, SIGNAL("selectionChanged()"), self.setKeyboard)

    def setKeyboard(self):
        pass

    def shown(self):
        pass

    def execute(self):
        pass


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

        # get Layout config
        self.config = KConfig("kxkbrc")
        self.config.setGroup("Layout")
        self.layoutList = str(self.config.readEntry("LayoutList"))
        self.lastLayout = 0

        # get keyboard layouts
        for lang in localedata.languages:
            for each in localedata.languages[lang].keymaps:
                item = KListViewItem(self.listKeyboard, "keyboard", each.xkb_layout, each.xkb_variant)
                item.setText(0, each.name)

        # set signals
        self.listKeyboard.connect(self.listKeyboard, SIGNAL("selectionChanged()"), self.setKeyboard)

    def setKeyboard(self):
        layout = self.listKeyboard.currentItem().key(1, True)
        variant = self.listKeyboard.currentItem().key(2, True)
        subprocess.Popen(["setxkbmap", layout, variant])

        if variant:
            self.lastLayout = layout + "(" + variant + ")"
        else:
            self.lastLayout = layout

    def shown(self):
        pass

    def execute(self):
        if self.lastLayout:
            layoutArr = self.layoutList.split(",")

            if self.lastLayout not in layoutArr:
                layoutArr.insert(0, str(self.lastLayout))
            else:
                layoutArr.remove(self.lastLayout)
                layoutArr.insert(0, str(self.lastLayout))

            layoutList =  ",".join(layoutArr)
            self.config.writeEntry("LayoutList", layoutList)
            self.config.sync()

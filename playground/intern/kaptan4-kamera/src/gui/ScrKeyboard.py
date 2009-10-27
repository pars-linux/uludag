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


from PyQt4 import QtGui

from PyQt4.QtCore import *
from PyKDE4.kdecore import ki18n, KConfig

import gui.ScrSummary  as summaryWidget
import gui.ScrSummary  as summaryWidget
from gui.ScreenWidget import ScreenWidget
from gui.keyboardWidget import Ui_keyboardWidget
import subprocess

from pardus import localedata

class Widget(QtGui.QWidget, ScreenWidget):
    screenSettings = {}
    screenSettings["hasChanged"] = False

    # title and description at the top of the dialog window
    title = ki18n("Insert some catchy title about keyboards..")
    desc = ki18n("Select your keyboard layout")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_keyboardWidget()
        self.ui.setupUi(self)
        self.ui.picKeyboard.setPixmap(QtGui.QPixmap(':/raw/pics/keyboards.png'))

        # get Layout config
        self.config = KConfig("kxkbrc")
        self.group = self.config.group("Layout")
        self.layoutList = str(self.group.readEntry("LayoutList"))
        self.lastLayout = 0

        for lang in localedata.languages:
            for each in localedata.languages[lang].keymaps:
                item = QtGui.QListWidgetItem(self.ui.listWidgetKeyboard)
                item.setText(each.name)
                item.setToolTip(each.xkb_layout)
                item.setStatusTip(each.xkb_variant)
                self.ui.listWidgetKeyboard.addItem(item)

        self.ui.listWidgetKeyboard.connect(self.ui.listWidgetKeyboard, SIGNAL("itemSelectionChanged()"), self.setKeyboard)

    def setKeyboard(self):
        layout = self.ui.listWidgetKeyboard.currentItem().toolTip()
        variant = self.ui.listWidgetKeyboard.currentItem().statusTip()

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

            for i in layoutArr:
                if i == "":
                    layoutArr.remove(i)

            layoutList =  ",".join(layoutArr)
            self.group.writeEntry("LayoutList", layoutList)
            self.group.writeEntry("DisplayNames", layoutList)
            self.config.sync()
        return True



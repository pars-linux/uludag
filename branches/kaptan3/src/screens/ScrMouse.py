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
from Xlib import display

from screens.Screen import ScreenWidget
from screens.mousedlg import MouseWidget

RIGHT_HANDED, LEFT_HANDED = range(2)

# set summary picture and description
summary = {"sum" : "",
           "pic" : "kaptan/pics/mouseSummary.png",
           "desc": i18n("Mouse")}

class Widget(MouseWidget, ScreenWidget):

    # title and description at the top of the dialog window
    title = i18n("Mouse Settings")
    desc = i18n("Configure your mouse")

    def __init__(self, *args):
        apply(MouseWidget.__init__, (self, ) + args)

        # set images
        self.pix_mouse.setPixmap(QPixmap(locate("data", "kaptan/pics/mouse_rh.png")))
        self.setPaletteBackgroundPixmap(QPixmap(locate("data", "kaptan/pics/middleWithCorner.png")))

        # set texts
        self.setCaption(i18n("Mouse"))
        self.checkReverse.setText(i18n("Reverse scroll"))
        self.mouseLabel.setText(i18n("<p align=\"left\">If you are left-handed, you may prefer to swap the functions on the left and right buttons on your pointing device bu choosing the \"Left handed\" option below. You can also select default click behaviour.</p>"))
        self.buttonOrderGroup.setTitle(i18n("Button Order"))
        self.leftHanded.setText(i18n("Left Hand"))
        self.rightHanded.setText(i18n("Right Hand"))
        self.clickSettingsGroup.setTitle(i18n("Click behaviour"))
        self.singleClick.setText(i18n("&Single-click to open files and folders"))
        self.doubleClick.setText(i18n("Dou&ble-click to open files and folders (select icons on first click)"))

        # set signals
        self.connect(self.singleClick, SIGNAL("toggled(bool)"),self.setClickBehaviour)
        self.connect(self.rightHanded, SIGNAL("toggled(bool)"), self.setHandedness)
        self.connect(self.checkReverse, SIGNAL("toggled(bool)"), self.setHandedness)

    def shown(self):
        pass

    def execute(self):
        if self.singleClick.isChecked():
            summary["sum"]= i18n("Single Click")
        else:
            summary["sum"]= i18n("Double Click")

        if self.rightHanded.isChecked():
            summary["sum"] += i18n(", Right Handed")
        else:
            summary["sum"] += i18n(", Left Handed")

        if self.checkReverse.isChecked():
            summary["sum"] += i18n(", Reverse Scrolling")

    def setClickBehaviour(self):
        config = KConfig("kdeglobals")
        config.setGroup("KDE")
        config.writeEntry("SingleClick", self.singleClick.isChecked())
        config.sync()

        KIPC.sendMessageAll(KIPC.SettingsChanged, KApplication.SETTINGS_MOUSE)

    def setHandedness(self, item):
        map = {}

        if self.rightHanded.isChecked():
            handed = RIGHT_HANDED
            self.pix_mouse.setPixmap(QPixmap(locate("data", "kaptan/pics/mouse_rh.png")))
        else:
            handed = LEFT_HANDED
            self.pix_mouse.setPixmap(QPixmap(locate("data", "kaptan/pics/mouse_lh.png")))

        map = display.Display().get_pointer_mapping()
        num_buttons = len(map)

        if num_buttons == 1:
            map[0] = 1
        elif num_buttons == 2:
            if handed == RIGHT_HANDED:
                map[0], map[1] = 1, 3
            else:
                map[0], map[1] = 3, 1
        else:
            if handed == RIGHT_HANDED:
                map[0], map[2] = 1, 3
            else:
                map[0], map[2] = 3, 1

            if num_buttons >= 5:
                pos = 0
                for pos in range(num_buttons):
                    if map[pos] == 4 or map[pos] == 5:
                        break

                if pos < num_buttons -1:
                    if self.checkReverse.isChecked():
                        map[pos], map[pos + 1] = 5, 4
                    else:
                        map[pos], map[pos + 1] = 4, 5

        display.Display().set_pointer_mapping(map)

        config = KConfig("kcminputrc")
        config.setGroup("Mouse")

        if handed == RIGHT_HANDED:
            config.writeEntry("MouseButtonMapping", QString("RightHanded"))
        else:
            config.writeEntry("MouseButtonMapping", QString("LeftHanded"))

        config.writeEntry("ReverseScrollPolarity", self.checkReverse.isChecked())
        config.sync()

        KIPC.sendMessageAll(KIPC.SettingsChanged, KApplication.SETTINGS_MOUSE)




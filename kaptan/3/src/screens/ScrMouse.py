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

class Widget(MouseWidget, ScreenWidget):

    # title and description at the top of the dialog window
    title = i18n("Mouse Settings")
    desc = i18n("Configure your mouse")
    icon = "kaptan/pics/icons/mouse.png"

    def __init__(self, *args):
        apply(MouseWidget.__init__, (self, ) + args)

        # set images
        self.pix_mouse.setPixmap(QPixmap(locate("data", "kaptan/pics/mouse_rh.png")))
        self.setPaletteBackgroundPixmap(QPixmap(locate("data", "kaptan/pics/middleWithCorner.png")))

        # set texts
        self.setCaption(i18n("Mouse"))
        self.checkReverse.setText(i18n("Reverse scrolling direction"))
        self.mouseLabel.setText(i18n("<p align='left'>The <b>clicking behavior</b> defines how many times you want to click when you are opening a file.<br/><br/>If you are <b>left handed</b>, you may prefer to swap the left and right buttons of your pointing device.</p>"))
        self.buttonOrderGroup.setTitle(i18n("Button Order"))
        self.leftHanded.setText(i18n("Left Hand"))
        self.rightHanded.setText(i18n("Right Hand"))
        self.clickSettingsGroup.setTitle(i18n("Clicking Behaviour"))
        self.singleClick.setText(i18n("&Single-click to open files and folders"))
        self.doubleClick.setText(i18n("Dou&ble-click to open files and folders"))

        # set signals
        self.connect(self.singleClick, SIGNAL("toggled(bool)"),self.setClickBehaviour)
        self.connect(self.rightHanded, SIGNAL("toggled(bool)"), self.setHandedness)
        self.connect(self.checkReverse, SIGNAL("toggled(bool)"), self.setHandedness)

    def shown(self):
        pass

    def execute(self):
        pass

    def setClickBehaviour(self):
        config = KConfig("kdeglobals")
        config.setGroup("KDE")
        config.writeEntry("SingleClick", self.singleClick.isChecked())
        config.sync()

        KIPC.sendMessageAll(KIPC.SettingsChanged, KApplication.SETTINGS_MOUSE)

    def setHandedness(self, item):
        mapMouse = {}

        if self.rightHanded.isChecked():
            handed = RIGHT_HANDED
            self.pix_mouse.setPixmap(QPixmap(locate("data", "kaptan/pics/mouse_rh.png")))

        else:
            handed = LEFT_HANDED
            self.pix_mouse.setPixmap(QPixmap(locate("data", "kaptan/pics/mouse_lh.png")))


        mapMouse = display.Display().get_pointer_mapping()
        num_buttons = len(mapMouse)

        if num_buttons == 1:
            mapMouse[0] = 1
        elif num_buttons == 2:
            if handed == RIGHT_HANDED:
                mapMouse[0], mapMouse[1] = 1, 3
            else:
                mapMouse[0], mapMouse[1] = 3, 1
        else:
            if handed == RIGHT_HANDED:
                mapMouse[0], mapMouse[2] = 1, 3
            else:
                mapMouse[0], mapMouse[2] = 3, 1

            if num_buttons >= 5:
                pos = 0
                for pos in range(num_buttons):
                    if mapMouse[pos] == 4 or mapMouse[pos] == 5:
                        break

                if pos < num_buttons -1:
                    if self.checkReverse.isChecked():
                        mapMouse[pos], mapMouse[pos + 1] = 5, 4
                    else:
                        mapMouse[pos], mapMouse[pos + 1] = 4, 5

        display.Display().set_pointer_mapping(mapMouse)

        config = KConfig("kcminputrc")
        config.setGroup("Mouse")

        if handed == RIGHT_HANDED:
            config.writeEntry("MouseButtonMapping", QString("RightHanded"))
        else:
            config.writeEntry("MouseButtonMapping", QString("LeftHanded"))

        config.writeEntry("ReverseScrollPolarity", self.checkReverse.isChecked())
        config.sync()

        KIPC.sendMessageAll(KIPC.SettingsChanged, KApplication.SETTINGS_MOUSE)




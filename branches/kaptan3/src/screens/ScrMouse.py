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
    title = "Mouse Settings"
    desc = "Configure your mouse"

    def __init__(self, *args):
        apply(MouseWidget.__init__, (self,) + args)
        self.pix_mouse.setPixmap(QPixmap(locate("data", "kaptan/pics/mouse_rh.png")))
        self.connect(self.singleClick, SIGNAL("toggled(bool)"),self.setClickBehaviour)
        self.connect(self.rightHanded, SIGNAL("toggled(bool)"), self.setHandedness)

    def shown(self):
        pass

    def execute(self):
        return True

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
        map= display.Display().get_pointer_mapping()
        num_buttons = len(map)

        if num_buttons == 1:
            map[0] = 1
        elif num_buttons == 2:
            if handed == RIGHT_HANDED:
                map[0], map[1] = 1,3
            else:
                map[0],map[1]= 3,1
        else:
            if handed == RIGHT_HANDED:
                map[0],map[2] = 1,3
            else:
                map[0],map[2] = 3,1
        if num_buttons >=5:
            pos = 0
            for pos in range(num_buttons):
                if map[pos] == 4 or map[pos] == 5:
                    break

            #check reverse
        
        display.Display().set_pointer_mapping(map)

        config = KConfig("kcminputrc")
        config.setGroup("Mouse")
        config.writeEntry("MouseButtonMapping", QString("RightHanded"))
        config.sync()
        KIPC.sendMessageAll(KIPC.SettingsChanged, KApplication.SETTINGS_MOUSE)




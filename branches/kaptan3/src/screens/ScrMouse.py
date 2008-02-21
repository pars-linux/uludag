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
from screens.mousedlg import MouseWidget

class Widget(MouseWidget, ScreenWidget):

    # title and description at the top of the dialog window
    title = "Mouse Settings"
    desc = "Configure your mouse"

    def __init__(self, *args):
        apply(MouseWidget.__init__, (self,) + args)
        self.connect(self.singleClick, SIGNAL("toggled(bool)"),self.setClickBehaviour)

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

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
import kdecore

from screens.Screen import ScreenWidget
from screens.multipledlg import MultipleWidget

summary = {"sum":""}
summary["pic"] = "kaptan/pics/mouse_rh.png"
summary["desc"] = "Multiple Desktops"


class Widget(MultipleWidget, ScreenWidget):

    # title and description at the top of the dialog window
    title = "Multiple Desktops"
    desc = "Configure virtual desktops.."
    #for simplicity, multiple desktops are limited to 4.
    maxDesktops = 8

    def __init__(self, *args):
        apply(MultipleWidget.__init__, (self,) + args)
        self.numInput.setRange(1, self.maxDesktops , 1, True)
        self.connect(self.numInput, SIGNAL("valueChanged(int)"), self.changed)
        self.connect(self.mouseWheel, SIGNAL("toggled(bool)"),self.clicked)

    def clicked(self):
        config = KConfig("kdesktoprc")
        config.setGroup("Mouse Buttons")
        config.writeEntry("WheelSwitchesWorkspace",self.mouseWheel.isChecked())

    def changed(self):
        numberOfDesktops =  self.numInput.value()
        info = kdecore.NETRootInfo(int(qt_xdisplay()))
        info.setNumberOfDesktops(numberOfDesktops)
        info.activate()

    def shown(self):
        pass

    def execute(self):
        summary["sum"] = str(self.numInput.value())
        if self.mouseWheel.isChecked():
            summary["sum"] += ", Wheel Switches Workspace"



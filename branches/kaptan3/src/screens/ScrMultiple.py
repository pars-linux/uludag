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

# set summary picture and description
summary = {"sum" : "",
           "pic" : "kaptan/pics/icons/multiple.png",
           "desc": i18n("Multiple Desktops")}

class Widget(MultipleWidget, ScreenWidget):

    # title and description at the top of the dialog window
    title = i18n("Multiple Desktops")
    desc = i18n("Configure virtual desktops..")
    icon = summary["pic"]

    # for simplicity, multiple desktops are limited to 8
    maxDesktops = 8

    def __init__(self, *args):
        apply(MultipleWidget.__init__, (self,) + args)

        self.info = kdecore.NETRootInfo(int(qt_xdisplay()))
        self.oldNumberOfDesktops =  self.info.numberOfDesktops()
        print self.oldNumberOfDesktops
        # set start value of desktops
        self.numInput.setValue(self.oldNumberOfDesktops)

        # set images
        self.setPaletteBackgroundPixmap(QPixmap(locate("data", "kaptan/pics/middleWithCorner.png")))

        if KGlobal.locale().language() == "tr":
            self.pixMultiple.setPixmap(QPixmap(locate("data", "kaptan/pics/multiple_tr.png")))
        else:
            self.pixMultiple.setPixmap(QPixmap(locate("data", "kaptan/pics/multiple_en.png")))

        self.numInput.setRange(1, self.maxDesktops , 1, True)

        # set texts
        self.setCaption(i18n("Multiple"))
        self.multipleText.setText(i18n("<p>In this module, you can configure how many virtual desktops you want and how these should be labeled.</p>"))
        self.mouseWheel.setText(i18n("Mouse wheel over desktop background switches desktop."))
        self.numInput.setSuffix(i18n(" Desktop(s)"))

        # set signals
        self.connect(self.numInput, SIGNAL("valueChanged(int)"), self.changed)
        self.connect(self.mouseWheel, SIGNAL("toggled(bool)"),self.clicked)

    def clicked(self):
        config = KConfig("kdesktoprc")
        config.setGroup("Mouse Buttons")
        config.writeEntry("WheelSwitchesWorkspace",self.mouseWheel.isChecked())

    def changed(self):
        numberOfDesktops =  self.numInput.value()
        self.info.setNumberOfDesktops(numberOfDesktops)
        self.info.activate()

    def shown(self):
        pass

    def execute(self):
        summary["sum"] = str(self.numInput.value()) + i18n(" desktop(s)")
        if self.mouseWheel.isChecked():
            summary["sum"] += i18n(", Wheel Switches Workspace")



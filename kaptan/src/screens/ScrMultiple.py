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
from pardus.procutils import capture

from screens.Screen import ScreenWidget
from screens.multipledlg import MultipleWidget

class Widget(MultipleWidget, ScreenWidget):

    # title and description at the top of the dialog window
    title = i18n("Multiple Desktops")
    desc = i18n("Configure virtual desktops..")
    icon = "kaptan/pics/icons/multiple.png"

    # for simplicity, multiple desktops are limited to 8
    maxDesktops = 8

    def __init__(self, *args):
        apply(MultipleWidget.__init__, (self,) + args)

        self.info = kdecore.NETRootInfo(int(qt_xdisplay()))

        try:
            # as detecting number of desktops via kdecore is not stable, 
            # first try to get it via xprobe.
            out, err = capture("xprop", "-root", "-f", "_NET_NUMBER_OF_DESKTOPS", "0c", " $0", "_NET_NUMBER_OF_DESKTOPS")
            self.oldNumberOfDesktops = int(out.split()[-1])
        except:
            self.oldNumberOfDesktops =  self.info.numberOfDesktops()

        # set start value of desktops
        self.numInput.setValue(self.oldNumberOfDesktops)

        # set images
        self.setPaletteBackgroundPixmap(QPixmap(locate("data", "kaptan/pics/middleWithCorner.png")))

        if KGlobal.locale().language() == "tr":
            self.pixMultiple.setPixmap(QPixmap(locate("data", "kaptan/pics/multiple_tr.png")))
        else:
            self.pixMultiple.setPixmap(QPixmap(locate("data", "kaptan/pics/multiple_en.png")))

        self.numInput.setRange(2, self.maxDesktops , 1, True)

        # set texts
        self.setCaption(i18n("Multiple"))
        self.multipleText.setText(i18n("<p>In this module, you can configure how many virtual desktops you want.</p>"))
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
        pass


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
from screens.welcomedlg import WelcomeWidget

class Widget(WelcomeWidget, ScreenWidget):

    title = i18n("Welcome")
    desc = i18n("Welcome to Kaptan Wizard :)")
    icon = "kaptan/pics/summary/welcome.png"


    def __init__(self, *args):
        apply(WelcomeWidget.__init__, (self,) + args)

        #set texts
        self.setCaption(i18n("Welcome"))
        self.textLabel1.setText(i18n("This application, called <b>Kaptan Desktop</b>, will help you with your basic but sufficient setup for your <b>Pardus</b> desktop in a quick manner. This application will also set some default configuration for a better desktop :)."))
        self.textLabel2.setText(i18n("<b>Pardus</b> is a GNU/Linux distribution, targeting at computer literate users' basic desktop needs; with acquiring the strong ideas, architecture and code of other distributions; with a custom configuration framework which has the ability to evolve into an autonomous system; for simplifying the installation and usage of the computers."))

        #set images
        self.setPaletteBackgroundPixmap(QPixmap(locate("data", "kaptan/pics/middleWithCorner.png")))
        self.pixWelcome.setPixmap(QPixmap(locate("data", "kaptan/pics/kaptan_welcome.png")))

    def shown(self):
        pass

    def execute(self):
        return True


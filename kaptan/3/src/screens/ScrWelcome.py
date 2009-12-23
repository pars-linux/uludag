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
    desc = i18n("Welcome to Kaptan")
    icon = "kaptan/pics/icons/welcome.png"


    def __init__(self, *args):
        apply(WelcomeWidget.__init__, (self,) + args)

        #set texts
        self.setCaption(i18n("Welcome"))
        self.textLabel1.setText(i18n("<b>Kaptan</b> will help you personalize your Pardus workspace easily and quickly.<br/><br/>Please click <b>next</b> in order to begin."))
        self.textLabel2.setText(i18n("<b>Pardus</b> is a reliable, secure, fast and user friendly operating system.<br/><br/>With Pardus, you can connect to the internet, read your e-mails, work with your office documents, watch movies, play music, develop applications, play games and much more!"))

        #set images
        self.setPaletteBackgroundPixmap(QPixmap(locate("data", "kaptan/pics/middleWithCorner.png")))
        self.pixWelcome.setPixmap(QPixmap(locate("data", "kaptan/pics/kaptan.png")))

    def shown(self):
        pass

    def execute(self):
        return True


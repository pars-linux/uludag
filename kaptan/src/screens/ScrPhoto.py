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
import os
import Image

from screens.Screen import ScreenWidget
from screens.photodlg import PhotoWidget

class Widget(PhotoWidget, ScreenWidget):

    # title and description at the top of the dialog window
    title = "Photo"
    desc = "Take your profile photo!..."
    icon = "kaptan/pics/icons/camera.png"

    def __init__(self, *args):
        apply(PhotoWidget.__init__, (self,) + args)

        #set background image
        self.setPaletteBackgroundPixmap(QPixmap(locate("data", "kaptan/pics/middleWithCorner.png")))
        
    def captureShot(self):
        """capture picture"""
        pass

    def shown(self):
        pass

    def execute(self):
        if self.kdmCheckBox.isChecked():
            self.homeDir = os.path.expanduser("~")
            infile = "kaptan/pics/icons/camera.png"
            self.picture = Image.open(infile)
            self.picture.save(self.homeDir+"/.face.icon" , "PNG")

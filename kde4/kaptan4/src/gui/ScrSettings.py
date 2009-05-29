# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#


from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyKDE4.kdecore import ki18n
import subprocess,os
from gui.ScreenWidget import ScreenWidget
from gui.settingsWidget import Ui_settingsWidget

# import other widgets to get the latest configuration
import gui.ScrWallpaper as wallpaperWidget
import gui.ScrMouse as mouseWidget
import gui.ScrWallpaper  as wallpaperWidget
import gui.ScrStyle  as styleWidget
import gui.ScrMenu  as menuWidget
import gui.ScrSearch  as searchWidget

class Widget(QtGui.QWidget, ScreenWidget):
    title = ki18n("Welcome")
    desc = ki18n("Welcome to Kaptan Wizard :)")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_settingsWidget()
        self.ui.setupUi(self)


        self.ui.pixKaptanLogo.setPixmap(QtGui.QPixmap(':/raw/pics/kaptan_settings.png'))

    def shown(self):
        selectedWallpaper = wallpaperWidget.Widget.selectedWallpaper
        selectedMouse = mouseWidget.Widget.selectedMouse
        selectedBehaviour = mouseWidget.Widget.selectedBehaviour
        selectedMenuName = menuWidget.Widget.selectedMenuName
        isNepomukOn = searchWidget.Widget.isNepomukOn
        selectedStyle = styleWidget.Widget.selectedStyle
        print selectedStyle
    def killPlasma(self):
        p = subprocess.Popen(["pidof", "-s", "plasma"], stdout=subprocess.PIPE)
        out, err = p.communicate()
        pidOfPlasma = int(out)

        try:
            os.kill(pidOfPlasma, 15)
            self.startPlasma()
        except OSError, e:
            print 'WARNING: failed os.kill: %s' % e
            print "Trying SIGKILL"
            os.kill(pidOfPlasma, 9)
            self.startPlasma()

    def startPlasma(self):
        p = subprocess.Popen(["plasma"], stdout=subprocess.PIPE)

    def execute(self):
        self.killPlasma()
        return True




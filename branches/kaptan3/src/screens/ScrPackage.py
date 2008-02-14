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
#import kconfig

from screens.Screen import ScreenWidget
from screens.packagedlg import PackageWidget

class Widget(PackageWidget, ScreenWidget):
    
    # title and description at the top of the dialog window
    title = "Package Manager"
    desc = "Configure package manager settings..."

    def __init__(self, *args):
        apply(PackageWidget.__init__, (self,) + args)
        self.applySettings()

    def applySettings(self):

        config = KConfig("package-managerrc")
        config.setGroup("General")
        config.writeEntry("SystemTray", True)
        config.writeEntry("UpdateCheck", True)
        config.writeEntry("UpdateCheckInterval", 2 * 60)
        config.sync();

        proc = KProcess()
        proc << locate("exe", "package-manager")
        proc.start(KProcess.DontCare)


    def shown(self):
        pass

    def execute(self):
        return True


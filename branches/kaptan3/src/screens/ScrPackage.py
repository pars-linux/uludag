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
from screens.packagedlg import PackageWidget

class Widget(PackageWidget, ScreenWidget):

    #TODO: Contrib depo ekleme hedesi yapilacak. Ama policykit, dbus ne alemde aboo

    # title and description at the top of the dialog window
    title = "Package Manager"
    desc = "Configure package manager settings..."

    def __init__(self, *args):
        apply(PackageWidget.__init__, (self,) + args)
        self.showTray.connect(self.showTray, SIGNAL("toggled(bool)"), self.enableCheckTime)
        self.checkUpdate.connect(self.checkUpdate, SIGNAL("toggled(bool)"), self.updateSelected);

    def enableCheckTime(self):
        if self.showTray.isOn():
            self.checkUpdate.setEnabled(True)
            self.updateInterval.setEnabled(self.checkUpdate.isChecked() and self.showTray.isChecked())
        else:
            self.checkUpdate.setEnabled(False)
            self.updateInterval.setEnabled(False)

    def updateSelected(self):
        if self.checkUpdate.isOn():
            self.updateInterval.setEnabled(True)
        else:
            self.updateInterval.setEnabled(False)

    def applySettings(self):

        config = KConfig("package-managerrc")
        config.setGroup("General")
        config.writeEntry("SystemTray", self.showTray.isChecked())
        config.writeEntry("UpdateCheck", self.checkUpdate.isChecked())
        config.writeEntry("UpdateCheckInterval", self.updateInterval.value() * 60)
        config.sync();

        if self.showTray.isChecked():
            proc = KProcess()
            proc << locate("exe", "package-manager")
            proc.start(KProcess.DontCare)
    
    #TODO: su applySettings hadisesi kaptan kapatildiktan sonra acilsin.
    def shown(self):
        self.applySettings()

    def execute(self):
        return True


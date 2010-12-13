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

import pisi
import logging

from screens.Screen import ScreenWidget
from screens.packagedlg import PackageWidget

isUpdateOn = False

class Widget(PackageWidget, ScreenWidget):

    # title and description at the top of the dialog window
    title = i18n("Package Manager")
    desc = i18n("Configure package manager settings...")
    icon = "kaptan/pics/icons/package.png"

    # min update time
    updateTime = 12

    def __init__(self, *args):
        apply(PackageWidget.__init__, (self,) + args)

        self.flagRepo = 0
        # set updateTime
        self.updateInterval.setValue(self.updateTime)

        # set texts
        self.setCaption(i18n("Package"))
        self.textPackage.setText(i18n("<b>Package-manager</b> is the graphical front-end of <b>PiSi</b>. You can easily install new programs and upgrade your system and also can see new upgrades of the programs periodically  from the system tray with package manager."))
        QToolTip.add(self.pixPackage,i18n("tooltipPisiPopup","Pisi Pop-Up Baloon"))
        self.groupBoxUpdates.setTitle(i18n("Updates"))
        self.showTray.setText(i18n("Show in system tray"))
        self.checkUpdate.setText(i18n("Check updates automatically for every"))
        self.updateInterval.setSuffix(i18n(" hours"))

        # set images
        self.setPaletteBackgroundPixmap(QPixmap(locate("data", "kaptan/pics/middleWithCorner.png")))
        self.pixPackage.setPixmap(QPixmap(locate("data", "kaptan/pics/package.png")))

        self.showTray.connect(self.showTray, SIGNAL("toggled(bool)"), self.enableCheckTime)
        self.checkUpdate.connect(self.checkUpdate, SIGNAL("toggled(bool)"), self.updateSelected)

        self.repodb = pisi.db.repodb.RepoDB()

        n = 1

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
        import ConfigParser
        import os

        config = ConfigParser.ConfigParser()

        # for case insensitive parser
        config.optionxform = str

        if not os.path.exists(os.path.expanduser('~/.config/Pardus')):
            os.mkdir(os.path.expanduser('~/.config/Pardus'))

        if not os.path.exists('~/.config/Pardus/Package-Manager.conf'):
            config.add_section("General")

        config_file = os.path.expanduser('~/.config/Pardus/Package-Manager.conf')
        config.read(config_file)

        config.set("General", "SystemTray", str(self.showTray.isChecked()).lower())
        config.set("General", "UpdateCheck", str(self.checkUpdate.isChecked()).lower())
        config.set("General", "UpdateCheckInterval", self.updateInterval.value() * 60)

        with open(config_file, 'w') as configfile:
            config.write(configfile)

        if self.showTray.isChecked():
            proc = KProcess()
            proc << locate("exe", "package-manager")
            proc.start(KProcess.DontCare)

    def shown(self):
        #self.applySettings()
        pass

    def execute(self):
        #return True
        self.applySettings()


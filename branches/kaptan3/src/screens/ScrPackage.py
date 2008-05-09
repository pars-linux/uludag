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

import contribrepo
import pisi

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

        # set updateTime
        self.updateInterval.setValue(self.updateTime)

        # set repo name and address
        self.repoName = "contrib"
        self.repoAddress = "http://paketler.pardus.org.tr/contrib-2007/pisi-index.xml.bz2"

        # set texts
        self.setCaption(i18n("Package"))
        self.textPackage.setText(i18n("<b>Package-manager</b> is the graphical front-end of <b>PiSi</b>. You can easily install new programs and upgrade your system and also can see new upgrades of the programs periodically  from the system tray with package manager."))
        QToolTip.add(self.pixPackage,i18n("tooltipPisiPopup","Pisi Pop-Up Baloon"))
        self.groupBoxUpdates.setTitle(i18n("Updates"))
        self.showTray.setText(i18n("Show in system tray"))
        self.checkUpdate.setText(i18n("Check updates automatically for every"))
        self.updateInterval.setSuffix(i18n(" hours"))
        self.groupBoxRepo.setTitle(i18n("Repo"))
        self.textLabelContrib.setText(i18n("Contrib repo includes extra packages."))
        self.checkBoxContrib.setText(i18n("Add contrib repo"))

        self.checkBoxContrib.setEnabled(True)

        # set images
        self.setPaletteBackgroundPixmap(QPixmap(locate("data", "kaptan/pics/middleWithCorner.png")))
        self.pixPackage.setPixmap(QPixmap(locate("data", "kaptan/pics/package.png")))

        self.showTray.connect(self.showTray, SIGNAL("toggled(bool)"), self.enableCheckTime)
        self.checkUpdate.connect(self.checkUpdate, SIGNAL("toggled(bool)"), self.updateSelected)
        self.checkBoxContrib.connect(self.checkBoxContrib, SIGNAL("toggled(bool)"), self.slotContribRepo)

        self.repodb = pisi.db.repodb.RepoDB()

        n = 1

        for repo in self.repodb.list_repos():
            if self.repoAddress == self.repodb.get_repo_url(repo):
                self.groupBoxRepo.hide()
            else:
                for r in self.repodb.list_repos():
                    if r == self.repoName + str(n):
                        n = n + 1
                    else:
                        self.repoName = r + str(n)

    def slotContribRepo(self):
        if self.checkBoxContrib.isChecked():
            print self.addRepo()
        else:
            print self.removeRepo()

    def addRepo(self):
        try:
            contribrepo.addRepo(self.repoName, self.repoAddress)
            return True
        except Exception, e:
            print e
            if e.get_dbus_name().endswith('policy.no'):
                print 'Access denied'
                return False
            elif e.get_dbus_name().endswith('policy.auth_admin'):
                print 'Access denied, root password required'
                authResult = contribrepo.auth("addrepository")

            elif e.get_dbus_name().endswith('policy.auth_user'):
                print 'Access denied, user password required'
                authResult = contribrepo.auth("addrepository")
            else:
                return False
            try:
                if authResult:
                    contribrepo.addRepo(self.repoName, self.repoAddress)
                else:
                    return False
            except:
                return False

    def removeRepo(self):
        try:
            contribrepo.removeRepo(self.repoName)
            return True
        except Exception, e:
            print e
            if e.get_dbus_name().endswith('policy.no'):
                print 'Access denied'
                return False
            elif e.get_dbus_name().endswith('policy.auth_admin'):
                print 'Access denied, root password required'
                authResult = contribrepo.auth("removerepository")

            elif e.get_dbus_name().endswith('policy.auth_user'):
                print 'Access denied, user password required'
                authResult = contribrepo.auth("removerepository")
            else:
                return False
            try:
                if authResult:
                    contribrepo.removeRepo(self.repoName)
                else:
                    return False
            except:
                return False

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
        config.sync()

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


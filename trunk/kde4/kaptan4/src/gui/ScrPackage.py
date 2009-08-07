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
from PyKDE4.kdecore import ki18n, KConfig, KProcess

from PyKDE4 import kdeui

from gui.ScreenWidget import ScreenWidget
from gui.packageWidget import Ui_packageWidget

import subprocess
import pisi
import comar

isUpdateOn = False

class Widget(QtGui.QWidget, ScreenWidget):
    title = ki18n("Package Manager")
    desc = ki18n("Configure package manager settings")

    # min update time
    updateTime = 12

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_packageWidget()
        self.ui.setupUi(self)

        self.flagRepo = 0
        # set updateTime
        self.ui.updateInterval.setValue(self.updateTime)

        # set repo name and address
        self.repoName = "contrib"
        self.repoAddress = "http://packages.pardus.org.tr/contrib-2009/pisi-index.xml.bz2"
        self.repoAddress2 = "http://paketler.pardus.org.tr/contrib-2009/pisi-index.xml.bz2"
        self.ui.picturePackage.setPixmap(QtGui.QPixmap(':/raw/pics/package.png'))

        # set signals
        self.ui.showTray.connect(self.ui.showTray, SIGNAL("toggled(bool)"), self.enableCheckTime)
        self.ui.checkUpdate.connect(self.ui.checkUpdate, SIGNAL("toggled(bool)"), self.updateSelected)
        self.ui.checkBoxContrib.connect(self.ui.checkBoxContrib, SIGNAL("toggled(bool)"), self.slotContribRepo)

        # create a db object
        self.repodb = pisi.db.repodb.RepoDB()
        n = 1 # temporary index variable for repo names

        # control if we already have contrib repo
        # if so, hide configuration box
        if self.repodb.has_repo_url(self.repoAddress) or self.repodb.has_repo_url(self.repoAddress2):
            self.ui.groupBoxRepo.hide()
        else:
            # control if we already have the same repo name
            if self.repodb.has_repo(self.repoName):
                tmpRepoName = self.repoName
                # if so, try to give a name like "contribn"
                for r in self.repodb.list_repos():
                    if self.repodb.has_repo(tmpRepoName):
                        tmpRepoName = self.repoName + str(n)
                        n = n +1
                    else:
                        break
                self.repoName = tmpRepoName

    def slotContribRepo(self):
        if self.ui.checkBoxContrib.isChecked():
            if self.addRepo(self.repoName, self.repoAddress) == False:
                self.flagRepo = 1
                self.ui.checkBoxContrib.setChecked(0)
                kdeui.KMessageBox.error(self,("You are not authorized for this operation."), "Authentication Error")
        else:
            if self.flagRepo != 1:
                self.removeRepo(self.repoName)

    def addRepo(self, r_name, r_address):
        try:
            link = comar.Link()
            link.setLocale()
            link.System.Manager["pisi"].addRepository(r_name, r_address)
            return True

        except:
            return False

    def getRepos(self):
        return repoList


    def removeRepo(self, r_name):
        try:
            link = comar.Link()
            link.setLocale()
            link.System.Manager["pisi"].removeRepository(r_name)
            return True
        except:
            return False

    def enableCheckTime(self):
        if self.ui.showTray.isChecked():
            self.ui.checkUpdate.setEnabled(True)
            self.ui.updateInterval.setEnabled(self.ui.checkUpdate.isChecked() and self.ui.showTray.isChecked())
        else:
            self.ui.checkUpdate.setEnabled(False)
            self.ui.updateInterval.setEnabled(False)

    def updateSelected(self):
        if self.ui.checkUpdate.isChecked():
            self.ui.updateInterval.setEnabled(True)
        else:
            self.ui.updateInterval.setEnabled(False)

    def applySettings(self):
        # write selected configurations to future package-managerrc
        config = KConfig("package-managerrc")
        group = config.group("General")
        group.writeEntry("SystemTray", str(self.ui.showTray.isChecked()))
        group.writeEntry("UpdateCheck", str(self.ui.checkUpdate.isChecked()))
        group.writeEntry("UpdateCheckInterval", str(self.ui.updateInterval.value() * 60))
        config.sync()

        if self.ui.showTray.isChecked():
            p = subprocess.Popen(["package-manager"], stdout=subprocess.PIPE)


    def shown(self):
        pass

    def execute(self):
        self.applySettings()
        return True



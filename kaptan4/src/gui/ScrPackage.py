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

from gui.ScreenWidget import ScreenWidget
from gui.packageWidget import Ui_packageWidget

import contribrepo
import pisi

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
        self.repoAddress = "http://paketler.pardus.org.tr/contrib-2007/pisi-index.xml.bz2"

        # set signals
        self.ui.showTray.connect(self.ui.showTray, SIGNAL("toggled(bool)"), self.enableCheckTime)
        self.ui.checkUpdate.connect(self.ui.checkUpdate, SIGNAL("toggled(bool)"), self.updateSelected)
        self.ui.checkBoxContrib.connect(self.ui.checkBoxContrib, SIGNAL("toggled(bool)"), self.slotContribRepo)

        # create a db object
        self.repodb = pisi.db.repodb.RepoDB()
        n = 1 # temporary index variable for repo names

        # control if we already have contrib repo
        # if so, hide configuration box
        if self.repodb.has_repo_url(self.repoAddress):
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

                message = ki18n("You are not authorized for this operation.")
                KMessageBox.error(self, message, ki18n("Authentication Error!"))
        else:
            if self.flagRepo != 1:
                self.removeRepo(self.repoName)

    def addRepo(self, r_name, r_address):
        try:
            contribrepo.addRepo(r_name, r_address)
            return True
        except Exception, e:
            if e.get_dbus_name().endswith('policy.no'):
                return False
            elif e.get_dbus_name().endswith('policy.auth_admin'):
                authResult = contribrepo.auth("addrepository")
            elif e.get_dbus_name().endswith('policy.auth_user'):
                authResult = contribrepo.auth("addrepository")
            else:
                return False
            try:
                if authResult:
                    contribrepo.addRepo(r_name, r_address)
                    return True
                else:
                    return False
            except:
                return False

    def removeRepo(self, r_name):
        try:
            contribrepo.removeRepo(r_name)
            return True
        except Exception, e:
            if e.get_dbus_name().endswith('policy.no'):
                return False
            elif e.get_dbus_name().endswith('policy.auth_admin'):
                authResult = contribrepo.auth("removerepository")
            elif e.get_dbus_name().endswith('policy.auth_user'):
                authResult = contribrepo.auth("removerepository")
            else:
                return False
            try:
                if authResult:
                    contribrepo.removeRepo(r_name)
                    return True
                else:
                    return False
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
            proc = KProcess()
            # call package manager

    def shown(self):
        pass

    def execute(self):
        self.applySettings()



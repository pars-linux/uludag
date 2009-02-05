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
        self.repoAddress = "http://paketler.pardus.org.tr/contrib-2008/pisi-index.xml.bz2"

        # add signals here

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
        if self.checkBoxContrib.isChecked():
            if self.addRepo(self.repoName, self.repoAddress) == False:
                self.flagRepo = 1
                self.ui.checkBoxContrib.setChecked(0)

                message = i18n("You are not authorized for this operation.")
                KMessageBox.error(self, message, ki18n("Authentication Error!"))
        else:
            if self.flagRepo != 1:
                self.removeRepo(self.repoName)

    def shown(self):
        pass

    def execute(self):
        return True



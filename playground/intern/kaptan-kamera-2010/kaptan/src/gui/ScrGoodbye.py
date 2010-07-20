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
from PyKDE4.kdecore import ki18n, KGlobal, KConfig
#from PyKDE4.kutils import KCModuleInfo, KCModuleProxy
import subprocess, sys
from gui.ScreenWidget import ScreenWidget
from gui.goodbyeWidget import Ui_goodbyeWidget
import gui.ScrSmolt as smoltWidget

sys.path.append('/usr/kde/4/share/apps/migration/')
from migration.utils import partition

class Widget(QtGui.QWidget, ScreenWidget):
    title = ki18n("More")
    desc = ki18n("Congratulations!")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_goodbyeWidget()
        self.ui.setupUi(self)

        lang = KGlobal.locale().language()

        if lang == "tr":
            self.helpPageUrl = "http://www.pardus.org.tr/destek"
        else:
            self.helpPageUrl = "http://www.pardus.org.tr/eng/support"

        self.smoltUrl = "http://smolt.pardus.org.tr:8090"

        users = partition.allUsers()
        if not users:
            self.ui.migrationGroupBox.hide()
            self.ui.label_2.hide()

        self.ui.buttonSystemSettings_2.connect(self.ui.buttonSystemSettings_2, SIGNAL("clicked()"), self.startSmolt)
        self.ui.buttonMigration.connect(self.ui.buttonMigration, SIGNAL("clicked()"), self.startMigration)
        self.ui.buttonSystemSettings.connect(self.ui.buttonSystemSettings, SIGNAL("clicked()"), self.startSystemSettings)
        self.ui.buttonHelpPages.connect(self.ui.buttonHelpPages, SIGNAL("clicked()"), self.startHelpPages)

    def startSystemSettings(self):
        self.procSettings = QProcess()
        self.procSettings.start("systemsettings")

    def startMigration(self):
        self.procSettings = QProcess()
        self.procSettings.start("migration")

    def startHelpPages(self):
        self.procSettings = QProcess()
        command = "kfmclient openURL " + self.helpPageUrl
        self.procSettings.start(command)

    def startSmolt(self):
        self.procSettings = QProcess()
        command = "kfmclient openURL " + self.smoltUrl
        self.procSettings.start(command)

    def setSmolt(self):
        if not self.smoltSettings["profileSend"]:
            self.ui.smoltGroupBox.hide()
            self.ui.label.hide()

    def shown(self):
       self.smoltSettings = smoltWidget.Widget.screenSettings
       self.setSmolt()

    def execute(self):
       return True



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
from PyKDE4.kdecore import ki18n, KGlobal
#from PyKDE4.kutils import KCModuleInfo, KCModuleProxy
import subprocess
from gui.ScreenWidget import ScreenWidget
from gui.goodbyeWidget import Ui_goodbyeWidget

class Widget(QtGui.QWidget, ScreenWidget):
    title = ki18n("Goodbye")
    desc = ki18n("Goodbye from Kaptan Wizard :)")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_goodbyeWidget()
        self.ui.setupUi(self)

        lang = KGlobal.locale().language()

        if lang == "tr":
            self.helpPageUrl = "http://www.pardus.org.tr/iletisim.html"
        else:
            self.helpPageUrl = "http://www.pardus.org.tr/eng/contact.html"

        self.ui.buttonSystemSettings.connect(self.ui.buttonSystemSettings, SIGNAL("clicked()"), self.startSystemSettings)
        self.ui.buttonHelpPages.connect(self.ui.buttonHelpPages, SIGNAL("clicked()"), self.startHelpPages)

    def startSystemSettings(self):
        self.procSettings = QProcess()
        self.procSettings.start("systemsettings")

    def startHelpPages(self):
        self.procSettings = QProcess()
        command = "kfmclient openURL " + self.helpPageUrl
        self.procSettings.start(command)

    def shown(self):
        pass

    def execute(self): 
       return True



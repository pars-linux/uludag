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
from screens.networkdlg import NetworkWidget

class Widget(NetworkWidget, ScreenWidget):

    # title and description at the top of the dialog window
    title = "Network Manager"
    desc = i18n("Configure network settings...")
    icon = "kaptan/pics/icons/network.png"

    running = False
    proc = QProcess()

    def __init__(self, *args):
        apply(NetworkWidget.__init__, (self,) + args)

        self.embedded = QXEmbed(self.networkFrame)
        self.embedded.resize(500,350)

        self.busy.setText(i18n("<big>Loading...</big>"))

        #set background image
        self.setPaletteBackgroundPixmap(QPixmap(locate("data", "kaptan/pics/middleWithCorner.png")))

    def __del__(self):
        if self.proc.isRunning():
            self.proc.kill()
            self.running = False

    def shown(self):
        if not self.running:
            self.proc.addArgument("kcmshell")
            self.proc.addArgument("--embed-proxy")
            self.proc.addArgument(QString.number(self.embedded.winId()))
            self.proc.addArgument("network-manager")

            code = self.proc.start()
            self.running = True

            self.connect(self.proc, SIGNAL("processExited()"),  self.endProcess)

    def endProcess(self):
        self.running = False

    def execute(self):
        pass



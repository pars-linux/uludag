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
from kdecore import KGlobal

from screens.Screen import ScreenWidget
from screens.goodbyedlg import GoodbyeWidget

import subprocess
import logging

class Widget(GoodbyeWidget, ScreenWidget):

    # title and description at the top of the dialog window
    title = "Goodbye!"
    desc = i18n("Enjoy with Pardus...")
    icon = "kaptan/pics/icons/goodbye.png"

    def __init__(self, *args):
        apply(GoodbyeWidget.__init__, (self,) + args)

        if KGlobal.locale().language() == "tr":
            self.helpUrl = "http://www.pardus.org.tr/destek"
        else:
            self.helpUrl = "http://www.pardus.org.tr/eng/support"

        self.minimumResolution = 800

        self.picTasma.setPixmap(QPixmap(locate("data", "kaptan/pics/icons/tasma.png")))
        #self.picFeedback.setPixmap(QPixmap(locate("data", "kaptan/pics/icons/feedback.png")))
        self.picHelp.setPixmap(QPixmap(locate("data", "kaptan/pics/icons/user_groups.png")))
        self.picResolution.setPixmap(QPixmap(locate("data", "kaptan/pics/icons/multiple.png")))

        # set background image
        self.setPaletteBackgroundPixmap(QPixmap(locate("data", "kaptan/pics/middleWithCorner.png")))

        # set signals
        self.connect(self.buttonTasma, SIGNAL("clicked()"), self.startTasma)
        self.connect(self.buttonHelp, SIGNAL("clicked()"), self.startHelp)
        self.connect(self.buttonResolution, SIGNAL("clicked()"), self.startDisplayManager)

        # if screen width smaller than 
        rect =  QApplication.desktop().screenGeometry()
        if rect.width() > self.minimumResolution:
            self.groupBoxResolution.hide()

    def isAppAvaiable(self, appName, widget2Hide):
        try:
            p = subprocess.Popen([appName], stdout = subprocess.PIPE)
            out, err = p.communicate()

            if out.strip() == "0":
                widget2Hide.hide()

        except OSError, e:
            logging.debug(appName + " is not installed: " + str(e))
            # hide app part, if it's not installed.
            widget2Hide.hide()

    def shown(self):
        pass

    def execute(self):
        return True

    def startDisplayManager(self):
        self.proc = QProcess()
        self.proc.addArgument("display-manager")
        self.proc.start()

    def startTasma(self):
        self.proc = QProcess()
        self.proc.addArgument("tasma")
        self.proc.start()

    def startHelp(self):
        self.proc = QProcess()
        self.proc.addArgument("firefox")
        self.proc.addArgument(self.helpUrl)
        self.proc.start()


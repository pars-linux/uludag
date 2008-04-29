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
    desc = "Enjoy with Pardus..."
    icon = "kaptan/pics/icons/goodbye.png"

    def __init__(self, *args):
        apply(GoodbyeWidget.__init__, (self,) + args)

        if KGlobal.locale().language() == "tr":
            self.helpUrl = "http://www.pardus.org.tr/iletisim.html"
        else:
            self.helpUrl = "http://www.pardus.org.tr/eng/contact.html"

        self.picMigration.setPixmap(QPixmap(locate("data", "kaptan/pics/icons/migration.png")))
        self.picTasma.setPixmap(QPixmap(locate("data", "kaptan/pics/icons/tasma.png")))
        self.picFeedback.setPixmap(QPixmap(locate("data", "kaptan/pics/icons/feedback.png")))
        self.picHelp.setPixmap(QPixmap(locate("data", "kaptan/pics/icons/user_groups.png")))

        # set background image
        self.setPaletteBackgroundPixmap(QPixmap(locate("data", "kaptan/pics/middleWithCorner.png")))

        # set signals
        self.connect(self.buttonMigration, SIGNAL("clicked()"), self.startMigration)
        self.connect(self.buttonTasma, SIGNAL("clicked()"), self.startTasma)
        self.connect(self.buttonHelp, SIGNAL("clicked()"), self.startHelp)

        try:
            p = subprocess.Popen(["mdsadigration-users"], stdout = subprocess.PIPE)
            out, err = p.communicate()

            isMigrationAvaiable = out
            if isMigrationAvaiable:
                self.groupBoxMigration.hide()
        except OSError, e:
            print "Error: ", e
            logging.debug("Migration is not installed: " + str(e))
            # hide migration part, if it's not installed.
            self.groupBoxMigration.hide()

    def shown(self):
        pass

    def execute(self):
        return True

    def startMigration(self):
        self.proc = QProcess()
        self.proc.addArgument("migration")
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


# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

from PyQt4 import QtGui
from PyQt4.QtCore import *

import yali4.sysutils
from yali4.gui.ScreenWidget import ScreenWidget
from yali4.gui.Ui.welcomewidget import Ui_WelcomeWidget
import yali4.gui.context as ctx
from yali4.gui.YaliDialog import Dialog
import GUIGPL

##
# Welcome screen is the first screen to be shown.
class Widget(QtGui.QWidget, ScreenWidget):
    title = _('Welcome !! ')
    desc = _('Welcome to the Pardus installer...')
    help = _('''
<font size="+2">Welcome !</font>
<font size="+1"><p>Welcome to Pardus 2008 that contains many easy-to-use software components. You can do everything you need to, including, but not limited to, connecting to the Internet, creating documents, playing games, listening to music using Pardus 2008.</p>
<p>This application will help you with the installation of Pardus 2008 to your computer in few and easy steps and then do what is necessary to identify and configure your hardware. We advise you to backup your data in your disk(s) before starting with the installation.</p>
<p>You can start the installation process (and step in on a free world) by pressing the Next button.</p>
</font>
''')

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_WelcomeWidget()
        self.ui.setupUi(self)
        self.ui.rebootButton.setEnabled(False)

        self.connect(self.ui.not_accept, SIGNAL("toggled(bool)"),
                     self.slotNotAcceptToggled)

        self.connect(self.ui.accept, SIGNAL("toggled(bool)"),
                     self.slotAcceptToggled)

        self.connect(self.ui.rebootButton, SIGNAL("clicked()"),
                     self.slotReboot)

        self.connect(self.ui.gplButton, SIGNAL("clicked()"),
                     self.showGPL)

    def slotAcceptToggled(self, b):
        if b:
            self.__enable_next(True)

    def slotNotAcceptToggled(self, b):
        if b:
            self.__enable_next(False)

    def __enable_next(self, b):
        if b:
            ctx.mainScreen.enableNext()
            self.ui.rebootButton.setEnabled(False)
        else:
            ctx.mainScreen.disableNext()
            self.ui.rebootButton.setEnabled(True)

    def showGPL(self):
        # make a GPL dialog
        r = GUIGPL.Widget(self)
        d = Dialog("GPL", r, self)
        d.resize(500,400)
        d.exec_()

    def slotReboot(self):
        yali4.sysutils.fastreboot()

    def shown(self):
        ctx.mainScreen.disableBack()
        if self.ui.accept.isChecked():
            ctx.mainScreen.enableNext()
        else:
            ctx.mainScreen.disableNext()
        ctx.mainScreen.processEvents()


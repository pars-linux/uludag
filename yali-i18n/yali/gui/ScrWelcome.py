# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import gettext
__trans = gettext.translation('yali', fallback=True)
_ = __trans.ugettext

from PyQt4 import QtGui
from PyQt4.QtCore import *

import yali.sysutils
from yali.gui.ScreenWidget import ScreenWidget
from yali.gui.Ui.welcomewidget import Ui_WelcomeWidget
import yali.gui.context as ctx
from yali.gui.YaliDialog import Dialog
from yali.gui.GUIAdditional import Gpl

##
# Welcome screen is the first screen to be shown.
class Widget(QtGui.QWidget, ScreenWidget):
    title = _("Welcome to Pardus")
    # FIXME: Use system's pardus release to gather version info and use it if needed
    help = _("""
<font size="+2">Welcome</font>
<font size="+1"><p>Pardus offers many easy-to-use tools for your desktop. The first of all, is this application which will help you to install Pardus easily.</p>
<p>After you accept General Public License (GPL), and please read it as it guarantees <strong>your freedom</strong>, you can start installation steps, where you can choose which disk/partition to use, your username/password etc. then Pardus will be configure your hardware and be installed.</p>
<p>We strongly suggest you to backup your data before starting.</p>
</font>
""")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_WelcomeWidget()
        self.ui.setupUi(self)

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
        else:
            ctx.mainScreen.disableNext()

    def showGPL(self):
        # make a GPL dialog
        d = Dialog("GPL", Gpl(self), self)
        d.resize(500,400)
        d.exec_()

    def slotReboot(self):
        yali.sysutils.ejectCdrom()
        yali.sysutils.reboot()

    def shown(self):
        ctx.mainScreen.disableBack()
        if self.ui.accept.isChecked():
            ctx.mainScreen.enableNext()
        else:
            ctx.mainScreen.disableNext()
        ctx.mainScreen.processEvents()


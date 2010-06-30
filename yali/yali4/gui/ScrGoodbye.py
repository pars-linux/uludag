# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2008, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import os

import gettext
__trans = gettext.translation('yali', fallback=True)
_ = __trans.ugettext

from PyQt4 import QtGui
from PyQt4.QtCore import *

import dbus
import time
import yali.sysutils
import yali.users
import yali.localeutils
import yali.postinstall
import yali.bootloader
import yali.storage
import yali.partitionrequest as partrequest
import yali.partitiontype as parttype
from os.path import basename
from yali.gui.ScreenWidget import ScreenWidget
from yali.gui.YaliDialog import InfoDialog
from yali.gui.YaliSteps import YaliSteps
from yali.gui.Ui.goodbyewidget import Ui_GoodByeWidget
import yali.gui.context as ctx
from yali.gui.installdata import *

##
# Goodbye screen
class Widget(QtGui.QWidget, ScreenWidget):
    title = _('Goodbye from YALI')
    desc = _('Enjoy your fresh Pardus !...')
    help = _('''
<font size="+2">Congratulations</font>


<font size="+1">
<p>
You have successfully installed Pardus, a very easy to use desktop system on
your machine. Now you can start playing with your system and stay productive
all the time.
</p>
<P>
Click on the Next button to proceed. One note: You remember your password,
don't you?
</p>
</font>
''')

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_GoodByeWidget()
        self.ui.setupUi(self)

        self.steps = YaliSteps()

    def shown(self):
        ctx.mainScreen.disableNext()
        ctx.yali.info.updateAndShow(_("Running post install operations.."))
        ctx.mainScreen.disableBack()
        ctx.yali.processPendingActions(self)
        self.steps.slotRunOperations()
        if not ctx.mainScreen.ui.helpContent.isVisible():
            ctx.mainScreen.slotToggleHelp()
        self.ui.label.setPixmap(QtGui.QPixmap(":/gui/pics/goodbye.png"))
        ctx.yali.info.hide()
        ctx.mainScreen.enableNext()

    def execute(self):
        ctx.mainScreen.disableNext()

        ctx.debugger.log("Show reboot dialog.")
        InfoDialog(_("Press <b>Reboot</b> button to restart your system."), _("Reboot"))

        ctx.yali.info.updateAndShow(_('<b>Rebooting system. Please wait!</b>'))

        # remove cd...
        if not ctx.yali.install_type == YALI_FIRSTBOOT:
            ctx.debugger.log("Trying to eject the CD.")
            yali.sysutils.ejectCdrom()

        ctx.debugger.log("Yali, reboot calling..")

        ctx.mainScreen.processEvents()
        time.sleep(4)
        yali.sysutils.reboot()


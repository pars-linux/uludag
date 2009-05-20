# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TUBITAK/UEKAE
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

import time
from yali4 import sysutils
import yali4.partitionrequest as request
import yali4.partitiontype as parttype
from yali4.gui.ScreenWidget import ScreenWidget
from yali4.gui.YaliDialog import WarningDialog, RebootWidget
from yali4.gui.YaliSteps import YaliSteps
from yali4.gui.Ui.goodbyewidget import Ui_GoodByeWidget
import yali4.gui.context as ctx
from yali4.gui.installdata import *

##
# Goodbye screen
class Widget(QtGui.QWidget, ScreenWidget):
    title = _('Rescue Mode')
    desc = _('Final step of Rescue operations...')
    help = _('''
<font size="+2">Rescue Mode</font>
<font size="+1"><p>Click <b>next</b> to reboot !</p></font>
''')

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_GoodByeWidget()
        self.ui.setupUi(self)

        self.steps = YaliSteps()
        self.steps.setOperations([{"text":      _("Installing BootLoader..."),
                                   "operation": self.installBootLoader}])

    def installBootLoader(self):
        # Mount selected partition
        ctx.partrequests.append(request.MountRequest(ctx.installData.rescuePartition, parttype.root))
        ctx.partrequests.applyAll()

        # Install bootloader
        ctx.yali.installBootloader(ctx.installData.rescuePartition)

    def shown(self):
        ctx.mainScreen.disableNext()
        ctx.yali.info.updateAndShow(_("Running rescue operations.."))
        ctx.mainScreen.disableBack()
        self.steps.slotRunOperations()
        if not ctx.mainScreen.helpContent.isVisible():
            ctx.mainScreen.slotToggleHelp()
        self.ui.label.setPixmap(QtGui.QPixmap(":/gui/pics/goodbye.png"))
        ctx.yali.info.hide()
        ctx.mainScreen.enableNext()

    def execute(self):
        ctx.mainScreen.disableNext()

        w = RebootWidget(self)

        ctx.debugger.log("Show reboot dialog.")
        self.dialog = WarningDialog(w, self)
        self.dialog.exec_()
        ctx.mainScreen.processEvents()
        ctx.yali.info.updateAndShow(_('<b>Rebooting system. Please wait!</b>'))

        # remove cd...
        if not ctx.yali.install_type == YALI_FIRSTBOOT:
            ctx.debugger.log("Trying to eject the CD.")
            sysutils.eject_cdrom()

        ctx.debugger.log("Yali, fastreboot calling..")

        ctx.mainScreen.processEvents()
        sysutils.run("sync")
        time.sleep(4)
        sysutils.fastreboot()


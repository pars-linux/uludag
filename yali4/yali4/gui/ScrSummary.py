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

import os

import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

from PyQt4 import QtGui
from PyQt4.QtCore import *

import yali4.sysutils
from yali4.gui.ScreenWidget import ScreenWidget
from yali4.gui.YaliDialog import WarningDialog, WarningWidget
from yali4.gui.Ui.summarywidget import Ui_SummaryWidget
import yali4.gui.context as ctx

# Auto Partition Methods
methodUseAvail, methodEraseAll = range(2)

##
# Summary screen
class Widget(QtGui.QWidget, ScreenWidget):
    title = _('The last step before install')
    desc = _('Summary of your installation..')
    #icon = "iconKeyboard"
    help = _('''
<font size="+2">Install Summary</font>
<font size="+1">
<p>
Here you can see your install options and look at them again before installation starts.
</p>
</font>
''')

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_SummaryWidget()
        self.ui.setupUi(self)

        self.ui.content.setText("")
        self.connect(self.ui.install, SIGNAL("clicked()"),ctx.mainScreen.slotNext)
        self.connect(self.ui.cancel, SIGNAL("clicked()"),self.slotReboot)

    def slotReboot(self):
        w = WarningWidget(self)
        w.warning.setText(_('''<b><p>This action will reboot your system !</p></b>'''))
        w.ok.setText(_("Reboot"))
        dialog = WarningDialog(w, self)
        if self.dialog.exec_():
            yali4.sysutils.fastreboot()

    def shown(self):
        ctx.mainScreen.disableNext()

    def execute(self):

        ctx.mainScreen.processEvents()

        # We should do partitioning operations in here.
        if ctx.options.dryRun == True:
            ctx.debugger.log("dryRun activated Yali stopped")
            return

        # Auto Partitioning
        if ctx.installData.autoPartDev:
            ctx.use_autopart = True

            if ctx.installData.autoPartMethod == methodEraseAll:
                ctx.yali.autoPartDevice()
                ctx.yali.checkSwap()
                ctx.yali.info.updateMessage(_("Formatting ..."))
                ctx.mainScreen.processEvents()
                ctx.partrequests.applyAll()

            elif ctx.installData.autoPartMethod == methodUseAvail:
                ctx.yali.autoPartUseAvail()
                ctx.yali.checkSwap()
                ctx.yali.info.updateMessage(_("Formatting ..."))
                ctx.mainScreen.processEvents()
                ctx.partrequests.applyAll()

        # Manual Partitioning
        else:
            ctx.debugger.log("Format Operation Started")
            ctx.yali.info.updateAndShow(_("Writing disk tables ..."))
            for dev in yali4.storage.devices:
                ctx.mainScreen.processEvents()
                dev.commit()
            # wait for udev to create device nodes
            time.sleep(2)
            ctx.yali.checkSwap()
            ctx.yali.info.updateMessage(_("Formatting ..."))
            ctx.mainScreen.processEvents()
            ctx.partrequests.applyAll()
            ctx.debugger.log("Format Operation Finished")

        ctx.yali.info.hide()

        return True


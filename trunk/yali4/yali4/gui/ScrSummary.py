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

# base
import os
import time
import yali4.sysutils
from yali4.gui.installdata import *

# multi language
import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

# PyQt4 Rocks
from PyQt4 import QtGui
from PyQt4.QtCore import *

# libParted
from yali4.parteddata import *
import yali4.partitionrequest as request
import yali4.partitiontype as parttype

# GUI Stuff
from yali4.gui.ScreenWidget import ScreenWidget
from yali4.gui.YaliDialog import WarningDialog, WarningWidget
from yali4.gui.Ui.summarywidget import Ui_SummaryWidget
import yali4.gui.context as ctx

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
        if dialog.exec_():
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
                ctx.yali.info.updateAndShow(_("Resizing ..."))
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

        # Find GRUB Dev
        root_part_req = ctx.partrequests.searchPartTypeAndReqType(parttype.root,
                                                                  request.mountRequestType)

        if ctx.installData.bootLoaderOption == B_DONT_INSTALL:
            ctx.installData.bootLoaderDev = None
        elif ctx.installData.bootLoaderOption == B_INSTALL_PART:
            ctx.installData.bootLoaderDev = basename(root_part_req.partition().getPath())
        elif ctx.installData.bootLoaderOption == B_INSTALL_MBR:
            ctx.installData.bootLoaderDev = basename(self.device.getPath())
        else:
            ctx.yali.guessBootLoaderDevice()

        root_part_req = ctx.partrequests.searchPartTypeAndReqType(parttype.root,request.mountRequestType)
        _ins_part = root_part_req.partition().getPath()

        ctx.debugger.log("Pardus Root is : %s" % _ins_part)
        ctx.debugger.log("GRUB will be installing to : %s" % ctx.installData.bootLoaderDev)

        return True


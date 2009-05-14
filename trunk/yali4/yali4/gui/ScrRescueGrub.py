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

import os
import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL

import yali4.storage
from yali4.gui.installdata import *
from yali4.gui.GUIAdditional import DeviceItem
from yali4.gui.ScreenWidget import ScreenWidget
from yali4.gui.Ui.rescuegrubwidget import Ui_RescueGrubWidget
from yali4.gui.GUIException import GUIException
import yali4.gui.context as ctx

##
# BootLoader screen.
class Widget(QtGui.QWidget, ScreenWidget):
    title = _('Rescue Mode for Bootlooader')
    desc = _('You can fix your bootloader...')
    icon = "iconBootloader"
    help = _('''
<font size="+2">Boot loader setup</font>
<font size="+1">
<p>
Pardus 2009 uses a boot manager called GRUB to start the operating system you choose.
</p>
<p>If there are multiple operating systems in your computer, you can start the one 
you like using GRUB. Installing GRUB to the beginning of the boot disk is the advised 
option to avoid boot problems.  If you are sure you know what you are doing, 
you can change boot loader settings.
</p>
<p>
Please refer to Pardus Installing and Using 
Guide for more information about GRUB boot 
loader.
</p>
</font>
''')

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_RescueGrubWidget()
        self.ui.setupUi(self)

        self.ui.installFirstMBR.setChecked(True)

        if len(yali4.storage.devices) > 1:
            self.device_list_state = True
            # fill device list
            for dev in yali4.storage.devices:
                DeviceItem(self.ui.deviceList, dev)
            # select the first disk by default
            self.ui.deviceList.setCurrentRow(0)
            # be sure first is selected device
            self.device = self.ui.deviceList.item(0).getDevice()
        else:
            # don't show device list if we have just one disk
            self.ui.installMBR.hide()
            self.device_list_state = False
            self.ui.deviceList.hide()
            self.ui.select_disk_label.hide()

            self.device = yali4.storage.devices[0]

        self.connect(self.ui.deviceList, SIGNAL("currentItemChanged(QListWidgetItem*,QListWidgetItem*)"), self.slotDeviceChanged)
        self.connect(self.ui.deviceList, SIGNAL("itemClicked(QListWidgetItem*)"), self.slotSelect)

    def shown(self):
        yali4.storage.setOrderedDiskList()
        print ctx.installData.orderedDiskList
        ctx.debugger.log("Disks BIOS Boot order : %s " % ','.join(ctx.installData.orderedDiskList))

    def slotSelect(self):
        self.ui.installSelectedDisk.toggle()

    def slotDeviceChanged(self, o, n):
        self.device = o.getDevice()
        ctx.bootLoaderOptionalDev = self.device

    def execute(self):
        ctx.installData.bootLoaderOptionalDev = self.device
        print self.device

        # Apply GRUB Options
        if self.ui.installSelectedPart.isChecked():
            ctx.installData.bootLoaderOption = B_INSTALL_PART
            ###### ctx.installData.bootLoaderDev = os.path.basename(SELECTEDPARTITION)
        elif self.ui.installSelectedDisk.isChecked():
            ctx.installData.bootLoaderOption = B_INSTALL_MBR
            ctx.installData.bootLoaderDev = os.path.basename(ctx.installData.bootLoaderOptionalDev.getPath())
        elif self.ui.installFirstMBR:
            ctx.installData.bootLoaderOption = B_INSTALL_SMART
            ctx.yali.guessBootLoaderDevice()

        print "Option", ctx.installData.bootLoaderOption
        print "Dev", ctx.installData.bootLoaderDev

        return True

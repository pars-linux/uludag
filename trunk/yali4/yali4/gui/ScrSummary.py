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
        self.fillContent()

    def fillContent(self):
        subject = "<p><li><b>%s</b></li><ul>"
        item    = "<li>%s</li>"
        end     = "</ul></p>"
        content = QString("")

        content.append("""<html><body><ul>""")

        # Keyboard Layout
        content.append(subject % _("Localization Settings"))
        content.append(item % _("Selected language is <b>%s</b>") % ctx.installData.keyData["name"])
        variant = ctx.installData.keyData["xkbvariant"] or ''
        content.append(item % _("Selected keyboard layout is <b>%s%s</b>") % (ctx.installData.keyData["xkblayout"],variant))
        content.append(end)

        # TimeZone
        content.append(subject % _("Date/Time Settings"))
        content.append(item % _("Selected TimeZone is <b>%s</b>") % ctx.installData.timezone)
        content.append(end)

        # Users
        content.append(subject % _("User Settings"))
        for user in yali4.users.pending_users:
            state = _("User %s (<b>%s</b>) added.")
            if "wheel" in user.groups:
                state = _("User %s (<b>%s</b>) added with <u>admin privileges</u>.")
            content.append(item % state % (user.realname, user.username))
        content.append(end)

        # HostName
        content.append(subject % _("Hostname Settings"))
        content.append(item % _("Hostname is set as <b>%s</b>") % ctx.installData.hostName)
        content.append(end)

        # Partition
        content.append(subject % _("Partition Settings"))
        if ctx.installData.autoPartMethod == methodEraseAll:
            content.append(item % _("Automatic Partitioning selected."))
            dev = ctx.installData.autoPartDev
            _sum = {"device":dev.getModel(),
                    "partition":dev.getName()+"1",
                    "size":dev.getTotalMB(),
                    "fs":parttype.root.filesystem.name(),
                    "type":parttype.root.name}

            content.append(item % _("All partitions on device <b>%(device)s</b> has been deleted.") % _sum)
            content.append(item % _("Partition <b>%(partition)s</b> <b>added</b> to device <b>%(device)s</b> with <b>%(size)s MB</b> as <b>%(fs)s</b>.") % _sum)
            content.append(item % _("Partition <b>%(partition)s</b> <b>selected</b> as <b>%(type)s</b>.") % _sum)

        elif ctx.installData.autoPartMethod == methodUseAvail:
            content.append(item % _("Automatic Partitioning (resize method) selected."))
            dev = ctx.installData.autoPartDev
            _part = ctx.installData.autoPartPartition
            part = _part["partition"]
            newPartSize = int(_part["newSize"]/2)
            ctx.debugger.log("UA: newPartSize : %s " % newPartSize)
            resizeTo = int(part.getMB()) - newPartSize

            _sum = {"device":dev.getModel(),
                    "partition":part.getName(),
                    "newPartition":"%s%s" % (part.getName()[:-1],int(part._minor)+1),
                    "size":newPartSize,
                    "currentFs":part._fsname,
                    "fs":parttype.root.filesystem.name(),
                    "type":parttype.root.name,
                    "currentSize":part.getMB(),
                    "resizeTo":resizeTo}

            content.append(item % _("Partition <b>%(partition)s - %(currentFs)s</b> <b>resized</b> to <b>%(resizeTo)s MB</b>, old size was <b>%(currentSize)s MB</b>") % _sum)
            content.append(item % _("Partition <b>%(newPartition)s</b> <b>added</b> to device <b>%(device)s</b> with <b>%(size)s MB</b> as <b>%(fs)s</b>.") % _sum)
            content.append(item % _("Partition <b>%(newPartition)s</b> <b>selected</b> as <b>%(type)s</b>.") % _sum)

        else:
            for operation in ctx.partSum:
                content.append(item % operation)
        content.append(end)

        # Bootloader
        content.append(subject % _("Bootloader Settings"))
        if ctx.installData.bootLoaderOption == B_DONT_INSTALL:
            content.append(item % _("GRUB will not be installed"))
        """
        elif ctx.installData.bootLoaderOption == B_INSTALL_PART:
            ctx.installData.bootLoaderDev = basename(root_part_req.partition().getPath())
        elif ctx.installData.bootLoaderOption == B_INSTALL_MBR:
            ctx.installData.bootLoaderDev = basename(self.device.getPath())
        else:
            ctx.yali.guessBootLoaderDevice()

        content.append(item % _("GRUB will be installing to <b>%s</b>") % ctx.installData.hostName)
        """
        content.append(end)

        content.append("""</ul></body></html>""")

        self.ui.content.setHtml(content)

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


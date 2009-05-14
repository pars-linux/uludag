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
from PyQt4.QtCore import *

import yali4.storage
from yali4.gui.ScreenWidget import ScreenWidget
from yali4.gui.Ui.rescuewidget import Ui_RescueWidget
import yali4.gui.context as ctx

class Widget(QtGui.QWidget, ScreenWidget):
    title = _('Rescue Mode')
    desc = _('You can reinstall your Grub or you can take back your system by using Pisi History...')
    icon = ""
    help = _('''
<font size="+2">Rescue Mode</font>
<font size="+1"><p>This is a rescue mode help document.</p></font>
''')

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_RescueWidget()
        self.ui.setupUi(self)
        self.radios = [self.ui.useGrub, self.ui.usePisiHs]
        self.isSuitableForRescue = True

        # initialize all storage devices
        if not yali4.storage.init_devices():
            raise GUIException, _("Can't find a storage device!")

        # Get usable partitions for rescue
        self.partitionList = PardusPartitions(self)

        for radio in self.radios:
            self.connect(radio, SIGNAL("toggled(bool)"), ctx.mainScreen.enableNext)

    def updateNext(self):
        for radio in self.radios:
            if radio.isChecked():
                ctx.mainScreen.enableNext()
                return
        ctx.mainScreen.disableNext()
        ctx.mainScreen.processEvents()

    def shown(self):
        ctx.mainScreen.disableBack()
        self.updateNext()

class PardusPartitions:
    def __init__(self, parentWidget):
        isPardusFound, partitionList = self.scanDisks()
        if len(partitionList) == 0:
            _msg = _("Yali couldn't find a suitable partition on your system")
            parentWidget.ui.partitionList.hide()
            parentWidget.isSuitableForRescue = False
        else:
            for p in partitionList:
                partition = p['partition']
                _info = "%s - %s %s" % (partition.getDevice().getModel(),
                                         partition.getPath(),
                                         p['release'])
                item = QtGui.QListWidgetItem(QtGui.QIcon(":/gui/pics/iconPartition.png"), _info)
                parentWidget.ui.partitionList.addItem(item)

        if isPardusFound:
            _msg = _("Yalı found a Pardus installed partition on your system.")
            if len(partitionList) > 1:
                _msg += _("Please select a partition from list.")
            else:
                parentWidget.ui.partitionList.hide()
        elif len(partitionList) > 0:
            _msg = _("Yalı couldn't find a Pardus installed partition on your system. But there is a Linux installed partitions.")
            if len(partitionList) > 1:
                _msg += _("Please select a partition from list")
            else:
                parentWidget.ui.partitionList.hide()

        parentWidget.ui.infoLabel.setText(_msg)

    def scanDisks(self):
        pardusPartitions = []
        linuxPartitions  = []
        ctx.debugger.log("Checking for Pardus ...")
        for disk in yali4.storage.devices:
            for partition in disk.getPartitions():
                print "Checking ... ", partition.getPath()
                fs = partition.getFSName()
                if fs in ("ext4", "ext3", "reiserfs", "xfs"):
                    linuxPartitions.append({'partition':partition, 'release':''})
                    ctx.debugger.log("Partition found which has usable fs (%s)" % partition.getPath())
                    guest_grub_conf = yali4.sysutils.is_linux_boot(partition.getPath(), fs)
                    if guest_grub_conf:
                        pardus_release = yali4.sysutils.pardus_release()
                        if pardus_release:
                            pardusPartitions.append({'partition':partition, 'release':pardus_release})
                    # If it is not a pardus installed partition skip it
                    yali4.sysutils.umount_()
        if len(pardusPartitions) > 0:
            return (True, pardusPartitions)
        return (False, linuxPartitions)

    def addPartition(self, path, label, version=None):
        pass


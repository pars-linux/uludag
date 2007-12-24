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

import yali4.gui.context as ctx
import yali4.partitionrequest as request
import yali4.partitiontype as parttype
from yali4.gui.YaliDialog import Dialog, WarningDialog, WarningWidget
#from yali4.gui.InformationWindow import InformationWindow
from yali4.gui.GUIException import *
from yali4.gui.ScreenWidget import ScreenWidget
from yali4.gui.PartListImpl import PartList
from yali4.gui.PartEditImpl import PartEdit, \
    editState, createState, deleteState, resizeState

##
# Partitioning screen.
class Widget(QGui.QWidget, ScreenWidget):
    title = _('Manual Partitioning')
    desc = _('You can easily configure your partitions..')
    help = _('''
<font size="+2">Partitioning your hard disk</font>

<font size="+1">
<p>
Pardus can be installed on a variety of hardware. You can install Pardus
on an empty disk or hard disk partition. <b>An installation will automatically
destroy the previously saved information on selected partitions. </b>
</p>
<p>
In order to use Pardus, you must create one Linux filesystem (for the 
system files), which is mandatory and a swap space 
(for improved performance), which is optional. This swap space 
is used whenever system needs more memory, but the system lacks it.
We advise you to allocate at least 4 GBs of hard disk area and 
swap space (between 500 MB - 2 GB, according to your needs) for 
convenience. A Linux partition size less than 3.5 GB is not allowed.
You may also optionally use another disk partition for storing 
user files.
</p>
<p>
You need to format a Linux partition, if it's used for the first time.
You can enable \'Use available free space\' option, if the hard disk's 
remaining space is to be used automatically.
</p>
<p>
The partition table shows the device, size, partition type and
filesystem information. If the partition will be formatted during
Pardus installation stage, then the corresponding \'Format\' 
column will be enabled.
</p>
<p>
Please refer to Pardus Installing and Using Guide for more information
about disk partitioning.
</p>
</font>
''')


    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)

        self.partlist = PartList(self)
        self.partedit = PartEdit(self)
        self.partedit.hide()
        self.dialog = None

        vbox = QVBoxLayout(self)
        vbox.addWidget(self.partlist)

        self.connect(self.partlist, PYSIGNAL("signalCreate"),
                     self.slotCreatePart)

        self.connect(self.partlist, PYSIGNAL("signalDelete"),
                     self.slotDeletePart)

        self.connect(self.partlist, PYSIGNAL("signalEdit"),
                     self.slotEditPart)

        self.connect(self.partlist, PYSIGNAL("signalResize"),
                     self.slotResizePart)

        self.connect(self.partedit, PYSIGNAL("signalApplied"),
                     self.slotApplied)

        self.connect(self.partedit, PYSIGNAL("signalCanceled"),
                     self.slotCanceled)


    def shown(self):
        from os.path import basename
        ctx.debugger.log("%s loaded" % basename(__file__))
        ctx.screens.disableNext()
        self.partlist.update()

    ##
    # do the work and run requested actions on partitions.
    def execute(self):
        ctx.debugger.log("Manual Partitioning selected...")
        ctx.screens.processEvents()
        return True

    def slotCreatePart(self, parent, d):
        self.partedit.setState(createState, d)
        self.dialog = Dialog(_("Create Partition"), self.partedit, self)
        self.dialog.exec_loop()

    def slotDeletePart(self, parent, d):
        self.partedit.setState(deleteState, d)
        self.dialog = Dialog(_("Delete Partition"), self.partedit, self)
        self.dialog.exec_loop()

    def slotEditPart(self, parent, d):
        self.partedit.setState(editState, d)
        self.dialog = Dialog(_("Edit Partition"), self.partedit, self)
        self.dialog.exec_loop()

    def slotResizePart(self, parent, d):
        self.partedit.setState(resizeState, d)
        self.dialog = Dialog(_("Resize Partition"), self.partedit, self)
        self.dialog.exec_loop()

    def slotApplied(self):
        self.dialog.done(0)
        self.partlist.update()

    def slotCanceled(self):
        self.dialog.reject()



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

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *

import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

import yali4.storage
import yali4.filesystem as filesystem
import yali4.partitionrequest as request
import yali4.partitiontype as parttype
import yali4.parteddata as parteddata

import yali4.gui.context as ctx
from yali4.gui.Ui.partlistwidget import Ui_PartListWidget
from yali4.gui.GUIException import *

class DiskList(QtGui.QWidget):
    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.resize(QSize(QRect(0,0,600,80).size()).expandedTo(self.minimumSizeHint()))
        self.setStyleSheet("""
            QToolBox::tab { background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                        stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                                        stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
                            border-radius: 5px; }
            QRadioButton::indicator { width:1px;height:1px;border-color:white; }
            QRadioButton:checked { border:3px solid #777 }
            QSplitter::handle { background-color:white; }
        """)
        self.gridlayout = QtGui.QGridLayout(self)
        self.toolBox = QtGui.QToolBox(self)
        self.gridlayout.addWidget(self.toolBox,0,0,1,1)
        self.initDevices()

    def addDisk(self,dw):
        self.toolBox.addItem(dw,dw.name)

    def update(self):

        #FIXME
        #self.clearList()

        for dev in self.devs:
            ctx.debugger.log("Device Found %s" % dev)
            self.addDevice(dev)

        # self.showPartitionRequests()
        # self.checkRootPartRequest()

    def initDevices(self):
        self.devs = []
        # initialize all storage devices
        if not yali4.storage.init_devices():
            raise GUIException, _("Can't find a storage device!")

        # for consistency list devices in reverse order.
        self.devs = [i for i in yali4.storage.devices]
        self.devs.reverse()

    def resetChanges(self):
        yali4.storage.clear_devices()
        self.initDevices()
        #ctx.partrequests.remove_all()
        #self.update()

    def addDevice(self, dev):

        def sizePix(mb,total):
            return (self.toolBox.width() * total) / mb

        def sizeStr(mb):
            if mb > 1024:
                return _("%0.1f GB free") % long(mb/1024.0)
            else:
                return _("%d MB free") % mb

        # add the device to the list
        devstr = u"%s (%s)" % (dev.getModel(), dev.getName())
        freespace = dev.getFreeMB()
        if freespace:
            size_str = dev.getSizeStr() + "  (%s)" % sizeStr(freespace)
        else:
            size_str = dev.getSizeStr()

        d = DiskItem("%s - %s" % (devstr,size_str))
        d.setData(dev)
        self.addDisk(d)

        # than add extended partition to reparent logical ones
        # fixme
        if dev.hasExtendedPartition() and 1==0:
            ext = dev.getExtendedPartition()
            free_ext = ext.getFreeMB()
            if free_ext:
                size_str = ext.getSizeStr() + "  (%s)" % sizeStr(free_ext)
            else:
                size_str = ext.getSizeStr()

            e = PartListItem(d,
                             _("Extended"),
                             size_str)
            e.setData(ext)

        # add partitions on device
        for part in dev.getOrderedPartitionList():
            parent_item = d
            if part.isExtended():
                continue
            elif part.getType() == parteddata.freeSpaceType:
                # Don't show free space as a new item on GUI #
                #name = _("Free")
                continue
            name = _("Partition %d") % part.getMinor()
            parent_item.addPartition(name,part)

            # use the first found "linux-swap" partition as swap (# 1049)
            if part.getFSName() == "linux-swap(new)" and not self.autoSwapSelected:
                ctx.partrequests.append(
                    request.MountRequest(part, parttype.swap))
                ctx.partrequests.append(
                    request.FormatRequest(part, parttype.swap))
                ctx.partrequests.append(
                    request.LabelRequest(part, parttype.swap))
                self.autoSwapSelected = True


class DiskItem(QtGui.QWidget):
    # storage.Device or partition.Partition
    _data = None

    def __init__(self, name):
        QtGui.QWidget.__init__(self,None)
        self.layout = QtGui.QGridLayout(self)
        self.layout.setContentsMargins(1,0,1,0)
        self.diskGroup = QtGui.QGroupBox(self)
        self.diskGroup.setMinimumSize(QSize(570,70))
        self.diskGroup.setMaximumSize(QSize(570,70))
        self.gridlayout = QtGui.QGridLayout(self.diskGroup)
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(0)
        self.splinter = QtGui.QSplitter(Qt.Horizontal,self.diskGroup)
        self.splinter.setHandleWidth(2)
        self.gridlayout.addWidget(self.splinter,0,0,1,1)
        self.layout.addWidget(self.diskGroup)
        self.partitions = []
        self.name = name

    def addPartition(self,name=None,data=None):
        partition = QtGui.QRadioButton("%s\n%s" % (name,data.getSizeStr()),self.diskGroup)
        partition.setStyleSheet("background-color:lightblue")
        partition.setMinimumSize(QSize(100,0))
        partition.setFocusPolicy(Qt.NoFocus)

        self.splinter.addWidget(partition)

        policy = partition.sizePolicy();
        policy.setHorizontalStretch(100);
        partition.setSizePolicy(policy);
        self.partitions.append({"name":name,"data":data})
        #{"size":part.getSizeStr(),
        # "installType":"",
        # "filesystem":part.getFSName()}

    def setData(self, d):
        self._data = d

    def getData(self):
        return self._data

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    diskList = DiskList()

    disk1 = DiskItem("/dev/sda")
    disk1.addPartition("/dev/sda1",{"size":"50GB"})
    disk1.addPartition("/dev/sda2",{"size":"50GB"})
    diskList.addDisk(disk1)

    disk2 = DiskItem("/dev/sdb")
    disk2.addPartition("/dev/sdb1",{"size":"10GB"})
    disk2.addPartition("/dev/sdb2",{"size":"50GB"})
    disk2.addPartition("/dev/sdb3",{"size":"10GB"})
    diskList.addDisk(disk2)

    diskList.show()
    sys.exit(app.exec_())


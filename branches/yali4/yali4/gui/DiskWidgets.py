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

import parted
import yali4.storage
import yali4.filesystem as filesystem
import yali4.partitionrequest as request
import yali4.partitiontype as parttype
import yali4.parteddata as parteddata

import yali4.gui.context as ctx
from yali4.gui.Ui.partedit import Ui_PartEdit
from yali4.gui.GUIException import *

partitonTypes = {0:None,
                 1:parttype.root,
                 2:parttype.home,
                 3:parttype.swap,
                 4:None}

class DiskList(QtGui.QWidget):

    def __init__(self, partEdit, *args):
        QtGui.QWidget.__init__(self,None)
        self.resize(QSize(QRect(0,0,600,80).size()).expandedTo(self.minimumSizeHint()))
        self.setAutoFillBackground(False)
        self.diskCount = 1
        self.partEdit = partEdit
        self.setStyleSheet("""
            QTabWidget::pane { border-radius: 4px;
                               border: 2px solid #FFFFFF; }
            QTabWidget::tab-bar { left: 5px; }
            QTabBar::tab { background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                       stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                                       stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
                           border: 2px solid #C4C4C3;
                           border-bottom-color: #FFFFFF;
                           border-top-left-radius: 4px;
                           border-top-right-radius: 4px;
                           min-width: 8ex;
                           padding: 2px;
                           padding-left:4px;
                           padding-right:4px;}
            QTabBar::tab:selected,
            QTabBar::tab:hover { background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                             stop: 0 #fafafa, stop: 0.4 #f4f4f4,
                                                             stop: 0.5 #e7e7e7, stop: 1.0 #fafafa); }
            QTabBar::tab:selected { border-color: #FFFFFF; border-bottom-color: #FFFFFF; }
            QTabBar::tab:!selected { margin-top: 2px; }
            QRadioButton::indicator { width:1px;height:1px;border-color:white; }
            QRadioButton:checked { border:3px solid #777;border-radius:4px; }
            QSplitter::handle { background-color:white; }
        """)
        self.vbox = QtGui.QVBoxLayout(self)

        self.toolBox = QtGui.QTabWidget(self)
        self.toolBox.setAutoFillBackground(False)
        self.toolBox.setFocusPolicy(Qt.NoFocus)

        self.partEdit = PartEdit()
        self.vbox.addWidget(self.toolBox)
        self.vbox.addWidget(self.partEdit)

        self.connect(self.toolBox,QtCore.SIGNAL("currentChanged(QWidget*)"),self.updatePartEdit)
        self.connect(self.partEdit.ui.formatType,QtCore.SIGNAL("currentIndexChanged(int)"),self.formatTypeChanged)
        self.connect(self.partEdit.ui.deletePartition,QtCore.SIGNAL("clicked()"),self.slotDeletePart)
        self.connect(self.partEdit.ui.applyTheChanges,QtCore.SIGNAL("clicked()"),self.slotApplyPartitionChanges)
        self.connect(self.partEdit.ui.resetAllChanges,QtCore.SIGNAL("clicked()"),self.resetChanges)
        self.initDevices()

    ##
    # GUI Operations
    #
    def updatePartEdit(self, dw):
        dw.updatePartEdit()

    def addDisk(self,dw):
        self.toolBox.addTab(dw,dw.name)
        self.toolBox.setTabToolTip(self.toolBox.count()-1,"%s - %s" % (dw.model,dw.name))
        self.diskCount+=1

    def update(self):
        _cur = self.toolBox.currentIndex()
        if _cur==-1: _cur = 0
        self.toolBox.clear()
        self.diskCount = 1

        for dev in self.devs:
            ctx.debugger.log("Device Found %s" % dev.getModel())
            self.addDevice(dev)

        self.toolBox.setCurrentIndex(_cur)
        self.updatePartEdit(self.toolBox.widget(_cur))
        self.checkRootPartRequest()

    def checkRootPartRequest(self):
        ctx.mainScreen.disableNext()

        for req in ctx.partrequests:
            if req.partitionType() == parttype.root:
                # root partition type. can enable next
                ctx.mainScreen.enableNext()

    def formatTypeChanged(self, cur):
        # index 1 is Pardus' root partition..
        if cur == 1:
            if self.partEdit.ui.partitionSize.maximum() < ctx.consts.min_root_size:
                self.partEdit.ui.formatType.setCurrentIndex(0)
                self.partEdit.ui.information.setText(
                        _("'Install Root' size must be larger than %s MB.") % (ctx.consts.min_root_size))
            else:
                self.partEdit.ui.partitionSize.setMinimum(ctx.consts.min_root_size)
        else:
            self.partEdit.ui.information.setText("")

    def initDevices(self):
        self.devs = []
        # initialize all storage devices
        if not yali4.storage.init_devices():
            raise GUIException, _("Can't find a storage device!")

        self.devs = [i for i in yali4.storage.devices]

    def resetChanges(self):
        yali4.storage.clear_devices()
        self.initDevices()
        ctx.partrequests.remove_all()
        self.update()

    def addDevice(self, dev):

        def sizeStr(mb):
            if mb > 1024:
                return _("%0.1f GB free") % long(round(mb/1024.0))
            else:
                return _("%d MB free") % mb

        # add the device to the list
        devstr = u"Disk %d (%s)" % (self.diskCount, dev.getName())
        freespace = dev.getFreeMB()
        if freespace:
            size_str = dev.getSizeStr() + "  (%s)" % sizeStr(freespace)
        else:
            size_str = dev.getSizeStr()

        diskItem = DiskItem("%s - %s" % (devstr,size_str),dev.getModel(),self.partEdit,dev.getTotalMB())
        diskItem.setData(dev)
        self.addDisk(diskItem)

        # add partitions on device
        for part in dev.getOrderedPartitionList():
            if part.isExtended():
                continue
            if part.getMinor() != -1:
                name = _("Partition %d") % part.getMinor()
            else:
                name = _("Free Space")
            ctx.debugger.log("Partition added with %s mb" % part.getMB())
            diskItem.addPartition(name,part)

        diskItem.updateSizes(self.toolBox.width())

    ##
    # Partition Operations
    #

    def slotDeletePart(self):
        """Creates delete request for selected partition"""
        dev = self.partEdit.currentPart.getDevice()
        dev.deletePartition(self.partEdit.currentPart)

        # check for last logical partition
        if dev.numberOfLogicalPartitions() == 0 and dev.getExtendedPartition():
            # if there is no more logical partition we also dont need the extended one ;)
            dev.deletePartition(dev.getExtendedPartition())

        ctx.partrequests.removeRequest(self.partEdit.currentPart, request.mountRequestType)
        ctx.partrequests.removeRequest(self.partEdit.currentPart, request.formatRequestType)
        ctx.partrequests.removeRequest(self.partEdit.currentPart, request.labelRequestType)
        self.update()

    def slotApplyPartitionChanges(self):
        """Creates requests for changes in selected partition"""

        t = partitonTypes[self.partEdit.ui.formatType.currentIndex()]

        if not t:
            return False

        def edit_requests(partition):
            """edit partition. just set the filesystem and flags."""
            if self.partEdit.ui.formatCheck.isChecked():
                __d = partition.getDevice()
                flags = t.parted_flags
                if (parted.PARTITION_BOOT in flags) and __d.hasBootablePartition():
                    flags = list(set(flags) - set([parted.PARTITION_BOOT]))
                partition.setPartedFlags(flags)
                partition.setFileSystemType(t.filesystem)
            try:
                ctx.partrequests.append(request.MountRequest(partition, t))
                ctx.partrequests.append(request.LabelRequest(partition, t))
                if self.partEdit.ui.formatCheck.isChecked():
                    ctx.partrequests.append(request.FormatRequest(partition, t))
                else:
                    # remove previous format requests for partition (if
                    # there are any)
                    ctx.partrequests.removeRequest(partition, request.formatRequestType)
            except request.RequestException, e:
                self.partEdit.ui.information.setText("%s" % e)
                self.partEdit.ui.information.show()
                return False
            return True

        partition = self.partEdit.currentPart

        # This is a new partition request
        if partition._parted_type == parteddata.freeSpaceType:
            device = partition.getDevice()
            type = parteddata.PARTITION_PRIMARY
            size = self.partEdit.ui.partitionSize.value()
            extendedPartition = device.getExtendedPartition()

            if device.numberOfPrimaryPartitions() == 3 and size+1==partition.getMB():
                type = parteddata.PARTITION_PRIMARY
            elif device.numberOfPrimaryPartitions() == 3 and extendedPartition == None:
                # if three primary partitions exists on disk and no more extendedPartition
                # we must create new extended one for other logical partitions
                ctx.debugger.log("There is no extended partition, Yalı will create new one")
                type = parteddata.PARTITION_EXTENDED
                p = device.addPartition(partition._partition, type, None, partition.getMB(), t.parted_flags)
                partition = device.getPartition(p.num)
                ctx.debugger.log("Yalı created new extended partition as number of %d " % p.num)
                type = parteddata.PARTITION_LOGICAL

            if extendedPartition and partition._partition.type & parteddata.PARTITION_LOGICAL:
                type = parteddata.PARTITION_LOGICAL

            p = device.addPartition(partition._partition, type, t.filesystem, size, t.parted_flags)
            device.update()
            self.update()

            partition = device.getPartition(p.num)
            if not edit_requests(partition):
                return False

class DiskItem(QtGui.QWidget):
    # storage.Device or partition.Partition
    _data = None

    def __init__(self, name, model, partEdit, totalSize):
        QtGui.QWidget.__init__(self,None)
        self.setAutoFillBackground(False)

        self.layout = QtGui.QVBoxLayout(self)

        self.diskGroup = QtGui.QGroupBox(self)
        self.diskGroup.setMinimumSize(QSize(570,100))
        self.diskGroup.setMaximumSize(QSize(2280,100))

        self.gridlayout = QtGui.QGridLayout(self.diskGroup)
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(0)

        self.splinter = QtGui.QSplitter(Qt.Horizontal,self.diskGroup)
        self.splinter.setHandleWidth(2)

        self.gridlayout.addWidget(self.splinter,0,0,1,1)

        spacerItem = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        self.layout.addItem(spacerItem)
        self.layout.addWidget(self.diskGroup)
        self.layout.addItem(spacerItem)

        self.partitions = []
        self.name = name
        self.model = model
        self.totalSize = totalSize
        self.partEdit = partEdit

    def addPartition(self,name=None,data=None):

        def color(fs_type):
            colors = {"fat32":"#18D918",
                      "hfs+" :"#C0A39E",
                      "fat16":"#00FF00",
                      "ext3" :"#7590AE",
                      "ext2" :"#9DB8D2",
                      "linux-swap(new)":"#C1665A"}
            if colors.has_key(fs_type):
                return colors[fs_type]
            return "#FFF79E"

        partition = QtGui.QRadioButton("%s\n%s" % (name,data.getSizeStr()),self.diskGroup)
        partition.setFocusPolicy(Qt.NoFocus)
        if data._parted_type == parteddata.freeSpaceType:
            partition.setStyleSheet("background-image:none;")
        else:
            partition.setStyleSheet("background-color:%s;" % color(data.getFSName()))
        partition.setToolTip(_("""<b>Path:</b> %s<br>
        <b>Size:</b> %s<br>
        <b>FileSystem:</b> %s""") % (data.getPath(),data.getSizeStr(),data.getFSName()))
        self.splinter.addWidget(partition)
        self.partitions.append({"name":name,"data":data})
        self.connect(partition,QtCore.SIGNAL("clicked()"),self.updatePartEdit)

    def updatePartEdit(self):
        i=0
        for part in self.partitions:
            if self.splinter.widget(i).isChecked():
                self.partEdit.ui.deviceGroup.setTitle(part["name"])
                self.partEdit.currentPart = part["data"]
                self.partEdit.updateContent()
            i+=1

    def setData(self, d):
        self._data = d

    def getData(self):
        return self._data

    def updateSizes(self,toolBoxWidth):
        i=0
        for part in self.partitions:
            _h = self.splinter.handle(i)
            _h.setEnabled(False)
            self.splinter.setCollapsible(i,False)

            _size = self.sizePix(part['data'].getMB(),toolBoxWidth)
            _widget = self.splinter.widget(i)
            _widget.resize(_size,70)
            if _size <= 8:
                _widget.setMinimumSize(QSize(_size,90))
                _widget.setMaximumSize(QSize(_size,100))
            else:
                _widget.setMaximumSize(QSize(_size,100))

            i+=1
        self.splinter.widget(0).setChecked(True)

    def sizePix(self,mb,toolBoxWidth):
        _p = (toolBoxWidth * mb) / self.totalSize
        if _p <= 8:
            return 8
        return _p

class PartEdit(QtGui.QWidget):

    currentPart = None

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_PartEdit()
        self.ui.setupUi(self)

    def updateContent(self):
        part = self.currentPart
        self.ui.deletePartition.setVisible(True)
        if part._parted_type == parteddata.freeSpaceType:
            self.ui.deletePartition.setVisible(False)
        self.ui.devicePath.setText(part.getPath())
        self.ui.fileSystem.setText(part.getFSName())
        self.ui.partitionSize.setMaximum(part.getMB()-1)
        self.ui.partitionSize.setValue(part.getMB()-1)
        self.ui.formatType.setCurrentIndex(0)
        self.ui.information.setText("")
        self.ui.partitionSize.setMinimum(0)


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
from yali4.gui.GUIAdditional import *

import yali4.raid
import yali4.partedutils
import yali4.mdutils

partitionTypes = {0:None,
                 1:parttype.root,
                 2:parttype.home,
                 3:parttype.swap,
                 4:parttype.archive,
                 5:parttype.RaidPartitionType(),
                 6:parttype.CustomPartitionType()}

class DiskList(QtGui.QWidget):

    def __init__(self, *args):
        QtGui.QWidget.__init__(self, None)
        self.resize(QSize(QRect(0,0,600,80).size()).expandedTo(self.minimumSizeHint()))
        self.setAutoFillBackground(False)
        self.diskCount = 1
        self.setStyleSheet("""
            QTabWidget::pane { border-top: 2px solid #FFFFFF; }
            QTabWidget::tab-bar { left: 5px; }
            QTabBar::tab { background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                       stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                                       stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
                           border-top: 2px solid #C4C4C3;
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
            QTabBar::tab:selected { border-color: #CCC; border-bottom-color: #FFFFFF; }
            QTabBar::tab:!selected { margin-top: 2px; }
            QRadioButton::indicator { width:1px;height:1px;border-color:white; }
            QRadioButton:checked { border:3px solid #777;border-radius:4px; }
            QSplitter::handle { background-color:white; }
        """)
        self.vbox = QtGui.QVBoxLayout(self)

        self.tabWidget = QtGui.QTabWidget(self)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setFocusPolicy(Qt.NoFocus)

        self.partEdit = PartEdit()
        self.partEdit.ui.fileSystemBox.setVisible(False)
        self.vbox.addWidget(self.tabWidget)
        self.vbox.addWidget(self.partEdit)

        self.connect(self.tabWidget,QtCore.SIGNAL("currentChanged(QWidget*)"),self.updatePartEdit)
        self.connect(self.partEdit.ui.formatType,QtCore.SIGNAL("currentIndexChanged(int)"),self.formatTypeChanged)
        self.connect(self.partEdit.ui.deletePartition,QtCore.SIGNAL("clicked()"),self.slotDeletePart)
        self.connect(self.partEdit.ui.resizePartition,QtCore.SIGNAL("clicked()"),self.slotResizePart)
        self.connect(self.partEdit.ui.applyTheChanges,QtCore.SIGNAL("clicked()"),self.slotApplyPartitionChanges)
        self.connect(self.partEdit.ui.resetAllChanges,QtCore.SIGNAL("clicked()"),self.resetChanges)
        self.connect(self.partEdit, SIGNAL("updateTheList"),self.update)

        self.initDevices()

    def resizeEvent(self,event):
        self.update()

    ##
    # GUI Operations
    #
    def updatePartEdit(self, dw):
        # dw is DiskItem object, placed in our tab widgets
        dw.updatePartEdit()

    # add the DiskItem object to tabwidget
    # and increase disk count
    def addDisk(self,dw):
        # QWidget page, QString label
        self.tabWidget.addTab(dw,dw.name)
        self.tabWidget.setTabToolTip(self.tabWidget.count()-1,"%s - %s" % (dw.model,dw.name))
        self.diskCount+=1

    # clears and refills the tabwidget with devices found in storage.devices
    def update(self):
        _cur = self.tabWidget.currentIndex()
        if _cur==-1: _cur = 0
        self.tabWidget.clear()
        print "cleared the tabwidget"
        self.diskCount = 1

        for dev in self.devs:
            try:
                ctx.debugger.log("Device Found %s" % dev.getModel())
            except:
                pass
            print "device found %s" % dev.getModel()
            # add Device objects representing block devices
            # @see storage.py global devices[] and Device class
            self.addDevice(dev)

        self.tabWidget.setCurrentIndex(_cur)
        self.updatePartEdit(self.tabWidget.widget(_cur))
        self.checkRootPartRequest()

    def checkRootPartRequest(self):
        ctx.mainScreen.disableNext()
        for req in ctx.partrequests:
            if req.partitionType() == parttype.root:
                # root partition type. can enable next
                ctx.mainScreen.enableNext()

    # sets the options for selected partition type
    # cur is the new index of combobox
    def formatTypeChanged(self, cur):

        def forceToFormat():
            self.partEdit.ui.formatCheck.setChecked(True)
            self.partEdit.ui.formatCheck.setEnabled(False)

        # index 1 is Pardus' root partition..
        if cur == 1:
            if self.partEdit.ui.partitionSize.maximum() < ctx.consts.min_root_size and not self.partEdit.isPartitionUsed:
                self.partEdit.ui.formatType.setCurrentIndex(0)
                self.partEdit.ui.information.setText(
                        _("'Install Root' size must be larger than %s MB.") % (ctx.consts.min_root_size))
            else:
                self.partEdit.ui.partitionSize.setMinimum(ctx.consts.min_root_size)
                self.partEdit.ui.partitionSlider.setMinimum(ctx.consts.min_root_size)
                forceToFormat()
        else:
            self.partEdit.ui.information.setText("")
            self.partEdit.ui.partitionSize.setMinimum(10)
            self.partEdit.ui.partitionSlider.setMinimum(10)
            self.partEdit.ui.formatCheck.setEnabled(True)

        if cur == 2:
            # if selected partition has different fs for userspace, forceToFormat
            if not self.partEdit.currentPart.getFSName() in ["ext3","reiserfs","xfs"]:
                forceToFormat()

        if cur == 3:
            forceToFormat()

        if cur == 4:
            forceToFormat()
            self.partEdit.ui.fileSystem.setVisible(False)
            self.partEdit.ui.fileSystemBox.setVisible(True)
        else:
            self.partEdit.ui.fileSystem.setVisible(True)
            self.partEdit.ui.fileSystemBox.setVisible(False)

        # if selected partition is freespace no matter what we have to format.
        if self.partEdit.currentPart.isFreespace():
            forceToFormat()

    # initialize all storage devices
    # @see storage.py
    def initDevices(self):
        self.devs = []
        if not yali4.storage.devices:
            "diskwidgets, initing devices"
            if not yali4.storage.init_devices():
                raise GUIException, _("Can't find a storage device!")

        self.devs = [i for i in yali4.storage.devices]

    def resetChanges(self):
        yali4.storage.clear_devices()
        self.initDevices()
        ctx.partrequests.remove_all()
        self.update()

    def addDevice(self, dev):
        # get the size as human readable
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

        # adding the tabwidget page is done
        # add partitions on device

        if dev.isRaid():
            pass

        for part in dev.getOrderedPartitionList():
            # we dont show extended partition
            if part.isExtended():
                continue
            if yali4.storage.isPartOfRaid("%s%d" % (dev._path, part.getMinor())):
                continue
            # if minor is -1, its freespace
            if part.getMinor() != -1:
                name = _("Partition %d") % part.getMinor()
                if part.isFileSystemReady():
                    try:
                        name = part.getFSLabel() or name
                    except:
                        pass
            else:
                print "found a freespace : ", part.getPath()
                name = _("Free Space")

            ctx.debugger.log("Partition added with %s mb" % part.getMB())
            diskItem.addPartition(name,part)

        diskItem.updateSizes(self.tabWidget.width())

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

    def slotResizePart(self):
        """ Asks for resize for selected partition """
        dev = self.partEdit.currentPart.getDevice()
        part = self.partEdit.currentPart
        resizeWidget = ResizeWidget(dev, part, self)
        resizeWidget.show()

    def slotApplyPartitionChanges(self):
        """Creates requests for changes in selected partition"""

        t = partitionTypes[self.partEdit.ui.formatType.currentIndex()]
        # file system type is available on archive partitions
        if t == parttype.archive:
            if self.partEdit.ui.fileSystemBox.currentIndex() == 1:
                t.setFileSystem("fat32")
            else:
                t.setFileSystem("ext3")

        if not t:
            return False

        def edit_requests(partition):
            """edit partition. just set the filesystem and flags."""
            if self.partEdit.ui.formatCheck.isChecked():
                disk = partition.getDevice()
                flags = t.parted_flags

                # There must be only one bootable partition on disk
                if (parted.PARTITION_BOOT in flags) and disk.hasBootablePartition():
                    flags = list(set(flags) - set([parted.PARTITION_BOOT]))
                partition.setPartedFlags(flags)
                partition.setFileSystemType(t.filesystem)
            try:
                if self.partEdit.ui.formatCheck.isChecked():
                    ctx.partrequests.append(request.FormatRequest(partition, t))
                else:
                    # remove previous format requests for partition (if there are any)
                    ctx.partrequests.removeRequest(partition, request.formatRequestType)

                ctx.partrequests.append(request.MountRequest(partition, t))
                ctx.partrequests.append(request.LabelRequest(partition, t))

            except request.RequestException, e:
                self.partEdit.ui.information.setText("%s" % e)
                self.partEdit.ui.information.show()
                return False
            return True

        # Get selected Partition and the other informations from GUI
        partition = self.partEdit.currentPart
        partitionNum = self.partEdit.currentPartNum
        device = partition.getDevice()
        size = self.partEdit.ui.partitionSize.value()

        # This is a new partition request
        if partition._parted_type & parteddata.freeSpaceType:
            type = parteddata.PARTITION_PRIMARY
            extendedPartition = device.getExtendedPartition()

            # GPT Disk tables doesnt support extended partitions
            # so we need to reach maximum limit with primary partitions
            if device._disk.type.name == "gpt":
                min_primary = 4
                if device.numberOfPrimaryPartitions() == 4:
                    QtGui.QMessageBox.information(self,
                                                _("Too many primary partition !"), 
                                                _("GPT Disk tables does not support for extended partitions.\n" \
                                                  "You need to delete one of primary partition from your disk table !"))
                    return
            else:
                min_primary = 1

            if partitionNum == 0:
                type = parteddata.PARTITION_PRIMARY
            elif device.numberOfPrimaryPartitions() >= min_primary and not extendedPartition:
                # if three primary partitions exists on disk and no more extendedPartition
                # we must create new extended one for other logical partitions
                ctx.debugger.log("There is no extended partition, Yalı will create new one")
                type = parteddata.PARTITION_EXTENDED
                p = device.addPartition(partition._partition, type, None, partition.getMB(), t.parted_flags)

                # New Fresh logical partition
                partition = device.getPartition(p.num)
                ctx.debugger.log("Yalı created new extended partition as number of %d " % p.num)
                type = parteddata.PARTITION_LOGICAL

            if extendedPartition and partition._partition.type & parteddata.PARTITION_LOGICAL:
                type = parteddata.PARTITION_LOGICAL

            # Let's create the partition
            p = device.addPartition(partition._partition, type, t.filesystem, size, t.parted_flags)

            # Get new partition meta
            partition = device.getPartition(p.num)

        # Apply edit requests
        if not edit_requests(partition):
            return False

        device.update()
        self.update()

class DiskItem(QtGui.QWidget):
    # storage.Device or partition.Partition
    _data = None

    def __init__(self, name, model, partEdit, totalSize):
        QtGui.QWidget.__init__(self,None)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_AlwaysShowToolTips)

        self.vboxlayout = QtGui.QVBoxLayout(self)
        spacerItem = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem)

        self.hboxlayout = QtGui.QHBoxLayout()
        spacerItem1 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)

        self.deleteAllPartitions = QtGui.QPushButton(_("Delete All Partitions"),self)
        self.hboxlayout.addWidget(self.deleteAllPartitions)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.diskGroup = QtGui.QGroupBox(self)
        self.diskGroup.setMinimumSize(QSize(570,100))
        self.diskGroup.setMaximumSize(QSize(2280,100))
        self.vboxlayout.addWidget(self.diskGroup)

        self.gridlayout = QtGui.QGridLayout(self.diskGroup)
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(0)

        self.splinter = QtGui.QSplitter(Qt.Horizontal,self.diskGroup)
        self.splinter.setHandleWidth(2)

        self.gridlayout.addWidget(self.splinter,0,0,1,1)

        spacerItem2 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem2)

        self.connect(self.deleteAllPartitions,QtCore.SIGNAL("clicked()"),self.deleteAll)

        # this containts dictionary type members as we fill the list
        # ex: {"name":name, "data":data} where data is Partition type object
        # @see partition.py
        self.partitions = []

        self.name = name
        self.model = model
        self.totalSize = totalSize
        self.partEdit = partEdit


    # @param data is Partition type object and 
    # @param name is (gui)label for partition like "Free Space" or "Partition /dev/hda1"
    # @see partition.py
    def addPartition(self,name=None,data=None):

        def getFSMeta(fs_type):

            metaTypes = {"fat32":{"bgcolor":"#18D918",
                                  "fgcolor":"#000000",
                                  "icon"   :"windows"},
                         "ntfs" :{"bgcolor":"#18D918",
                                  "fgcolor":"#000000",
                                  "icon"   :"windows"},
                         "hfs+" :{"bgcolor":"#C0A39E",
                                  "fgcolor":"#000000",
                                  "icon"   :"other"},
                         "fat16":{"bgcolor":"#00FF00",
                                  "fgcolor":"#000000",
                                  "icon"   :"windows"},
                         "ext3" :{"bgcolor":"#7590AE",
                                  "fgcolor":"#FFFFFF",
                                  "icon"   :"linux"},
                         "ext2" :{"bgcolor":"#9DB8D2",
                                  "fgcolor":"#FFFFFF",
                                  "icon"   :"linux"},
                    "linux-swap":{"bgcolor":"#C1665A",
                                  "fgcolor":"#FFFFFF",
                                  "icon"   :"linux"},
                 "software raid":{"bgcolor":"#000000",
                                  "fgcolor":"#999999",
                                  "icon"   :"other"}}
            if metaTypes.has_key(fs_type):
                return metaTypes[fs_type]

            return {"bgcolor":"#FFF79E",
                    "fgcolor":"#000000",
                    "icon"   :"other"}
        
        # Get Partition Info
        partitionType = getPartitionType(data)
        
        _name = ''
        _mpoint = ''
        if partitionType:
            if partitionType == partitionTypes[1]:
                _name += "\n" + _("Pardus will install here")
                _mpoint= "[ / ]"
            elif partitionType == partitionTypes[2]:
                _name += "\n" + _("User files will store here")
                _mpoint= "[ /home ]"
            elif partitionType == partitionTypes[3]:
                _name += "\n" + _("Swap will be here")
                _mpoint= "[ swap ]"
            elif partitionType == partitionTypes[4]:
                _name += "\n" + _("Backup or archive files will store here")
                _mpoint= "[ /mnt/archive ]"
            elif partitionType == partitionTypes[5]:
                _name += "\n" + _("A Software Raid Partition")
                _mpoint= ""

        # Create partition
        partition = QtGui.QRadioButton("%s%s\n%s %s" % (name, _name, data.getSizeStr(), _mpoint), self.diskGroup)

        # Modify partition
        partition.setFocusPolicy(Qt.NoFocus)

        if data._parted_type == parteddata.freeSpaceType:
            partition.setStyleSheet("background-image:none;")
        else:
            meta = getFSMeta(data.getFSName())
            if partitionType:
                icon = "parduspart"
            else:
                icon = meta["icon"]
            partition.setIcon(QtGui.QIcon(":/gui/pics/%s.png" % icon))
            partition.setIconSize(QSize(32,32))
            partition.setStyleSheet("background-color:%s;color:%s" % (meta["bgcolor"],meta["fgcolor"]))

        partition.setToolTip(_("""<b>Path:</b> %s<br>
        <b>Size:</b> %s<br>
        <b>FileSystem:</b> %s%s""") % (data.getPath(),data.getSizeStr(),data.getFSName(),_name.replace("\n","<br>")))

        # Add it to the disk
        self.splinter.addWidget(partition)
        self.partitions.append({"name":name,"data":data})
        self.connect(partition,QtCore.SIGNAL("clicked()"),self.updatePartEdit)

    # updates partEdit's content due to checked partition
    def updatePartEdit(self):
        i=0
        # partitions : {"name":name, "data":data}
        for part in self.partitions:
            if self.splinter.widget(i).isChecked():
                self.partEdit.ui.deviceGroup.setTitle(part["name"])
                self.partEdit.currentPart = part["data"]
                self.partEdit.currentPartNum = i
                self.partEdit.updateContent()
            i+=1

    def deleteAll(self):
        for p in self._data.getPartitions():
            ctx.partrequests.removeRequest(p, request.mountRequestType)
            ctx.partrequests.removeRequest(p, request.formatRequestType)
            ctx.partrequests.removeRequest(p, request.labelRequestType)
        self._data.deleteAllPartitions()
        QObject.emit(self.partEdit,SIGNAL("updateTheList"))

    def setData(self, d):
        self._data = d

    def getData(self):
        return self._data

    def updateSizes(self,tabWidgetWidth):
        i=0
        for part in self.partitions:
            _h = self.splinter.handle(i)
            _h.setEnabled(False)
            self.splinter.setCollapsible(i,False)

            _size = self.sizePix(part['data'].getMB(),tabWidgetWidth)

            _widget = self.splinter.widget(i)
            _widget.resize(_size,70)
            if _size <= 8:
                _widget.setMinimumSize(QSize(_size,90))
                _widget.setMaximumSize(QSize(_size,100))
            else:
                _widget.setMaximumSize(QSize(_size,100))

            i+=1
        #self.splinter.widget(0).setChecked(True)

    def sizePix(self,mb,tabWidgetWidth):
        _p = (tabWidgetWidth * mb) / self.totalSize
        if _p <= 8:
            return 8
        return _p

    def slotLvm(self):
        pass

    def slotRaid(self):
        pass


# part is Partition type object, and rt is request type
def getPartitionType(part,rt=1):
    """ Get partition type from request list """
    # pt are objects derived from PartitionType class
    # like RootPartitionType or SwapPartitionType objects
    # @see partitiontype.py
    for pt in partitionTypes.values():
        # We use MountRequest type for search keyword
        # which is 1, defined in partitionrequest.py
        req = ctx.partrequests.searchPartTypeAndReqType(pt, rt)
        if req:
            if req.partition() == part:
                return pt
    return None

class PartEdit(QtGui.QWidget):

    currentPart = None
    currentPartNum = 0
    isPartitionUsed = False

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_PartEdit()
        self.ui.setupUi(self)

    def updateContent(self):
        part = self.currentPart
        self.ui.deletePartition.setVisible(True)
        self.ui.resizePartition.setVisible(True)
        self.ui.formatType.setCurrentIndex(0)
        self.ui.formatCheck.setChecked(False)

        self.ui.resizePartition.setVisible(part.isResizable())
        if part._parted_type == parteddata.freeSpaceType:
            self.ui.deletePartition.setVisible(False)
            self.ui.resizePartition.setVisible(False)
            self.ui.partitionSize.setEnabled(True)
            self.ui.partitionSlider.setEnabled(True)
        elif part._parted_type == parteddata.raidPartitionType:
            self.ui.formatType.setCurrentIndex(5)
            self.ui.formatType.setEnabled(False)
            self.ui.formatCheck.setChecked(True)
            self.ui.formatCheck.setEnabled(False)
        else:
            self.ui.partitionSize.setEnabled(False)
            self.ui.partitionSlider.setEnabled(False)

        self.ui.devicePath.setText(part.getPath())
        self.ui.fileSystem.setText(part.getFSName())
        self.ui.partitionSize.setMaximum(part.getMB()-1)
        self.ui.partitionSlider.setMaximum(part.getMB()-1)
        self.ui.partitionSize.setValue(part.getMB()-1)
        self.ui.information.setText("")
        self.ui.partitionSize.setMinimum(10)
        self.ui.partitionSlider.setMinimum(10)

        # We must select formatType after GUI update
        partitionType = getPartitionType(part)
        if partitionType:
            self.isPartitionUsed = True
            for i,j in partitionTypes.items():
                if j == partitionType:
                    self.ui.formatType.setCurrentIndex(i)
        else:
            self.isPartitionUsed = False

        isFormatChecked = getPartitionType(part,0)
        if isFormatChecked:
            self.ui.formatCheck.setChecked(True)


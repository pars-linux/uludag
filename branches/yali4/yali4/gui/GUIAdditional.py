# -*- coding: utf-8 -*-
#
# Copyright (C) 2008, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

from PyQt4 import QtGui
from PyQt4.QtCore import *

import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

import yali4.gui.context as ctx
from yali4.postinstall import *
from yali4.exception import *
from yali4.gui.Ui.partresize import Ui_PartResizeWidget
from yali4.gui.Ui.lvmedit import Ui_LvmEdit
from yali4.gui.Ui.lvmwidget import Ui_LvmWidget
from yali4.gui.Ui.autopartquestion import Ui_autoPartQuestion
from yali4.gui.Ui.connectionlist import Ui_connectionWidget
from yali4.gui.YaliDialog import Dialog
import yali4.lvmutils as lvmutils
import yali4.lvm as lvm

class LvmWidget(QtGui.QWidget):
    def __init__(self, rootWidget, parts, parttypes):
        QtGui.QWidget.__init__(self, ctx.mainScreen)
        self.ui = Ui_LvmWidget()
        self.ui.setupUi(self)
        self.rootWidget = rootWidget
        self.setStyleSheet("""

                QGroupBox#groupBox {
                    background-image: url(:/gui/pics/transBlack.png);
                    border: 1px solid #BBB;
                    border-radius:8px;
                }
                
                QGridLayout#grid1 {
                    background-image: url(:/gui/pics/transBlack.png);
                    border: 1px solid #BBB;
                    border-radius:8px;
                }

                QGridLayout#grid2 {
                    background-image: url(:/gui/pics/transBlack.png);
                    border: 1px solid #BBB;
                    border-radius:8px;
                }

                QWidget#LvmWidget {
                
                    background-image: url(:/gui/pics/trans.png);
                }
        """)
        
        self.resize(ctx.mainScreen.size())
        
        self.totalSize = 0
        self.freeSize = 0
        self.usedSize = 0
        
        self.partitionTypes = parttypes
        self.physicalVolumes = parts
        self.fillPVS(parts)
        self.fillpeSizeList(64)
        
        #self.connect(self.ui.vgName, SIGNAL("textChanged(const QString &)"),self.slotTextChanged)
        #self.connect(self.ui.pvs, SIGNAL("itemClicked (QListWidgetItem * item)"), self.slotUpdateSizes)
        self.connect(self.ui.addButton, SIGNAL("clicked()"), self.addLogicalVolume)
        self.connect(self.ui.editButton, SIGNAL("clicked()"), self.editLogicalVolume)
        self.connect(self.ui.deleteButton, SIGNAL("clicked()"), self.deleteLogicalVolume)
        self.connect(self.ui.cancelButton, SIGNAL("clicked()"), self.hide)
        
    def lvs(self):
        return [d for d in lvm.pending_lvm if isinstance(d, LogicalVolume) ]
    
    def vgs(self):
        return [d for d in lvm.pending_lvm if isinstance(d, VolumeGroup) ]

    def pvs(self):
        return [d for d in lvm.pending_lvm if isinstance(d, PhysicalVolume) ]
    
    def activePVS(self):
        lvm.pending_lvm.extend(lvm.PhysicalVolume(self.ui.pvs.item(i)._part) for i in range(self.ui.pvs.count()) if self.ui.pvs.item(i).checkState() == Qt.Checked)    
    
    def fillPVS(self, parts):
        for part in parts:
            #self.pvs.append(PhysicalVolume(part))
            item = QtGui.QListWidgetItem(self.ui.pvs)
            check = PVItem(self.ui.pvs, part)
            self.ui.pvs.setItemWidget(item, check)
            self.connect(check, SIGNAL("clicked()"), self.slotUpdateSizes)
            self.totalSize += part.getMB()
            print "totalSize %d" % self.totalSize
        self.ui.totalSpace.setText("<center>%d</center>" % self.totalSize)
    
    def fillpeSizeList(self, max):
        for i in range(4, max):
            if not i % 4:
                self.ui.peSize.addItem("%d" % i)
        
    def slotTextChanged(self):
        vg = lvmutils.safeLvmName(self.ui.vgName.text())

    def slotUpdateSizes(self):
        print "slotUpdateSizes"
        pvs = self.ui.pvs
        self.totalSize = 0
        for i in range(pvs.count()):
            item = pvs.itemWidget(pvs.item(i))
            if item.isChecked():
                self.totalSize += item._part.getSize()
            self.ui.totalSpace.setText("<center>%d</center>" % self.totalSize)
            
    def addLogicalVolume(self):
        lvmedit = LvmEditWidget(self, self.totalSize, self.partitionTypes,)
        lvmwin = Dialog(_('LVM Edit'), lvmedit, self)
        lvmwin.exec_()
        
        if self.ui.vgName.text():
            vg = lvmutils.safeLvmName(self.ui.vgName.text())
    
    def editLogicalVolume(self):
        pass
    def deleteLogicalVolume(self):
        pass
    
    def showError(self, message):
        self.ui.lvm_error.setText("<center>%s</center>" % message)
        self.ui.lvm_error.setVisible(True)
        self.ui.createButton.setEnabled(False)
        
class LvmEditWidget(QtGui.QWidget):

    def __init__(self, rootWidget, maxsize, partitionTypes):
        QtGui.QWidget.__init__(self, ctx.mainScreen)
        self.ui = Ui_LvmEdit()
        self.ui.setupUi(self)
        self.rootWidget = rootWidget
        
        self.resize(ctx.mainScreen.size())
        self.ui.partitionSlider.setMinimum(10)
        self.ui.partitionSlider.setMaximum(maxsize)
        
        self.connect(self.ui.cancelButton, SIGNAL("clicked()"), self.hide)
        
class PVItem(QtGui.QCheckBox):
    def __init__(self, parent, part):
        text = u"%s" % part.getPath()
        QtGui.QCheckBox.__init__(self, text)
        self.setChecked(True)
        self._part = part

class ResizeWidget(QtGui.QWidget):

    def __init__(self, dev, part, rootWidget):
        QtGui.QWidget.__init__(self, ctx.mainScreen)
        self.ui = Ui_PartResizeWidget()
        self.ui.setupUi(self)
        self.rootWidget = rootWidget
        self.setStyleSheet("""
                 QSlider::groove:horizontal {
                     border: 1px solid #999999;
                     height: 12px;
                     background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);
                     margin: 2px 0;
                 }

                 QSlider::handle:horizontal {
                     background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
                     border: 1px solid #5c5c5c;
                     width: 18px;
                     margin: 0 0;
                     border-radius: 2px;
                 }

                QFrame#mainFrame {
                    background-image: url(:/gui/pics/transBlack.png);
                    border: 1px solid #BBB;
                    border-radius:8px;
                }

                QWidget#PartResizeWidget {
                    background-image: url(:/gui/pics/trans.png);
                }
        """)

        self.resize(ctx.mainScreen.size())
        self.dev = dev
        self.part = part
        minSize = self.part.getMinResizeMB()

        if minSize == 0:
            self.ui.resizeMB.setVisible(False)
            self.ui.resizeMBSlider.setVisible(False)
            self.ui.resizeButton.setVisible(False)
            self.ui.label.setText(_("""<p><span style="color:#FFF"><b>It seems this partition is not ready for resizing.</b></span></p>"""))
        else:
            maxSize = self.part.getMB()
            self.ui.resizeMB.setMaximum(maxSize)
            self.ui.resizeMBSlider.setMaximum(maxSize)
            self.ui.resizeMB.setMinimum(minSize)
            self.ui.resizeMBSlider.setMinimum(minSize)
            self.connect(self.ui.resizeButton, SIGNAL("clicked()"), self.slotResize)

        self.connect(self.ui.cancelButton, SIGNAL("clicked()"), self.hide)

    def slotResize(self):
        self.hide()
        ctx.yali.info.updateAndShow(_("Resizing to %s MB..") % (self.ui.resizeMB.value()))
        ctx.debugger.log("Resize started on partition %s " % self.part.getPath())
        QTimer.singleShot(500,self.res)

    def res(self):
        resizeTo = int(self.ui.resizeMB.value())
        try:
            self.dev.resizePartition(self.part._fsname, resizeTo,self.part)
        except FSCheckError, message:
            QtGui.QMessageBox.information(self.rootWidget, _("Filesystem Error"), unicode(message))
            return

        _sum = {"partition":self.part.getName(),
                "currentSize":self.part.getMB(),
                "resizeTo":resizeTo,
                "fs":self.part._fsname}
        ctx.partSum.append(_("Partition <b>%(partition)s - %(fs)s</b> <b>resized</b> to <b>%(resizeTo)s MB</b>, old size was <b>%(currentSize)s MB</b>") % _sum)

        self.rootWidget.update()
        ctx.yali.info.hide()

class AutoPartQuestionWidget(QtGui.QWidget):

    def __init__(self, rootWidget, partList):
        QtGui.QWidget.__init__(self, ctx.mainScreen)
        self.ui = Ui_autoPartQuestion()
        self.ui.setupUi(self)
        self.setStyleSheet("""
                QFrame#mainFrame {
                    background-image: url(:/gui/pics/transBlack.png);
                    border: 1px solid #BBB;
                    border-radius:8px;
                }
                QWidget#autoPartQuestion {
                    background-image: url(:/gui/pics/trans.png);
                }
        """)

        self.rootWidget = rootWidget

        self.connect(self.ui.bestChoice, SIGNAL("clicked()"), self.slotDisableList)
        self.connect(self.ui.cancelButton, SIGNAL("clicked()"), self.slotCancelSelected)
        self.connect(self.ui.userChoice, SIGNAL("clicked()"), self.slotEnableList)
        self.connect(self.ui.useSelectedButton, SIGNAL("clicked()"), self.slotUseSelected)

        for part in partList:
            pi = PartitionItem(self.ui.partition_list, part)

        self.ui.partition_list.setCurrentRow(0)
        self.ui.bestChoice.toggle()
        self.slotDisableList()
        self.resize(ctx.mainScreen.size())

    def slotEnableList(self):
        self.ui.partition_list.setEnabled(True)

    def slotDisableList(self):
        self.rootWidget.autoPartPartition = self.ui.partition_list.item(0).getPartition()
        self.ui.partition_list.setEnabled(False)

    def slotUseSelected(self):
        self.hide()
        if self.ui.partition_list.isEnabled():
            self.rootWidget.autoPartPartition = self.ui.partition_list.currentItem().getPartition()
        ctx.mainScreen.processEvents()
        self.rootWidget.execute_(True)

    def slotCancelSelected(self):
        self.hide()
        ctx.mainScreen.enableNext()

class PartitionItem(QtGui.QListWidgetItem):

    def __init__(self, parent, _part):
        part = _part["partition"]
        if part.isFreespace():
            label = _("Free Space")
        else:
            label = part.getFSLabel() or _("Partition %d") % part.getMinor()
        text = _("(%s) [%s] Size : %s - Free : %s" % (part.getDevice().getName(),
                                                      label,
                                                      part.getSizeStr(),
                                                      part.getSizeStr(_part["newSize"])))
        QtGui.QListWidgetItem.__init__(self, text, parent)
        self.part = _part

    def getPartition(self):
        return self.part

class DeviceItem(QtGui.QListWidgetItem):
    def __init__(self, parent, dev):
        self.text = u"%s - %s (%s)" %(dev.getModel(),
                                      dev.getName(),
                                      dev.getSizeStr())
        QtGui.QListWidgetItem.__init__(self, self.text, parent)
        self._dev = dev

    def setBootable(self):
        self.setText(_("%s (Boot Disk)" % self.text))

    def getDevice(self):
        return self._dev

class PartItem(QtGui.QListWidgetItem):
    def __init__(self, parent, partition, label, icon):
        QtGui.QListWidgetItem.__init__(self, QtGui.QIcon(":/gui/pics/%s.png" % icon), label, parent)
        self._part = partition

    def getPartition(self):
        return self._part

class ConnectionItem(QtGui.QListWidgetItem):
    def __init__(self, parent, connection, package):
        QtGui.QListWidgetItem.__init__(self, QtGui.QIcon(":/gui/pics/%s.png" % package), connection, parent)
        self._connection = [connection, package]

    def getConnection(self):
        return self._connection[0]

    def getPackage(self):
        return self._connection[1]

    def connect(self):
        connectTo(self.getPackage(), self.getConnection())

class ConnectionWidget(QtGui.QWidget):

    def __init__(self, rootWidget):
        QtGui.QWidget.__init__(self, ctx.mainScreen)
        self.ui = Ui_connectionWidget()
        self.ui.setupUi(self)
        self.setStyleSheet("""
                QFrame#mainFrame {
                    background-image: url(:/gui/pics/transBlack.png);
                    border: 1px solid #BBB;
                    border-radius:8px;
                }
                QWidget#autoPartQuestion {
                    background-image: url(:/gui/pics/trans.png);
                }
        """)

        self.rootWidget = rootWidget
        self.needsExecute = False
        self.connect(self.ui.buttonCancel, SIGNAL("clicked()"), self.hide)
        self.connect(self.ui.buttonConnect, SIGNAL("clicked()"), self.slotUseSelected)

        connections = getConnectionList()

        for package in connections.keys():
            for connection in connections[package]:
                ci = ConnectionItem(self.ui.connectionList, str(connection), package)

        self.ui.connectionList.setCurrentRow(0)
        self.resize(ctx.mainScreen.size())

    def slotUseSelected(self):
        current = self.ui.connectionList.currentItem()
        ctx.yali.info.updateAndShow(_("Connecting to network <b>%s</b> ...") % current.getConnection())

        try:
            ret = current.connect()
        except:
            ret = True
            self.rootWidget.ui.labelStatus.setText(_("Connection failed"))
            ctx.yali.info.updateAndShow(_("Connection failed"))

        if not ret:
            self.rootWidget.ui.labelStatus.setText(_("Connected"))
            ctx.yali.info.updateAndShow(_("Connected"))

        self.hide()
        ctx.mainScreen.processEvents()
        ctx.yali.info.hide()

        if self.needsExecute:
            self.rootWidget.execute_(True)

        
        
#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.

# Python Modules
import os
import sys
import time

# KDE/QT Modules
from qt import *
from kdecore import *
from kdeui import *
from kfile import *

# Widget
import kdedesigner
from mainform import mainForm

# COMAR
import comar

# FSTAB
import fstab

version = '0.1'

def AboutData():
    about_data = KAboutData('fstab-manager',
                            'Fstab Manager',
                            version,
                            'Fstab Manager Interface',
                            KAboutData.License_GPL,
                            '(C) 2006 UEKAE/TÜBİTAK',
                            None, None,
                            'gokmen@pardus.org.tr')
    about_data.addAuthor('Gökmen GÖKSEL', None, 'gokmen@pardus.org.tr')
    return about_data

def loadIcon(name, group=KIcon.Desktop, size=16):
    return KGlobal.iconLoader().loadIcon(name, group, size)

def loadIconSet(name, group=KIcon.Desktop, size=16):
    return KGlobal.iconLoader().loadIconSet(name, group, size)

def asText(anarray):
    xx=''
    for i in anarray:
        xx+=i+','
    return xx.rstrip(',')

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setCaption(i18n('Fstab Manager'))
        self.layout = QGridLayout(self)
        self.htmlPart = KHTMLPart(self)
        self.resize(500, 300)
        self.layout.addWidget(self.htmlPart.view(), 1, 1)
        if os.environ['LANG'].startswith('tr_TR'):
            self.htmlPart.openURL(KURL(locate('data', 'fstab-manager/help/tr/main_help.html')))
        else:
            self.htmlPart.openURL(KURL(locate('data', 'fstab-manager/help/en/main_help.html')))

class fstabForm(mainForm):
    def __init__(self, parent=None, name=None):
        mainForm.__init__(self, parent, name)

        self.Fstab = fstab.Fstab()
        self.blockDevices = fstab.getBlockDevices()
        self.fstabPartitions = self.getPartitionsFromFstab()
        self.prettyList={}
        self.btn_Update.setEnabled(False)
        self.frame_detail.hide()

        # Just for block devices
        self.knownFS=['ext3:Ext3',
                      'ext2:Ext2',
                      'reiserfs:ReiserFS',
                      'xfs:XFS',
                      'ntfs-3g:NTFS',
                      'vfat:Fat 16/32']

        self.fillFileSystems()
        self.list_main.header().hide()
        self.diskIcon.setPixmap(loadIcon('hdd_unmount',size=64))
        self.fillDiskList()

        # Connections
        self.connect(self.list_main, SIGNAL('selectionChanged()'), self.slotList)
        self.connect(self.btn_Update, SIGNAL('clicked()'), self.slotUpdate)
        self.connect(self.btn_autoFind, SIGNAL('clicked()'), self.fillDiskList)

    def slotList(self):
        try:
            selected=self.list_main.selectedItem()
            # I will find another way for that
            # I know it sucks
            selectedDisk = str(selected.parent().text(0)).split('\n')[0]
            selectedPartition = str(selected.text()).split('\n')[0]

            for xx in self.prettyList[selectedDisk]:
                if xx['partition_name']==selectedPartition:
                    partitionInfo = xx

            self.line_mountpoint.setText(partitionInfo['mount_point'])
            self.line_opts.setText(asText(partitionInfo['options']))
            self.label_disk.setText(selectedPartition)
            i=0
            for xx in self.knownFS:
                if xx.split(':')[0]==partitionInfo['file_system']:
                    self.combo_fs.setCurrentItem(i)
                i+=1
            self.frame_detail.show()

        except:
            self.frame_detail.hide()
            pass

    def slotAddNew(self):
        pass

    def slotUpdate(self):
        pass

    def slotDelete(self):
        pass

    def fillDiskList(self):
        self.frame_detail.hide()
        self.list_main.clear()
        for disk in self.blockDevices:
            disks = QListViewItem(self.list_main,QString(disk+'\nDisk Name'))
            disks.setMultiLinesEnabled(True)
            disks.setPixmap(0,loadIcon('Disk',size=32))
            disks.setOpen(True)
            self.prettyList[disk]=[]

            for partition in self.getPartitionsFromSys(disk):
                if self.fstabPartitions.has_key(partition[0]):
                    activePartition = self.fstabPartitions.get(partition[0])
                    pixie = loadIcon('DiskAdded',size=32)
                    check = QCheckListItem.On
                else:
                    activePartition = partition[1]
                    pixie = loadIcon('DiskNotAdded',size=32)
                    check = QCheckListItem.Off

                activePartition['partition_name']=partition[0]
                self.prettyList[disk].append(activePartition)

                partitions = QCheckListItem(disks,QString('%s\nMount Point : %s \t FileSystem Type : %s ' %
                                                  (activePartition['partition_name'],activePartition['mount_point'],activePartition['file_system'])),
                                                  QCheckListItem.CheckBox)
                partitions.setState(check)
                partitions.setMultiLinesEnabled(True)
                partitions.setPixmap(0,pixie)

    def fillFileSystems(self):
        id=0
        for fs in self.knownFS:
            self.combo_fs.insertItem(fs.split(':')[1],id)
            id+=1

    def getPartitionsFromSys(self,dev):
        return [info for info in fstab.getPartitionsOfDevice(dev)]

    def getPartitionsFromFstab(self):
        return self.Fstab.getFstabPartitions()

class Module(KCModule):
    def __init__(self, parent, name):
        KCModule.__init__(self, parent, name)
        KGlobal.locale().insertCatalogue('fstab-manager')
        KGlobal.iconLoader().addAppDir('fstab-manager')
        self.config = KConfig('fstab-manager')
        self.aboutdata = AboutData()
        widget = fstabForm(self)
        toplayout = QVBoxLayout(self, 0, KDialog.spacingHint())
        toplayout.addWidget(widget)
    def aboutData(self):
        return self.aboutdata

def create_fstab_manager(parent, name):
    global kapp
    kapp = KApplication.kApplication()
    return Module(parent, name)

def main():
    about_data = AboutData()
    KCmdLineArgs.init(sys.argv, about_data)
    if not KUniqueApplication.start():
        print i18n('Fstab Manager is already running!')
        return
    app = KUniqueApplication(True, True, True)

    win = QDialog()
    win.setCaption(i18n('Fstab Manager'))
    win.setMinimumSize(520, 420)
    win.resize(520, 420)
    win.setIcon(loadIcon('fstab_manager', size=128))
    widget = fstabForm(win)
    toplayout = QVBoxLayout(win, 0, KDialog.spacingHint())
    toplayout.addWidget(widget)

    app.setMainWidget(win)
    sys.exit(win.exec_loop())

if __name__ == '__main__':
    main()

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
from khtml import *

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
        self.list_main_items=[]
        self.frame_detail.hide()
        self.sessionLocked=True

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
        self.connect(self.btn_update, SIGNAL('clicked()'), self.slotUpdate)
        self.connect(self.btn_cancel, SIGNAL('clicked()'), self.slotCancel)
        self.connect(self.btn_help, SIGNAL('clicked()'), self.slotHelp)
        self.connect(self.btn_autoFind, SIGNAL('clicked()'), self.fillDiskList)
        self.connect(self.btn_defaultOpts, SIGNAL('clicked()'),self.getDefaultOptions)
        self.connect(self.check_allPart, SIGNAL('clicked()'), self.toggleAllPartitions)
        self.connect(self.line_opts, SIGNAL('lostFocus()'), self.saveSession)
        self.connect(self.line_mountpoint, SIGNAL('lostFocus()'), self.saveSession)
        self.connect(self.combo_fs,SIGNAL('activated(const QString&)'),self.saveSession)

    def saveSession(self,Single=False):
        if not self.sessionLocked or Single:
            selected_=self.list_main.selectedItem()
            selected =self.getDetailsOfSelected(selected_,key=True)
            self.prettyList[selected[0]][selected[1]]['mount_point']=str(self.line_mountpoint.text())
            self.prettyList[selected[0]][selected[1]]['options']=str(self.line_opts.text())
            self.prettyList[selected[0]][selected[1]]['file_system']=self.getFsName(self.combo_fs.currentText())

    def getFsName(self,fs):
        for fileSystem in self.knownFS:
            if fileSystem.split(':')[1]==fs:
                return fileSystem.split(':')[0]

    def getDefaultOptions(self):
        selected_=self.list_main.selectedItem()
        selected =self.getDetailsOfSelected(selected_,key=True)
        self.line_opts.setText(self.getDefaultOptionsFor(self.prettyList[selected[0]][selected[1]]['file_system']))
        self.saveSession(Single=True)

    def getDefaultOptionsFor(self,type):
        return self.Fstab.defaultFileSystemOptions[type]

    def getDetailsOfSelected(self,selected,key=False):
        selectedDisk = str(selected.parent().text(0)).split('\n')[0]
        selectedPartition = str(selected.text()).split('\n')[0]
        x=0
        for partition in self.prettyList[selectedDisk]:
            if partition['partition_name']==selectedPartition:
                if key:
                    return selectedDisk,x
                else:
                    return partition
            x+=1

    def slotList(self):
        try:
            selected=self.list_main.selectedItem()
            partitionInfo = self.getDetailsOfSelected(selected)

            self.line_mountpoint.setText(partitionInfo['mount_point'])
            self.line_opts.setText(partitionInfo['options'])
            self.label_disk.setText(partitionInfo['partition_name'])
            i=0
            for xx in self.knownFS:
                if xx.split(':')[0]==partitionInfo['file_system']:
                    self.combo_fs.setCurrentItem(i)
                i+=1
            if selected.isOn():
                self.btn_update.setEnabled(True)
            self.frame_detail.show()
            self.sessionLocked=False

        except:
            self.frame_detail.hide()
            self.sessionLocked=True

    def slotUpdate(self):
        for disk in self.blockDevices:
            for node in self.prettyList[disk]:
                self.Fstab.addFstabEntry(node['partition_name'],node)
        print self.Fstab.content
        self.Fstab.writeContent()
        self.__init__()

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
                partitions = QCheckListItem(disks,QString('%s\nMount Point : %s \t FileSystem Type : %s ' %
                                                  (activePartition['partition_name'],activePartition['mount_point'],activePartition['file_system'])),
                                                  QCheckListItem.CheckBox)
                partitions.setState(check)
                partitions.setMultiLinesEnabled(True)
                partitions.setPixmap(0,pixie)

                activePartition['list_widget']=partitions
                self.prettyList[disk].append(activePartition)

                self.toggleAllPartitions()

    def toggleAllPartitions(self):
        self.frame_detail.hide()
        for disk in self.prettyList:
            for item in self.prettyList[disk]:
                if item['mount_point']=='/':
                    if self.check_allPart.isOn():
                        item['list_widget'].setVisible(True)
                    else:
                        item['list_widget'].setVisible(False)

    def fillFileSystems(self):
        id=0
        for fs in self.knownFS:
            self.combo_fs.insertItem(fs.split(':')[1],id)
            id+=1

    def getPartitionsFromSys(self,dev):
        return [info for info in fstab.getPartitionsOfDevice(dev)]

    def getPartitionsFromFstab(self):
        return self.Fstab.getFstabPartitions()

    def slotHelp(self):
        self.helpwin = HelpDialog(self)
        self.helpwin.show()

    def slotCancel(self):
        sys.exit()

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

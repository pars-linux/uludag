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

        self.btn_Update.setEnabled(False)
        self.btn_Delete.setEnabled(False)

        #self.list_main.setFont( QFont( "dejavu", 10, QFont.Bold ))

        self.list_main.header().hide()
        self.list_main.setRootIsDecorated(True)
        self.list_main.setMultiSelection(False)

        self.fillDiskList()

        # Initialize Comar
        # self.comar = comar.Link()
        # self.comar.localize(os.environ['LANG'].split('_')[0])

        # Connections
        self.connect(self.list_main, SIGNAL('selectionChanged()'), self.slotList)
        self.connect(self.btn_addNew, SIGNAL('clicked()'), self.slotAddNew)
        self.connect(self.btn_Delete, SIGNAL('clicked()'), self.slotDelete)
        self.connect(self.btn_Update, SIGNAL('clicked()'), self.slotUpdate)

    def slotList(self):
        pass

    def slotAddNew(self):
        pass

    def slotUpdate(self):
        pass

    def slotDelete(self):
        pass

    def fillDiskList(self):
        count=0
        for disk in self.blockDevices:
            disks = QListViewItem(self.list_main,QString(disk))
            disks.setOpen(True)
            for partition in self.getPartitionsFromSys(disk):
                if self.fstabPartitions.has_key(partition[0]):
                    activePartition = self.fstabPartitions.get(partition[0])
                else:
                    activePartition = partition[1]
                print activePartition
                partitions = QListViewItem(self.list_main.firstChild(),
                                           QString(partition[0]),
                                           QString('Partition %d'%count),
                                           QString(activePartition['mount_point']),
                                           #QString(''),
                                           QString(activePartition['file_system']))
                count+=1

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

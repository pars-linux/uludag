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
import dbus
import grp
import subprocess
import functools

# KDE/QT Modules
from qt import *
from kdecore import *
from kdeui import *
from kfile import *
from khtml import *

# Widget
import kdedesigner
from diskform import mainForm

# COMAR
import comar

# DBus event loop
import dbus
from dbus.mainloop.qt3 import DBusQtMainLoop

version = '2.0.0'

def AboutData():
    about_data = KAboutData('disk-manager',
                            'Disk Manager',
                            version,
                            'Disk Manager Interface',
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
        self.setCaption(i18n('Disk Manager'))
        self.layout = QGridLayout(self)
        self.htmlPart = KHTMLPart(self)
        self.resize(500, 300)
        self.layout.addWidget(self.htmlPart.view(), 1, 1)
        self.lang_code = os.environ['LANG'][:5].split('_')[0].lower()
        if os.path.isdir(locate('data', 'disk-manager/help/%s/'%self.lang_code)):
            self.htmlPart.openURL(KURL(locate('data', 'disk-manager/help/%s/main_help.html'%self.lang_code)))
        else:
            self.htmlPart.openURL(KURL(locate('data', 'disk-manager/help/en/main_help.html')))

class diskForm(mainForm):
    def __init__(self, parent=None, name=None):
        mainForm.__init__(self, parent, name)

        self.link = comar.Link()

        # Connections
        """
        self.connect(self.btn_defaultOpts, SIGNAL('clicked()'),self.getDefaultOptions)
        self.connect(self.line_opts, SIGNAL('lostFocus()'), self.saveSession)
        self.connect(self.line_mountpoint, SIGNAL('lostFocus()'), self.saveSession)
        self.connect(self.combo_fs,SIGNAL('activated(const QString&)'),self.saveSession)
        self.connect(self.btn_help, SIGNAL('clicked()'), self.slotHelp)
        """
        self.connect(self.list_main, SIGNAL('selectionChanged()'), self.slotList)
        self.connect(self.combo_fs, SIGNAL('activated(const QString&)'), self.slotFS)
        self.connect(self.btn_reset, SIGNAL('clicked()'), self.slotReset)
        self.connect(self.btn_update, SIGNAL('clicked()'), self.slotUpdate)
        self.connect(self.frame_entry, SIGNAL('toggled(bool)'), self.slotToggle)

        self.list_main.header().hide()
        self.frame_detail.setEnabled(False)

        self.knownFS = [
            ('ext3', 'Extended 3'),
            ('ext2', 'Extended 2'),
            ('reiserfs', 'Reiser FS'),
            ('xfs', 'XFS'),
            ('ntfs-3g', 'NTFS'),
            ('vfat', 'Fat 16/32'),
        ]
        self.fsOptions = {
            "vfat": "quiet,shortname=mixed,dmask=007,fmask=117,utf8,gid=6",
            "ext2": "noatime",
            "ext3": "noatime",
            "ntfs-3g": "dmask=007,fmask=117,locale=tr_TR.UTF-8,gid=6",
            "reiserfs": "noatime",
            "xfs": "noatime",
        }

        for name, label in self.knownFS:
            self.combo_fs.insertItem(label)

        self.initialize()

        # Listen signals
        self.link.listenSignals("Disk.Manager", self.signalHandler)

    def getFSName(self):
        for name, label in self.knownFS:
            if label == self.combo_fs.currentText():
                return name
        return None

    def setFSName(self, fsname):
        for name, label in self.knownFS:
            if fsname == name:
                self.combo_fs.setCurrentText(label)
                return
        # Unknown FS type, add to list
        self.knownFS.append((fsname, fsname))
        self.combo_fs.insertItem(fsname)
        self.combo_fs.setCurrentText(fsname)

    def initialize(self):
        # Package
        self.package = None
        # Entry list
        self.entries = {}
        # Devices on entry list
        self.devices = []
        # Labels
        self.labels = {}
        # Items
        self.items = {}
        # Get entries
        self.link.Disk.Manager.listEntries(async=self.asyncListEntries)

    def signalHandler(self, package, signal, args):
        self.initialize()

    def asyncListEntries(self, package, exception, result):
        if not self.package:
            self.package = package
        else:
            return
        if not exception:
            for entry in result[0]:
                device = self.getRealDevice(entry)
                self.entries[device] = self.link.Disk.Manager[self.package].getEntry(entry)
            # Get devices
            self.link.Disk.Manager[self.package].getDevices(async=self.asyncGetDevices)

    def asyncGetDevices(self, package, exception, result):
        if not exception:
            self.list_main.clear()
            for device in result[0]:
                disk = QListViewItem(self.list_main, device)
                disk.setMultiLinesEnabled(True)
                disk.setPixmap(0,loadIcon('Disk', size=32))
                disk.setOpen(True)
                disk.setVisible(False)
                # Get parts
                self.link.Disk.Manager[package].getDeviceParts(device, async=functools.partial(self.asyncGetPartitions, disk))

    def asyncGetPartitions(self, listItem, package, exception, result):
        if not exception:
            for part in result[0]:
                if part in self.entries:
                    label = "%s\n%s" % (part, self.getEntryInfo(part))
                    pixie = loadIcon('DiskAdded', size=32)
                else:
                    label = "%s\n%s" % (part, "")
                    pixie = loadIcon('DiskNotAdded', size=32)
                listItem.setVisible(True)
                disk_part = QListViewItem(listItem, label)
                disk_part.setMultiLinesEnabled(True)
                disk_part.setPixmap(0, pixie)
                self.items[disk_part] = part

    def getEntryInfo(self, device):
        info = self.entries[device]
        return "%s" % (info[0])

    def getDeviceByLabel(self, label):
        return self.link.Disk.Manager[self.package].getDeviceByLabel(label)

    def getRealDevice(self, device):
        if device.startswith("LABEL="):
            label = device.split("=", 1)[1]
            device = self.getDeviceByLabel(label)
            self.labels[device] = label
            return device
        return device

    def slotToggle(self, checked):
        if checked:
            self.slotFS()

    def slotFS(self, text=""):
        fsType = self.getFSName()
        options = self.fsOptions[fsType]
        self.line_opts.setText(options)

    def slotList(self):
        item = self.list_main.selectedItem()
        if item not in self.items:
            self.frame_detail.setEnabled(False)
            return
        device = str(self.items[item])
        if device not in self.entries:
            self.line_mountpoint.setText("")
            self.line_opts.setText("")
            self.combo_fs.setCurrentText(self.knownFS[0][1])
            self.frame_entry.setChecked(False)
        else:
            options = []
            for key, value in self.entries[device][2].iteritems():
                if value:
                    options.append("%s=%s" % (key, value))
                else:
                    options.append(key)
            self.line_mountpoint.setText(self.entries[device][0])
            self.line_opts.setText(",".join(options))
            self.setFSName(self.entries[device][1])
            self.frame_entry.setChecked(True)
        self.frame_detail.setEnabled(True)

    def slotUpdate(self):
        item = self.list_main.selectedItem()
        if item not in self.items:
            self.frame_detail.setEnabled(False)
            return
        device = str(self.items[item])
        if device in self.labels:
            device = "LABEL=%s" % self.labels[device]
        if self.frame_entry.isChecked():
            # Path
            path = str(self.line_mountpoint.text())
            # FS type
            fsType = str(self.getFSName())
            # Options
            options = {}
            for opt in str(self.line_opts.text()).split(","):
                if "=" in opt:
                    key, value = opt.split("=", 1)
                    options[key] = value
                else:
                    options[opt] = ""
            try:
                self.link.Disk.Manager[self.package].addEntry(device, path, fsType, options)
            except dbus.DBusException, e:
                KMessageBox.sorry(self, unicode(e.message))
        else:
            self.link.Disk.Manager[self.package].removeEntry(device)

    def slotReset(self):
        name = self.getFSName()
        if name in self.fsOptions:
            self.line_opts.setText(self.fsOptions[name])
        else:
            self.line_opts.setText("")

    def slotHelp(self):
        self.helpwin = HelpDialog(self)
        self.helpwin.show()

    def slotQuit(self):
        self.combo_fs.clear()
        # self.frame_detail.hide()


class Module(KCModule):
    def __init__(self, parent, name):
        KCModule.__init__(self, parent, name)
        KGlobal.locale().insertCatalogue('disk-manager')
        KGlobal.iconLoader().addAppDir('disk-manager')
        self.config = KConfig('disk-manager')
        self.aboutdata = AboutData()
        widget = diskForm(self)
        toplayout = QVBoxLayout(self, 0, KDialog.spacingHint())
        toplayout.addWidget(widget)

    def aboutData(self):
        return self.aboutdata

def create_disk_manager(parent, name):
    global kapp
    kapp = KApplication.kApplication()
    if not dbus.get_default_main_loop():
        DBusQtMainLoop(set_as_default=True)
    return Module(parent, name)

def main():
    about_data = AboutData()
    KCmdLineArgs.init(sys.argv, about_data)
    if not KUniqueApplication.start():
        print i18n('Disk Manager is already running!')
        return
    app = KUniqueApplication(True, True, True)


    DBusQtMainLoop(set_as_default=True)

    win = QDialog()
    win.setCaption(i18n('Disk Manager'))
    win.setIcon(loadIcon('disk_manager', size=128))
    widget = diskForm(win)
    toplayout = QVBoxLayout(win, 0, KDialog.spacingHint())
    toplayout.addWidget(widget)

    app.setMainWidget(win)
    app.connect(app, SIGNAL("lastWindowClosed()"), widget.slotQuit)

    sys.exit(win.exec_loop())

if __name__ == '__main__':
    main()

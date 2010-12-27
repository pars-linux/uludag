#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.

# Python Modules
import os
import sys
import dbus
import functools
import string
import parted

# KDE/QT Modules
from qt import *
from kdeui import *
from kfile import *
from khtml import *
from kdecore import *

# Widget
from diskform import mainForm

# COMAR
import comar

# DBus event loop
from dbus.mainloop.qt3 import DBusQtMainLoop

version = '2.1.2'

"""
A util list for HAL. It is used for storing volume device changes.
Plugging and removing volumes effects it.
"""
deviceList = {}

# HAL related variables.
# These are used for configuring communication with 'hald'.
serviceName = 'org.freedesktop.Hal'
interfaceName =  '/org/freedesktop/Hal/Manager'
managerName = 'org.freedesktop.Hal.Manager'
deviceManagerName = 'org.freedesktop.Hal.Device'

"""
diskForm pointer. This is set in main function and used in
hal daemon communication functions (such as deviceAdded function).
"""
dmWidget = None 

def AboutData():
    about_data = KAboutData('disk-manager',
                            'Disk Manager',
                            version,
                            'Disk Manager Interface',
                            KAboutData.License_GPL,
                            '(C) 2006-2010 UEKAE/TÜBİTAK',
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
        self.connect(self.list_main, SIGNAL('selectionChanged()'), self.slotList)
        self.connect(self.combo_fs, SIGNAL('activated(const QString&)'), self.slotFS)
        self.connect(self.btn_reset, SIGNAL('clicked()'), self.slotReset)
        self.connect(self.btn_update, SIGNAL('clicked()'), self.slotUpdate)
        self.connect(self.btn_mount, SIGNAL('clicked()'), self.slotMount)
        self.connect(self.frame_entry, SIGNAL('toggled(bool)'), self.slotToggle)

        self.list_main.header().hide()
        self.frame_detail.setEnabled(False)
        self.frame_detail.hide()

        self.knownFS = [
            ('ext4', 'ext4'),
            ('ext3', 'ext3'),
            ('ext2', 'ext2'),
            ('reiserfs', 'Reiser FS'),
            ('xfs', 'XFS'),
            ('ntfs-3g', 'NTFS'),
            ('vfat', 'Fat 16/32'),
        ]

        self.fsOptions = {
            "vfat"      : "quiet,shortname=mixed,dmask=007,fmask=117,utf8,gid=6",
            "ext2"      : "noatime",
            "ext3"      : "noatime",
            "ext4"      : "noatime",
            "ntfs-3g"   : "dmask=007,fmask=117,locale=tr_TR.UTF-8,gid=6",
            "reiserfs"  : "noatime",
            "xfs"       : "noatime",
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
        # Items
        self.items = {}
        # Get entries
        self.link.Disk.Manager.listEntries(async=self.asyncListEntries)


    def signalHandler(self, package, signal, args):
        self.initialize()
        self.frame_detail.setEnabled(False)
        self.frame_detail.hide()

    def asyncUmount(self, device, package, exception, result):
        """
        Asynchronous umount function displays if any error occurs.
        """
        if not exception:
            self.initialize()
            self.frame_detail.setEnabled(False)
            self.frame_detail.hide()
        else:
            if unicode(exception.message).startswith("tr.org.pardus.comar"):
                self.btn_mount.setEnabled(True)
            else:
                KMessageBox.sorry(self, unicode(exception.message))

    def asyncMount(self, device, path, package, exception, result):
        """
        Asynchronous mount function displays if any error occurs.
        """
        if not exception:
            self.initialize()
            self.frame_detail.setEnabled(False)
            self.frame_detail.hide()
        else:
            if unicode(exception.message).startswith("tr.org.pardus.comar"):
                self.btn_mount.setEnabled(True)
            else:
                KMessageBox.sorry(self, unicode(exception.message))

    def asyncListEntries(self, package, exception, result):
        if not self.package:
            self.package = package
        else:
            return
        if not exception:
            for device in result[0]:
                self.entries[device] = self.link.Disk.Manager[self.package].getEntry(device)
            # Get devices
            self.link.Disk.Manager[self.package].getDevices(async=self.asyncGetDevices)

    def getDeviceByLabel(self, label):
        return self.link.Disk.Manager[self.package].getDeviceByLabel(label)

    def humanReadableSize(self, size, precision=".1"):
        symbols, depth = [' B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'], 0
        while size > 1000 and depth < 8:
            size = float(size / 1024)
            depth += 1
        if size == 0:
            return "0 B"
        fmt = "%%%sf %%s" % precision
        return fmt % (size, symbols[depth])

    def asyncGetDevices(self, package, exception, result):
        if not exception:
            self.list_main.clear()
            for device in result[0]:
                try:
                    dsk = parted.Disk(parted.Device(device))
                except:
                    pass #no medium found
                model = dsk.device.model
                size = self.humanReadableSize(dsk.device.getSize(unit="B"))
                label = "%s  (%s)\n%s" % (device, size, model)
                disk = QListViewItem(self.list_main, label)
                disk.setMultiLinesEnabled(True)
                disk.setPixmap(0,loadIcon('mounted', size=32))
                disk.setOpen(True)
                disk.setVisible(False)
                # Get parts
                self.link.Disk.Manager[package].getDeviceParts(device, async=functools.partial(self.asyncGetPartitions, disk))

    def asyncGetPartitions(self, listItem, package, exception, result):
        if not exception:
            for part in result[0]:
                if part in self.entries:
                    info = self.getEntryInfo(part)
                    dsk = parted.Disk(parted.Device(part.rstrip(string.digits)))
                    sda1 = dsk.getPartitionByPath(part)
                    size = self.humanReadableSize(sda1.getSize(unit="B"))
                    label = "%s (%s)\n%s" % (part, size, info)
                else:
                    dsk = parted.Disk(parted.Device(part.rstrip(string.digits)))
                    info = self.getFSType(part).upper()
                    label = "%s\n%s" % (part, info)
                if self.link.Disk.Manager[self.package].isMounted(part):
                    pixie = loadIcon('mounted', size=32)
                else:
                    pixie = loadIcon('notmounted', size=32)
                listItem.setVisible(True)
                disk_part = QListViewItem(listItem, label)
                disk_part.setMultiLinesEnabled(True)
                disk_part.setPixmap(0, pixie)
                self.items[disk_part] = part

    def getEntryInfo(self, device):
        info = self.entries[device]
        return "%s" % (info[0])

    def slotToggle(self, checked):
        if checked:
            self.slotFS()

    def slotFS(self, text=""):
        fsType = self.getFSName()
        options = self.fsOptions.get(fsType, "defaults")
        self.line_opts.setText(options)

    def getFSType(self, part):
        return self.link.Disk.Manager[self.package].getFSType(part)

    def slotMount(self):
        """
        Triggered when mount/umount button clicked. If the selected 
        partition is not mounted this function calls mount function 
        otherwise calls umount function.
        """
        item = self.list_main.selectedItem()
        device = str(self.items[item])
        try:
            if not self.link.Disk.Manager[self.package].isMounted(device):
                self.link.Disk.Manager.mount(device, '', async=functools.partial(self.asyncMount, device, ''))
            else:
                self.link.Disk.Manager.umount(device, async=functools.partial(self.asyncUmount, device))
        except Exception, e:
            if e.message.startswith("tr.org.pardus.comar"):
                pass
            else:
                KMessageBox.sorry(self, unicode(e.message))
        # This is for preventing user to push repeatedly.
        self.btn_mount.setEnabled(False)

    def slotList(self):
        item = self.list_main.selectedItem()
        if item not in self.items:
            self.frame_detail.setEnabled(False)
            self.frame_detail.hide()
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
        self.link.Disk.Manager.isMounted(device, async=functools.partial(self.asyncCheckMounted, device))

    def asyncCheckMounted(self, device, package, exception, result):
        """
        Checks partition's mount state and due to this result
        configures mount button's behaviour.
        """
        if result and not not result[0]:
            # There is a mount point for this partition so enable the 
            # mount button and set its text as 'unmount'.
            self.btn_mount.setText(i18n('Unmount'))
            self.frame_entry.setEnabled(True)
            self.frame_detail.show()
            self.btn_mount.setEnabled(True)
        else:
            # This partition is not mounted.
            fstype = self.getFSType(device)
            if fstype == 'swap' or fstype == 'LVM2_member':
                # If partition is a swap or LVM member there won't be mount option.
                self.frame_entry.setEnabled(False)
                self.frame_detail.hide()
                self.btn_mount.setEnabled(False)
            else:
                # Partition is not mounted and other than a swap.
                # Enable the mount button and set its text as 'mount'.
                self.btn_mount.setText(i18n('Mount'))
                self.frame_entry.setEnabled(True)
                self.btn_mount.setEnabled(True)
                self.frame_detail.show()


    def slotUpdate(self):
        item = self.list_main.selectedItem()
        if item not in self.items:
            self.frame_detail.setEnabled(False)
            self.frame_detail.hide()
            return
        device = str(self.items[item])
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
                # Get the mount path for related partition. This must be
                # stored before call of the addEntry function.
                mountPath = self.link.Disk.Manager[self.package].isMounted(device)
                # Try to add an entry for this partition to fstab.
                # Add entry function also mounts a partition if it is
                # not mounted.
                self.link.Disk.Manager[self.package].addEntry(device, path, fsType, options)
                # Entry added. Before saving an entry if the partition
                # mounted a point which is different from entry's path,
                # say to user that it is saved but not mounted to entry's
                # path beacause it is mounted another point.
                if not not mountPath and not mountPath == path:
                    KMessageBox.sorry(self, i18n("Changes saved but system couldn't mount it because it has been already mounted another point"))
            except dbus.DBusException, e:
                if e.message.startswith("tr.org.pardus.comar"):
                    pass
                else:
                    KMessageBox.sorry(self, unicode(e.message))
        else:
            path = str(self.line_mountpoint.text())
            if path == '/boot':
                confirm = KMessageBox.questionYesNo(self, i18n("Removing this partition from auto mount list can cause some boot problems.\nDo you want to continue?"), i18n("Warning"))
                if confirm == KMessageBox.Yes:
                    pass
                else:
                    return
            try:
                self.link.Disk.Manager[self.package].removeEntry(device)
            except Exception, e:
                if e.message.startswith("tr.org.pardus.comar"):
                    pass
                else:
                    KMessageBox.sorry(self, unicode(e.message))

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

def deviceAdded(udi):
    """
    Triggered when a device added to system by hal daemon. Adds device
    to the device list if it is a volume device and reinits disk form.
    """
    if not deviceList.has_key(udi):
        device = dbus.SystemBus().get_object(serviceName, udi)
        deviceInterface = dbus.Interface(device, deviceManagerName)
        try:
            if deviceInterface.GetProperty('info.category') == 'volume':
                deviceList[udi] = udi
                dmWidget.initialize()
                self.frame_detail.setEnabled(False)
                self.frame_detail.hide()
        except Exception, e:
            pass

def deviceRemoved(udi):
    """
    Triggered when a device removed from system by hal daemon. Deletes
    related device if it is in our device list and reinits disk form.
    """
    if deviceList.has_key(udi):
        del deviceList[udi]
        dmWidget.initialize()
        self.frame_detail.setEnabled(False)
        self.frame_detail.hide()

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

    # Set global variable for further usages.
    global dmWidget
    dmWidget = widget

    # Connect to SystemBus
    systemBus = dbus.SystemBus()
    dbusService = systemBus.get_object(serviceName, interfaceName)
    halInterface = dbus.Interface(dbusService, managerName)

    # Connect to Device{Added/Removed} signals
    systemBus.add_signal_receiver(deviceAdded, 'DeviceAdded',  managerName, serviceName, interfaceName)
    systemBus.add_signal_receiver(deviceRemoved, 'DeviceRemoved',  managerName, serviceName, interfaceName)


    # Generate Global Device List
    for device in halInterface.GetAllDevices():
        deviceList[device] = device

    app.setMainWidget(win)
    app.connect(app, SIGNAL("lastWindowClosed()"), widget.slotQuit)

    sys.exit(win.exec_loop())

if __name__ == '__main__':
    main()

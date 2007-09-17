#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import glob
import os

default_options = {
    "vfat":     ("quiet", "shortname=mixed", "dmask=007", "fmask=117", "utf8", "gid=6"),
    "ext3":     ("noatime", ),
    "ext2":     ("noatime", ),
    "ntfs-3g":  ("dmask=007", "fmask=117", "gid=6"),
    "reiserfs": ("noatime", ),
    "xfs":      ("noatime", ),
    "defaults": ("defaults", ),
}

pardus_labels = ("PARDUS_ROOT", "PARDUS_HOME", "PARDUS_SWAP")

excluded_file_systems = ("proc", "tmpfs", "sysfs", "swap", "nfs", "nfs4", "cifs")

default_mount_dir = "/mnt"

def getBlockDevices():
    """Returns a list of block devices attached to the system"""

    if not os.path.exists("/sys/block"):
        return fail("sysfs not found!")

    devices = []

    sysfs_devs = glob.glob("/sys/block/*")
    for sysfs_dev in sysfs_devs:
        if not "loop" in sysfs_dev and not "ram" in sysfs_dev:
            if not int(open(sysfs_dev + "/removable").read().strip()):
                devlink = os.readlink(sysfs_dev + "/device")
                if not "/usb" in devlink:
                    devices.append("/dev/" + os.path.basename(sysfs_dev))

    devices.sort()
    return devices

def getPartitions(device):
    """Returns all partitions and their filesystems
        of a given device but swap partition"""

    import parted

    partitions = []

    pdev = parted.PedDevice.get(device)
    try:
        disk = parted.PedDisk.new(pdev)
    except:
        disk = pdev.disk_new_fresh(parted.disk_type_get("msdos"))

    part = disk.next_partition()
    while part:
        if part.fs_type and part.fs_type.name != "linux-swap(new)":
            partitions.append( device + str(part.num) + ":" + part.fs_type.name )
        part = disk.next_partition(part)

    return partitions

def getMountedPartitions():
    ret = []
    f = open('/proc/mounts', 'r')
    try:
        for line in f:
            if line.startswith('/'):
                ret.append(line)
    finally:
        f.close()
    return ret

    return subprocess.call(cmd, stdout=f, stderr=f)

def doMount(device, mount_path=None):
    import subprocess

    efestab = Fstab()

    if mount_path == None:
        mount_path = os.path.join(default_mount_dir, os.path.basename(device))

    for line in getMountedPartitions():
        if device in line.split(' ')[0]:
            return fail("already mounted partition")
        if mount_path in line.split(' ')[1]:
            return fail("%s is already mounted to %s" % (device, mount_path))

    for i in efestab.entries:
        if i.device_node == device and i.mount_point == '/':
            return fail("trying to mount root partition")

    if not os.path.exists(mount_path):
        os.makedirs(mount_path)

    f = file('/dev/null', 'w')

    if subprocess.call(["mount", device, mount_path], stdout=f, stderr=f) != 0:
        f.close()
        return fail("error mounting")
    f.close()

def doUmount(device):
    import subprocess

    tmp = 0

    for line in getMountedPartitions():
        if device == line.split(' ')[0]:
            if line.split(' ')[1] == '/':
                return fail("trying to umount root partition")
            tmp = 1

    if tmp == 1:
        f = file('/dev/null', 'w')
        if subprocess.call(["umount", device], stdout=f, stderr=f) == 0:
            f.close()
            return None
        else:
            f.close()
            return fail("error umounting")

    return fail("not mounted")

def blockNameByLabel(label):
    path = os.path.join("/dev/disk/by-label/%s" % label)
    if os.path.islink(path):
        return "/dev/%s" % os.readlink(path)[6:]
    else:
        return None

def getLocale():
    return os.environ['LC_ALL']

class FstabEntry:
    def __init__(self, line=None):
        defaults = [ None, None, "auto", "defaults", 0, 0 ]

        args = []
        if line:
            args = line.split()

        args = args[:len(args)] + defaults[len(args):]

        self.device_node = args[0]
        self.mount_point = args[1]
        self.file_system = args[2]
        self.options = args[3]
        self.dump_freq = args[4]
        self.pass_no = args[5]

    def __str__(self):
        return "%-20s %-16s %-9s %-20s %s %s" % (
            self.device_node,
            self.mount_point,
            self.file_system,
            self.options,
            self.dump_freq,
            self.pass_no
        )

class Fstab:
    comment = """
# See the manpage fstab(5) for more information.
#
#   <fs>             <mountpoint>     <type>    <opts>               <dump/pass>\n"""

    def __init__(self, path=None):
        if not path:
            path = "/etc/fstab"
        self.path = path
        self.entries = []
        self.partitions = None
        self.labels = {}
        for line in file(path):
            if line.strip() != "" and not line.startswith('#'):
                try:
                    assert(len(line.split()) == 6)
                    self.entries.append(FstabEntry(line))
                except:
                    fail("Fstab syntax incorrect")

    def __str__(self):
        return "\n".join(map(str, self.entries))

    def scan(self):
        self.partitions = {}
        for dev in getBlockDevices():
            for part in getPartitions(dev):
                self.partitions[part.split(":")[0]] = part.split(":")[1]
        if os.path.exists("/dev/disk/by-label"):
            for label in os.listdir("/dev/disk/by-label/"):
                self.labels[blockNameByLabel(label)] = label

    def write(self, path=None):
        if not path:
            path = self.path

        for entry in self.entries:
            if not os.path.exists(entry.mount_point):
                os.makedirs(entry.mount_point)

        f = file(path, "w")
        f.write(self.comment)
        f.write("\n")
        f.write(str(self))
        f.write("\n")
        f.close()

    def removeEntry(self, device_node):
        for i, entry in enumerate(self.entries):
            if entry.device_node == device_node and entry.mount_point != "/":
                del self.entries[i]

    def addEntry(self, device_node, mount_point=None):
        if not self.partitions:
            self.scan()

        if not mount_point:
            mount_point = os.path.join(default_mount_dir, os.path.basename(device_node))

        for entry in self.entries:
            if entry.device_node == device_node:
                return None

        if device_node in self.entries:
            return None

        file_system = self.partitions.get(device_node)
        if file_system in ("fat16", "fat32"):
            file_system = "vfat"
        if file_system == "ntfs":
            file_system = "ntfs-3g"

        options = default_options.get(file_system, None)
        if not options:
            options = default_options.get("defaults")

        entry = FstabEntry()
        entry.device_node = device_node
        entry.mount_point = mount_point
        entry.file_system = file_system
        entry.options = ",".join(options)
        if file_system == "ntfs-3g":
            entry.options += ",locale=%s" % getLocale()
        self.entries.append(entry)

    def refresh(self):
        if not self.partitions:
            self.scan()

        # Carefully remove non existing partitions
        removal = []
        for i, entry in enumerate(self.entries):
            node = entry.device_node
            if entry.mount_point == "/":
                # Root partition is never removed
                continue
            if not entry.mount_point.startswith("/mnt"):
                # Only remove partitions that were added in /mnt
                continue
            elif entry.file_system in excluded_file_systems:
                # Virtual file systems are never removed
                continue
            elif node.startswith("LABEL="):
                label = node.split("=", 1)[1]
                if label in pardus_labels:
                    # Labelled Pardus system partitions are never removed
                    continue
                if not self.partitions.has_key(blockNameByLabel(label)):
                    removal.append(node)
            else:
                if not self.partitions.has_key(node):
                    removal.append(node)
        map(self.removeEntry, removal)
        # Append all other existing non-removable partitions
        mounted = set(map(lambda x: x.device_node, self.entries))
        for part in self.partitions:
            if not part in mounted:
                if part in self.labels:
                    if "LABEL=%s" % self.labels[part] in mounted:
                        continue
                self.addEntry(part)

def updateFstab():
    efestab = Fstab()
    efestab.refresh()
    efestab.write()

def addEntry(device, mount_path=None):
    efestab = Fstab()
    efestab.addEntry(device, mount_path)
    efestab.write()

def getEntry(device):
    efestab = Fstab()
    for entry in efestab.entries:
        if entry.device_node.startswith('/') and entry.device_node == device:
            return str(entry)

        elif entry.device_node.startswith("LABEL"):
            entry.device_node = blockNameByLabel(entry.device_node.split("=")[1])
            if entry.device_node and entry.device_node == device:
                return str(entry)

def delEntry(device):
    efestab = Fstab()
    efestab.removeEntry(device)
    efestab.write()


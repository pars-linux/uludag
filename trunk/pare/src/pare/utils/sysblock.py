# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

from pare.diskdevice import Disk


# all disks
disks = []
# all logical volumes
lvs = []


def _comp(x, y):
    """sort disks using getName()"""
    x = x.name
    y = y.name
    if x > y: return -1
    elif x == y: return 0
    else: return 1

##
# initialize all devices and fill devices list
def init(force = False):
    global disks

    if disks and not force:
        return True

    clear_devices()

    devs = detect_disk()
    for dev_path in devs:
        d = Disk(dev_path)
        disks.append(d)

    disks.sort(_comp,reverse=True)

    if disks:
        return True

    return False

def clearAll():
    clear_disks()
    clear_lvs()
    
def clear_disks():
    global disks
    disks = []

def clear_lvs():
    global lvs
    lvs = []

def detect_procPartitions():
    # Check for sysfs. Only works for >2.6 kernels.
    if not os.path.exists("/sys/bus"):
        raise DeviceError, "sysfs not found!"

    # Check for /proc/partitions
    if not os.path.exists("/proc/partitions"):
        raise DeviceError, "/proc/partitions not found!"

    partitions = []
    for line in open("/proc/partitions"):
        entry = line.split()

        if not entry:
            continue
        if not entry[0].isdigit() and not entry[1].isdigit():
            continue

        major = int(entry[0])
        minor = int(entry[1])
        device = "/dev/" + entry[3]

        partitions.append((major, minor, device))

    return partitions

##
# Return a list of block devices in system
def detect_disk():

    partitions = detect_procPartitions()
    
    _devices = []
    # Scan sysfs for the device types.
    #FIXME:Developer PreventeR:Added glob.glob("/sys/block/sda*") for unhandled parition table destroy test later it will erased
    #FIXME:Added glob.glob("/sys/block/dm*") for to detect LVM
    blacklisted_devs = glob.glob("/sys/block/ram*") + glob.glob("/sys/block/loop*") + glob.glob("/sys/block/dm*")
    sysfs_devs = set(glob.glob("/sys/block/*")) - set(blacklisted_devs)
    for sysfs_dev in sysfs_devs:
        dev_file = sysfs_dev + "/dev"
        major, minor = open(dev_file).read().split(":")
        major = int(major)
        minor = int(minor)

        # Find a device listed in /proc/partitions
        # that has the same minor and major as our
        # current block device.
        for record in partitions:
            if major == record[0] and minor == record[1]:
                _devices.append(record[2])

    return _devices

def detect_lv():
    
    partitions = detect_procPartitions()
    
    _logicalVolumes = []
    blacklistDEVS = glob.glob("/sys/block/ram*") + glob.glob("/sys/block/loop*") + glob.glob("/sys/block/sd*")
    sysfs = set(glob.glob("/sys/block/*")) - set(blacklistDEVS)
    for device in sysfs:
        dev_node = device + "/dev"
        major, minor = open(dev_node).read().split(":")
        major = int(major)
        minor = int(minor)
        
        for record in partitions:
            if major == record[0] and minor == record[1]:
                #FIXME:If vg name has '-' character lvm convert it to '--'
                #FIXME:Recheck right lvm name splitting 
                name = open(device +"/dm/name").read().split("-")[-1]  
                uuid = open(device +"/dm/uuid").read()
                
                _logicalVolumes.append((name, uuid))
    
    return _logicalVolumes
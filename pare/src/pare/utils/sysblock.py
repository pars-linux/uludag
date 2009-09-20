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
from pare.lvmdevice import LogicalVolume, VolumeGroup
from pare.utils import lvm
from pare.errors import *
import os
import glob

# all disks
disks = []
# all logical volumes
vgs = []


def _comp(x, y):
    """sort disks using getName()"""
    x = x.name
    y = y.name
    if x > y: return -1
    elif x == y: return 0
    else: return 1

##
# initialize all devices and fill devices list
def init_disks(force = False):
    global disks
    if disks and not force:
        return True

    clear_disks()

    devs = detect_disks()
    for dev_path in devs:
        d = Disk(dev_path)
        disks.append(d)

    disks.sort(_comp,reverse=True)

    if disks:
        return True

    return False

def init_vgs():
    global vgs

    clear_vgs()


    volumegroups = detect_vgs()
    if len(volumegroups) > 0:
        for vg in volumegroups:
            info = lvm.vginfo(vg)
            if info:
                volumegroup = VolumeGroup(name=info['name'], size=info['size'], uuid=info['uuid'], maxPV=info['max_pv'], pvCount=info['pv_count'], peSize=info['vg_extent_size'], peCount=info['vg_extent_count'], peFree=info['vg_free_count'], freespace=info['vg_free'], maxLV= info['max_lv'], existing=1)
                vgs.append(volumegroup)

    vgs.sort(_comp, reverse=True)

    if vgs:
        return True

    return False

def clearAll():
    clear_disks()
    clear_lvs()

def clear_disks():
    global disks
    disks = []

def clear_vgs():
    global vgs
    vgs = []

def detect_procMounts():
    if not os.path.exists("/proc/mounts"):
        raise FileError("/proc/mounts")

    mounts = []
    for line in open("/proc/mounts"):
        entry = line.split()

        if not entry:
            continue
        mounts.append(entry[0])

    return  mounts

def detect_procPartitions():
    # Check for sysfs. Only works for >2.6 kernels.
    if not os.path.exists("/sys/bus"):
        raise FileError, "sysfs not found!"

    # Check for /proc/partitions
    if not os.path.exists("/proc/partitions"):
        raise FileError, "/proc/partitions not found!"

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
def detect_disks():

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

def _lvmNameParser(name):
    tmp = name.strip()
    tmp = tmp.replace("--", ".")
    lvm = tmp.split("-")
    vg = lvm[0].replace(".", "-")
    lv = lvm[1].replace(".", "-")

    return (vg,lv)

def detect_vgs():
    partitions = detect_procPartitions()

    _vgs = []
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
                name = open(device +"/dm/name").read()
                uuid = open(device +"/dm/uuid").read()
                vg=_lvmNameParser(name)[0]
                if vg in _vgs:
                    continue
                _vgs.append(vg)
                #_lvm.append((_lvmNameParser(name)[0],_lvmNameParser(name)[1], uuid))

    return _vgs


# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2008, TUBITAK/UEKAE
# Copyright 1999-2008 Gentoo Foundation
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# First version of storage.py has it's roots in GLI (Gentoo Linux
# Installer). It has changed overtime, making it somewhat incompatible
# with it though.

# Storage module handles disk/partitioning basics for
# installation. Basically it provides a Device interface to physical
# storage devices.


import parted
import os
import glob
import time
import struct
import binascii

from pardus.diskutils import *
from yali4.parteddata import *
from yali4.partition import Partition, FreeSpace
from yali4.exception import YaliError, YaliException
import yali4.sysutils as sysutils
import yali4.filesystem

class DeviceError(YaliError):
    pass

# all storage devices
devices = []

##
# initialize all devices and fill devices list
def init_devices(force = False):
    global devices

    if devices and not force:
        return True

    clear_devices()

    devs = detect_all()
    for dev_path in devs:
        d = Device(dev_path)
        devices.append(d)

    def comp(x, y):
        """sort disks using getName()"""
        x = x.getName()
        y = y.getName()

        if x > y: return -1
        elif x == y: return 0
        else: return 1

    devices.sort(comp,reverse=True)

    if devices:
        return True

    return False

def clear_devices():
    global devices
    devices = []

##
# Class representing a partitionable storage
class Device:

    ##
    # Init Device
    # @param device_path: Device node (eg. /dev/hda, /dev/sda)
    # @param arch: Architecture that we're partition for (defaults to 'x86')
    def __init__(self, device_path, arch="x86"):

        self._arch = arch
        self._path = ""
        self._device = None
        self._model = ""
        self._disk = None
        self._partitions = []
        self._disklabel = ""
        self._length = 0       # total sectors
        self._sector_size = 0
        self._parted_type = deviceType

        _partedDev = parted.Device(device_path)
        dev = _partedDev.getPedDevice()

        self._model = dev.model
        self._length = dev.length
        self._sector_size = dev.sector_size

        self._dev = dev
        self._disk = parted.Disk(_partedDev)
        #except:
        #    label = archinfo[self._arch]["disklabel"]
        #    disk_type = parted.diskType[label]
        #    self._disk = self._dev.disk_new_fresh(disk_type)

        self._disklabel = self._disk.type
        self._path = device_path
        self.update()

    ##
    # clear and re-fill partitions dict.
    def update(self):
        self._partitions = []
        for part in self._disk.partitions:
            self.__addToPartitionsDict(part)

    ##
    # do we have room for another primary partition?
    # @returns: boolean
    def primaryAvailable(self):
        primary = len(self.getPrimaryPartitions())
        if self.hasExtendedPartition(): primary += 1
        if primary == 4:
            return False
        return True


    def getType(self):
        return self._parted_type

    ##
    # get device capacity in bytes
    # @returns: long
    def getTotalBytes(self):
        return long(self._length * self._sector_size)

    ##
    # get device capacity in MBs
    # @returns: long
    def getTotalMB(self):
        return long(round(self.getTotalBytes() / MEGABYTE))

    def getTotalGB(self):
        return long(round(self.getTotalBytes() / GIGABYTE))

    ##
    # get device capacity string
    # @returns: string
    def getSizeStr(self):
        bytes = self.getTotalBytes()
        if bytes > GIGABYTE:
            return "%d GB" % self.getTotalGB()
        else:
            return "%d MB" % self.getTotalMB()

    ##
    # get device path (eg. /dev/hda)
    # @returns: string
    def getPath(self):
        return self._path

    ##
    # get device name (eg. hda)
    # @returns: string
    def getName(self):
        return os.path.basename(self.getPath())

    ##
    # get device model
    # @returns: string
    def getModel(self):
        return self._model

    ##
    # get partitions from disk
    # @returns: [Partition]
    def getPartitions(self):
        return self._partitions

    ##
    # get a partition by number
    # @param num: partition number
    #
    # @returns: Partition
    def getPartition(self, num):
        for part in self._partitions:
            if part._minor == num:
                return part
        return None

    ##
    # check if the device has an extended partition
    # @returns: True/False
    def hasExtendedPartition(self):
        if self.getExtendedPartition():
            return True
        return False

    ##
    # check if the device has a bootable partition
    # @returns: True/False
    def hasBootablePartition(self):
        flag = parted.PARTITION_BOOT
        for p in self.getPartitions():
            if not p._parted_type == freeSpaceType:
                ped = p.getPartition()
                if ped.is_flag_available(flag) and ped.get_flag(flag):
                    return True
        return False

    ##
    # get the extended partition on device (if it has one)
    def getExtendedPartition(self):
        for p in self.getPartitions():
            if p._partition.type == parted.PARTITION_EXTENDED:
                return p
        return None

    ##
    # get primary partitions on device
    # @returns: [Partition]
    def getPrimaryPartitions(self):
        l = []
        for p in self.getPartitions():
            if p._partition.type == parted.PARTITION_NORMAL:
                l.append(p)
        return l

    ##
    # get logical partitions on device
    # @returns: [Partition]
    def getLogicalPartitions(self):
        l = []
        for p in self.getPartitions():
            if p._partition.type == parted.PARTITION_LOGICAL:
                l.append(p)
        return l

    ##
    # get number of primary partitions on device
    # @returns: Number
    def numberOfLogicalPartitions(self):
        return len(self.getLogicalPartitions())

    ##
    # get number of primary partitions on device
    # @returns: Number
    def numberOfPrimaryPartitions(self):
        return len(self.getPrimaryPartitions())

    ##
    # get the partition list in an order
    # @returns: [Partition]
    def getOrderedPartitionList(self):

        def comp(x, y):
            """sort partitions using get_start()"""
            x = x.getStart()
            y = y.getStart()

            if x > y: return -1
            elif x == y: return 0
            else: return 1

        l = self.getPartitions()
        l.sort(comp,reverse=True)
        return l

    ##
    # get the total free space (in MB)
    # @returns: int
    def getFreeMB(self):
        size_total = self.getTotalMB()

        # 8: magic number that all, even windows, use.
        # (OK not really ;)
        size_parts = 8
        for p in self.getPartitions():
            # don't count logical parts and free spaces
            if not p.isLogical() and not p.isFreespace():
                size_parts += p.getMB()

        size = size_total - size_parts
        if size > 1:
            return size
        else:
            return 0

    def getLargestContinuousFreeMB(self):
        bytes = self.__pedPartitionBytes(self.__getLargestFreePedPartition())
        return long(bytes / MEGABYTE)

    ##
    # internal
    # get the largest, continuous free space (in MB)
    # @returns: parted.PedPartition
    def __getLargestFreePedPartition(self):
        size = 0
        largest = None
        for pedPart in self._disk.partitions:
            if parted.PARTITION_FREESPACE == pedPart.type:
                p_size = self.__pedPartitionBytes(pedPart)
                if p_size > size:
                    size = p_size
                    largest = pedPart
        return largest


    def __pedPartitionBytes(self, ped_part):
        if ped_part:
            return long(ped_part.geom.length *
                        self._sector_size)
        return 0

    ###############################
    # Partition mangling routines #
    ###############################

    ##
    # Add (create) a new partition to the device
    # @param part: parted partition; must be parted.PARTITION_FREESPACE
    # @param type: parted partition type (eg. parted.PARTITION_NORMAL)
    # @param fs: filesystem.FileSystem or file system name (like "ext3")
    # @param size_mb: size of the partition in MBs.
    def addPartition(self, part, type, fs, size_mb, flags = [], manualGeomStart = None):

        # Don't set bootable flag if there is already a bootable
        # partition in this disk. See bug #2217
        if (parted.PARTITION_BOOT in flags) and self.hasBootablePartition():
            flags = list(set(flags) - set([parted.PARTITION_BOOT]))

        size = int(size_mb * MEGABYTE / self._sector_size)

        if not part:
            part = self.__getLargestFreePedPartition()

        if not manualGeomStart:
            geom = part.geom

            # creating a partition
            if geom.length >= size:
                return self.addPartitionStartEnd(type,
                                                 fs,
                                                 geom.start,
                                                 geom.start + size,
                                                 flags)
        else:
            return self.addPartitionStartEnd(type,
                                             fs,
                                             manualGeomStart,
                                             manualGeomStart + size,
                                             flags)

        # if you are here and then we have some problems..
        raise DeviceError, ("Not enough free space on %s to create new partition" % self.getPath())

    ##
    # add a partition starting from a given geom...
    def addPartitionFromStart(self, type, fs, start, size_mb, flags = []):
        size = int(size_mb * MEGABYTE / self._sector_size)
        return self.addPartitionStartEnd(type, fs, start, start + size, flags)

    ##
    # Add (create) a new partition to the device from start to end.
    #
    # @param type: parted partition type (eg. parted.PARTITION_NORMAL)
    # @param fs: filesystem.FileSystem or file system name (string like "ext3")
    # @param start: start geom..
    # @param end: end geom
    def addPartitionStartEnd(self, type, fs, start, end, flags = []):

        if isinstance(fs, str):
            # a string... get the corresponding FileSystem object
            fs = yali4.filesystem.get_filesystem(fs)

        if isinstance(fs, yali4.filesystem.FileSystem):
            fs = fs.getFSType()
        else:
            fs = None

        constraint = self._disk.dev.constraint_any()
        newp = self._disk.partition_new(type, fs, start, end)
        for flag in flags:
            newp.set_flag(flag, 1)

        try:
            self._disk.add_partition(newp, constraint)
        except parted.error, e:
            raise DeviceError, e

        return self.__addToPartitionsDict(newp, fs_ready=False)

    ##
    # (internal function)
    # add partition to the partitions dictionary
    # @param part: pyparted partition type
    #
    # @returns: Partition
    def __addToPartitionsDict(self, part, fs_ready=True):
        geom = part._geometry
        part_mb = long((geom.end - geom.start + 1) * self._sector_size / MEGABYTE)
        if part.number >= 1:
            fs_name = ""
            if part._fileSystem:
                fs_name = part._fileSystem._type
            elif part.type & parted.PARTITION_EXTENDED:
                fs_name = "extended"

            self._partitions.append(Partition(self, part,
                                                    part.number,
                                                    part_mb,
                                                    geom.start,
                                                    geom.end,
                                                    fs_name,
                                                    fs_ready))

        elif part.type & parted.PARTITION_FREESPACE and part_mb >= 10:
            self._partitions.append(FreeSpace(self, part,
                                                    part_mb,
                                                    geom.start,
                                                    geom.end))
        return part

    ##
    # delete a partition
    # @param part: Partition
    def deletePartition(self, part):
        self._disk.delete_partition(part.getPartition())
        self.update()

    def deleteAllPartitions(self):
        self._disk.deleteAllPartitions()
        self.update()

    def resizePartition(self, fs, size_mb, part):

        # maximum cylinder size currently is less than 140 MB hence
        # this extra size should be always enough.
        #
        # see: http://mlf.linux.rulez.org/mlf/ezaz/ntfsresize.html
        size_mb += 150

        if isinstance(fs, str):
            # a string... get the corresponding FileSystem object
            fs = yali4.filesystem.get_filesystem(fs)

        if not isinstance(fs, yali4.filesystem.FileSystem):
            raise DeviceError, "filesystem is None, can't resize"

        if not fs.resize(size_mb, part):
            raise DeviceError, "fs.resize ERROR"

        start = part.getPartition().geom.start
        fs_name = part.getFSName()
        if part.isLogical():
            ptype = PARTITION_LOGICAL
        else:
            ptype = PARTITION_NORMAL
        time.sleep(3)
        self.deletePartition(part)
        self.commit()
        np = self.addPartitionFromStart(ptype, fs_name, start, size_mb)
        self.commit()
        return np

    def commit(self):
        self._disk.commit()
        self.update()

    def close(self):
        # pyparted will do it for us.
        del self._disk

def setOrderedDiskList():
    devices = detect_all()
    devices.sort()

    import yali4.gui.context as ctx

    # Check EDD Module
    if not os.path.exists("/sys/firmware/edd"):
        cmd_path = sysutils.find_executable("modprobe")
        cmd = "%s %s" % (cmd_path, "edd")
        p = os.popen(cmd)
        o = p.readlines()
        if p.close():
            ctx.installData.orderedDiskList = devices
            ctx.debugger.log("ERROR : Inserting EDD Module failed !")
            return

    edd = EDD()
    sortedList = []
    edd_list = edd.list_edd_signatures()
    mbr_list = edd.list_mbr_signatures()
    edd_keys = edd_list.keys()
    edd_keys.sort()
    for bios_num in edd_keys:
        edd_sig = edd_list[bios_num]
        if mbr_list.has_key(edd_sig):
            sortedList.append(mbr_list[edd_sig])

    if len(devices) > 1:
        a = ctx.installData.orderedDiskList = sortedList
        b = devices
        # check consistency of diskList
        if not len(filter(None, map(lambda x: x in a,b))) == len(b):
            ctx.installData.orderedDiskList = devices
            ctx.isEddFailed = True
    else:
        ctx.installData.orderedDiskList = devices

##
# Return a list of block devices in system
def detect_all():

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

    _devices = []
    # Scan sysfs for the device types.
    blacklisted_devs = glob.glob("/sys/block/ram*") + glob.glob("/sys/block/loop*")
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

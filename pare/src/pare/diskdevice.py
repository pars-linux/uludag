# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
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
from pare.partition import Partition, FreeSpace
from pare.errors import PareError
import pare.utils.sysutils as sysutils
from pare.filesystem import getFilesystem, FileSystem
from pare.parteddata import *

import logging
log = logging.getLogger("pare")

class DeviceError(PareError):
    pass

# all storage devices
disks = []

##
# initialize all devices and fill devices list
def init(force = False):
    global disks

    if disks and not force:
        return True

    clear_devices()

    devs = detect_all()
    for dev_path in devs:
        d = Disk(dev_path)
        disks.append(d)

    def comp(x, y):
        """sort disks using getName()"""
        x = x.name
        y = y.name

        if x > y: return -1
        elif x == y: return 0
        else: return 1

    disks.sort(comp,reverse=True)

    if disks:
        return True

    return False

def clear_devices():
    global devices
    devices = []

##
# Class representing a partitionable storage
class Disk:
    
    
    _type = deviceType
    # @param device_path: Device node (eg. /dev/hda, /dev/sda)
    # @param arch: Architecture that we're partition for (defaults to 'x86')
    def __init__(self, path, arch="x86"):

        self._arch = arch
        self._path = ""
        self._device = None
        self._model = ""
        self._disk = None
        self._disklabel = ""
        self._length = 0       # total sectors
        self._sectorSize = 0
        self._isSetup = False

        device = parted.Device(path)

        self._model = device.model
        self._length = device.length
        self._sectorSize = device.sectorSize

        self._device = device
        try:
            self._disk = parted.Disk(device)
        except:
            print "freshhdisk yaratılıyor"
            label = archinfo[self._arch]["disklabel"]
            self._disk = parted.freshDisk(self._device, ty=label)

        self._disklabel = self._disk.type

        self._path = path

    
    
    ##
    # do we have room for another primary partition?
    # @returns: boolean
    def primaryAvailable(self):
        primary = len(self.getPrimaryPartitions())
        if self.hasExtendedPartition(): primary += 1
        if primary == 4:
            return False
        return True

    @property
    def type(self):
        return self._type

    def needSetup(self, bool):
        self._isSetup = bool
    
    def isSetup(self):
        return self._isSetup
        
    def getSize(self, unit='MB'):
        return self._disk.device.getSize(unit)

    @property
    def sizeStr(self):
        bytes = self.getSize()
        if bytes > GIGABYTE:
            return "%d GB" % self.getSize("GB")
        else:
            return "%d MB" % self.getSize()


    @property
    def sectorSize(self):
        return self._sectorSize
    
    @property
    def path(self):
        return self._path

    @property
    def name(self):
        return os.path.basename(self.path)

    @property
    def model(self):
        return self._model

    ##
    # check if the device has an extended partition
    # @returns: True/False
    def hasExtendedPartition(self):
        if self.extendedPartition:
            return True
        return False

    ##
    # check if the device has a bootable partition
    # @returns: True/False
    def hasBootablePartition(self):
        flag = parted.PARTITION_BOOT
        for partition in self.getAllPartitions():
            if not partition.type == parted.PARTITION_FREESPACE:
                if partition.isFlagAvailable(flag) and partition.getFlag(flag):
                    return True
        return False

    @property
    def extendedPartition(self):
        return self._disk.getExtendedPartition()
        

    @property
    def primaryPartitions(self):
        return self._disk.getPrimaryPartitions()

    @property
    def logicalPartitions(self):
        return self._disk.getLogicalPartitions()

    @property
    def numberOfLogicalPartitions(self):
        return len(self.logicalPartitions)

    ##
    # get number of primary partitions on device
    # @returns: Number
    def numberOfPrimaryPartitions(self):
        return len(self.primaryPartitions)

    def getAllPartitions(self):
        allparts = []
        part = self._disk.getFirstPartition()
        while part:
            #Cant get metadata partitions
            if part.getSize(unit="MB") > 10:
                allparts.append(part)
            part = part.nextPartition()
        return allparts
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

        l = self.partitions
        l.sort(comp,reverse=True)
        return l

    ##
    # get the total free space (in MB)
    # @returns: int
    def getFreeSize(self):
        disksize = self.getSize()

        # 8: magic number that all, even windows, use.
        # (OK not really ;)
        partsize = 8
        for part in self.partitions:
            # don't count logical parts and free spaces
            if not part.isLogical and not p.isFreespace:
                partsize += part.size

        size = disksize - partsize
        if size > 1:
            return size
        else:
            return 0


    def getLargestFreePartition(self):
        size = 0
        largest = None
        freespaces = self._disk.getFreeSpacePartitions()
        for part in freespaces:
            if part.getSize() > size:
                size = part.getSize()
                largest = part
        
        return largest

    def addPartition(self, type, filesystem, start, end, flags = []):
        constraint = self._device.getConstraint()
        geom = parted.Geometry(self._device, start, end=end)
        part = parted.Partition(self._disk, type, geometry=geom)
        
        for flag in flags:
            part.setFlag(flag)

        try:
            return self._disk.addPartition(part, constraint)
        except parted.error, e:
            raise DeviceError, e
        
        return True

    ##
    # delete a partition
    # @param part: Partition
    def deletePartition(self, part):
        self._isSetup = True
        return self._disk.deletePartition(part)

    def deleteAllPartitions(self):
        return self._disk.deleteAllPartitions()

    def resizePartition(self, filesystem, size, partition):

        start = partition.geom.start
        
        if partition.isLogical:
            type = parted.PARTITION_LOGICAL
        else:
            type = parted.PARTITION_NORMAL
            
        time.sleep(3)
        self.deletePartition(partition)
        self.commit()
        np = self.addPartition(type, fileSystem, start, size)
        self.commit()
        return np

    def commit(self):
        try:
            self._disk.commit()
        except:
            sysutils.run("sync")
            time.sleep(3)
            sysutils.run("sync")
            log.error("Commit Failed!")
            self._disk.commit()
            self._isSetup = False

    def close(self):
        # pyparted will do it for us.
        del self._disk


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
    #FIXME:Added glob.glob("/sys/block/sda*") for unhandled parition table destroy test later it will erased
    blacklisted_devs = glob.glob("/sys/block/ram*") + glob.glob("/sys/block/loop*") + glob.glob("/sys/block/sda*")
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

# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file


import os
import parted
from errors import *
import pare.utils.sysblock as sysblock
from pare.partition import *


import logging
log = logging.getLogger("pare")


class Storage(object):
    _partitionTable = {}
    _diskTable = {}
    _lvmTable = {}
    _raidTable = {}

    def __init__(self):
        if storage.init():
            for disk in sysblock.disks:
                if isinstance(disk, storage.Disk):
                    self._diskTable[disk.path] =  disk
                else:
                    raise PareError("Filling Disk failed!")
            for disk in self._diskTable.values():    
                self._update(disk)

    #FIXME:ready can change Partition existing and setup Parameter!!! 
    def _addPartitionDict(self, disk, part, ready=True):

        def getParePartition(disk, part):
            geom = part.geometry
            size = part.getSize()
            print "### %s partition.geom:%s partition.size:%s" % (disk.path, geom.start, size )
            if part.number >= 1:
                filesystem = ""
                if part.filesystem:
                    filesystem = part.filesystem.name
                #FIXME:Check LVM, RAID, Partition assignment
                if part.type & parted.PARTITION_LVM:
                    return PhysicalVolume(disk, part, part.number, size, geom.start, geom.end, filesystem, ready)
                elif part.type & parted.PARTITION_RAID:
                    return RaidMember(disk, part, part.number, size, geom.start, geom.end, filesystem, ready)
                else:
                    if part.type & parted.PARTITION_EXTENDED:
                        filesystem = "extended"
                        print "disk %s partition.name:%s" % (disk.path, part.path)
                        return Partition(disk, part, part.number, size, geom.start, geom.end, filesystem, ready)

            elif part.type & parted.PARTITION_FREESPACE and size >= 10:
                return FreeSpace(disk, part, size, geom.start, geom.end)
                print "FreeSpace disk %s partition.name:%s" % (disk.path, part.name)

        if not self._partitionTable.has_key(disk.path):
            #print "getParePartition(disk,part).name:%s" % getParePartition(disk,part)
            self._partitionTable[disk.path] = [getParePartition(disk,part)]
        else:
            #print "getParePartition(disk,part).name:%s" % getParePartition(disk,part)
            self._partitionTable[disk.path].append(getParePartition(disk, part))

    def _update(self, disk):

            print "len:%d" % len(disk.getAllPartitions())
            for part in disk.getAllPartitions():
                print "part.path name:%s" % part.path
                self._addPartitionDict(disk, part)

    @property
    def disks(self):
        return self._diskTable.values()

    def diskPartitions(self, disk):
        return self._partitionTable[disk]


    def getPartition(self, disk, num):
        for part in self.diskPartitions(disk):
            if part.minor == num:
                return part
        return None

    def commitToDisk(self, disk):
        self._diskTable[disk].commit()
        for partition in self.diskPartitions(disk):
            partition.exists = True

    ##
    # Add (create) a new partition to the device
    # @param part: parted partition; must be parted.PARTITION_FREESPACE
    # @param type: parted partition type (eg. parted.PARTITION_PRIMARY)
    # @param fs: filesystem.FileSystem or file system name (like "ext3")
    # @param size_mb: size of the partition in MBs.
    def addPartition(self, pareDisk, parePartition, parePartitionType, pareFilesystem, size, flags = [], manualGeomStart = None):

        size = int((size * MEGABYTE) / pareDisk.sectorSize)

        if isinstance(pareFilesystem, str):
            filesystem = getFilesystem(pareFilesystem)

        if isinstance(filesystem, FileSystem):
            filesystemType = filesystem.fileSystemType
        else:
            filesystemType = None

        # Don't set bootable flag if there is already a bootable
        # partition in this disk. See bug #2217
        if (parted.PARTITION_BOOT in flags) and pareDisk.hasBootablePartition():
            flags = list(set(flags) - set([parted.PARTITION_BOOT]))

        if not parePartition.partition:
            partion = pareDisk.__getLargestFreePartition()

        if not manualGeomStart:
            geom = parePartition.partition.geometry
            if geom.length >= size:
                if pareDisk.addPartition(parePartitionType, filesystem, geom.start, geom.start + size,flags):
                    #FIXME:Check partitions existing state conditions?
                    self._update(pareDisk)
                else:
                    raise DeviceError, ("Not enough free space on %s to create new partition" % self.getPath())
        else:
            if pareDisk.addPartition(type,filesystem,manualGeomStart,manualGeomStart + size, flags):
                #FIXME:Check partitions existing state conditions?
                self._update(pareDisk)
            else:
                raise DeviceError, ("Not enough free space on %s to create new partition" % self.getPath())


    def deletePartition(self, pareDisk, parePartition):
        if not self._diskTable[pareDisk.path].deletePartition(parePartition.partition):
            raise PareError("Partition delete failed!")
        else:
            self._update(pareDisk)
            return True

    def deleteAllPartitions(self, pareDisk, parePartition):
        if not self._partitionTable[pareDisk.path].deleteAllPartition():
            raise PareError("All Partitions delete failed!")
        else:
            return True

    def resizePartition(self, pareDisk, parePartition, pareFileSystem, size):
        if isinstance(pareFileSystem, str):
            filesystem = getFilesystem(pareFileSystem)

        if not isinstance(pareFileSystem, FileSystem):
            raise PareError, "filesystem is None, can't resize"

        if not filesystem.resize(size, parePartition.path):
            raise PareError, "fs.resize ERROR"
        else:
           fileSystem = parePartition.getFileSystemType()
           if not pareDisk.resizePartition(filesystem,size,parePartition.partition):
               raise PareError("partition.resize failed!")
           else:
               return True

    def createVolumeGroup(self):
        pass


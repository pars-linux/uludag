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
import pare.diskdevice as storage
from pare.partition import *


import logging
log = logging.getLogger("pare")

class Pare(object):
    _partitionTable = {}
    _diskTable = {}
    _lvmTable = {}
    _raidTable = {}
    
    def __init__(self):
        if storage.init_devices():
            for disk in storage.disks:
                if isinstance(disk, storage.Disk):
                    self._diskTable[disk.path] =  disk
                else:
                    raise PareError("Filling Disk failed!")
            for disk in self._diskTable.itervalues():    
                self._update(disk)
    
    def _addPartitionDict(self, disk, part):
        
        def getParePartition(disk, part):
            geom = part.geometry
            size = part.getSize()
            if part.number >= 1:
                type = ""
                if part.fileSystem.name:
                    type = part.fileSystem.name
                elif part.type & parted.PARTITION_EXTENDED:
                    type = "extended"

                return Partition(disk, part,part.number,size,
                                 geom.start,geom.end,name,ready)
            
            elif part.type & parted.PARTITION_FREESPACE and size >= 10:
                return FreeSpace(disk, part, size, geom.start, geom.end)
        
        if not self._partitionTable.has_key(disk.path):
            #print "getParePartition(disk,part).name:%s" % getParePartition(disk,part)
            self._partitionTable[disk.path] = [getParePartition(disk,part)]
        else:
            #print "getParePartition(disk,part).name:%s" % getParePartition(disk,part)
            self._partitionTable[disk.path].append(getParePartition(disk, part))
    
    def _update(self, disk):
        
            print "len:%d" % len(disk.getAllPartitions())
            for part in disk.getAllPartitions():
                print "name:%s" % part.path
                self._addPartitionDict(disk, part)
    
    @property                
    def disks(self):
        return self._diskTable.itervalues()
    
    def diskPartitions(self, disk):
        return self._partitionTable[disk]
    
    
    def getPartition(self, disk, num):
        for part in self.partitions(disk):
            if part.minor == num:
                return part
        return None
    
    ##
    # Add (create) a new partition to the device
    # @param part: parted partition; must be parted.PARTITION_FREESPACE
    # @param type: parted partition type (eg. parted.PARTITION_PRIMARY)
    # @param fs: filesystem.FileSystem or file system name (like "ext3")
    # @param size_mb: size of the partition in MBs.
    def addPartition(self, pareDisk, parePartion, parePartitionType, pareFilesystem, size, flags = [], manualGeomStart = None):
        
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

        if not parePartion.partition:
            partion = pareDisk.__getLargestFreePartition()

        if not manualGeomStart:
            geom = parePartition.partition.geometry
            if geom.length >= size:
                if pareDisk.addPartitionStartEnd(type,filesystem,
                                                 geom.start, geom.start + size,flags):
                    self._update()
        else:
            if pareDisk.addPartitionStartEnd(type,filesystem,manualGeomStart,
                                          manualGeomStart + size, flags):
                self._update()
            
        raise DeviceError, ("Not enough free space on %s to create new partition" % self.getPath())
       
    
    def deletePartition(self, pareDisk, parePartition):
        if not self._partitionTable[pareDisk.path].deletePartition(parePartition.partition):
            raise PareError("Partition delete failed!")
        else:
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
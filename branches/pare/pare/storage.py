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
from pare.diskdevice import Disk
from pare.lvmdevice import VolumeGroup, LogicalVolume
from pare.partition import *
import pare.parteddata as parteddata


import logging
log = logging.getLogger("pare")


class Storage(object):
    _devices = []


    def __init__(self):
        self.populate()

    def _vgs(self):
        """ VGs' Name dict to access VG"""
        vgs = {}
        for vg in self.volumeGroups:
            if vg.name in vgs:
                raise ValueError("Duplicate VG in Volume Groups")
            vgs[vg.name] = vg

        return vgs

    def populate(self):
        if sysblock.init_disks():
            for disk in sysblock.disks:
                if isinstance(disk, Disk):
                    self._devices.append(disk)
                else:
                    raise PareError("Filling Disk failed!")

        if sysblock.init_vgs():
            print "LVM BULUNDU"
            for vg in sysblock.vgs:
                if isinstance(vg, VolumeGroup):
                    #vg = VolumeGroup(name=info[0], size=info[1], uuid=info[2], maxPV=info[3], pvCount=info[4], peSize=info[5], peCount=info[6], peFree=info[7], freespace=info[8], maxLV=info[9], existing=1)
                    self._devices.append(vg)
                else:
                    raise PareError("Filling Volume Group Failed!")

    @property
    def disks(self):
        return [d for d in self._devices if d.type == parteddata.disk]

    @property
    def volumeGroups(self):
        return [d for d in self._devices if d.type == parteddata.volumeGroup]

    @property
    def logicalVolumes(self):
        lvs = []
        for vg in self.volumeGroups:
            lvs.extend(vg.lvs)
        return lvs

    def physicalVolumes(self, disk):
        _physicalVolumes = []

        for part in disk.partitions:
            if parteddata.physicalVolume == part.type:
                print "disk.name %s part.name %s" % (disk.name,part.name)
                _physicalVolumes.append(part)

        return _physicalVolumes



    def diskPartitions(self, disk):
        return disk.partitions

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
                if not pareDisk.addPartition(parePartitionType, filesystem, geom.start, geom.start + size,flags):
                    raise DeviceError, ("Not enough free space on %s to create new partition" % self.getPath())
        else:
            if not pareDisk.addPartition(type,filesystem,manualGeomStart,manualGeomStart + size, flags):
                raise DeviceError, ("Not enough free space on %s to create new partition" % self.getPath())


    def deletePartition(self, pareDisk, parePartition):
        if not pareDisk.deletePartition(parePartition.partition):
            raise PareError("Partition delete failed!")

        return True

    def deleteAllPartitions(self, pareDisk):
        if not pareDisk.deleteAllPartition():
            raise PareError("All Partitions delete failed!")
        return True

    def resizePartition(self, pareDisk, parePartition, pareFileSystem, size):
        if isinstance(pareFileSystem, str):
            filesystem = getFilesystem(pareFileSystem)
        else:
            filesystem = pareFileSystem

        if not isinstance(filesystem, FileSystem):
            raise PareError, "filesystem is None, can't resize"

        if not filesystem.resize(size, parePartition.path):
            raise PareError, "fs.resize ERROR"
        else:
           fileSystem = parePartition.getFileSystemType()
           if not pareDisk.resizePartition(filesystem,size,parePartition.partition):
               raise PareError("partition.resize failed!")
           else:
               return True

    def removeVG(self, vg):
        pass

    def removeLV(self, lv):
        """
            logicalVolume -- LV' name
        """
        if not isinstance(lv, LogicalVolume):
            raise ValueError("lv parameter must be type of lvmdevice.LogicalVolume")
        else:
            lv.destroy()



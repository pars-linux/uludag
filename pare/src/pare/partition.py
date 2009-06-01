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
#

import os
import parted

from pare.filesystem import FileSystem, getFilesystem
from pare.parteddata import partition, physicalVolume, raidMember, freeSpace
from pare.errors import *
import gettext
_ = lambda x:gettext.ldgettext("pare", x)

##
# Class representing a single partition within a Device object
class Partition:

    _type = partition

    def __init__(self, disk, partedPartition, minor, size, start, end, format, existing=False):
        self._disk = disk
        self._partedPartition = partedPartition
        self._minor = minor
        self._size = size
        self._start = start
        self._end = end
        self._format = format
        self._exists = existing
        self.tmpLabel = ''

    def setup(self):
        if not self.exists:
            raise PartitionError("Partition has not been created!")

        if self.status:
            self.format.setup()

    def teardown(self):
        if not self.exists:
            raise PartitionError("Partition has not been created!")

        if self.status and self.format.exists:
            self.format.teardown()
            #FIXME:add udev_settle()

    @property
    def exists(self):
        return self._exists

    @property
    def status(self):
        """ Add parted cache list but it cant be committed to disk"""
        if not self.exists:
            return False

        return os.access(self.path, os.W_OK)

    def setFileSystemType(self, _format):
        if isinstance(_format, FileSystem):
            _format = _format.fileSystemType
        elif isinstance(_format, str):
            _format = getFilesystem(_format).fileSystemType

        self.partition.fileSystem = _format

    def getFileSystemType(self):
        return self.partition.fileSystem.name    

    def getFSYSName(self):
        return getFilesystem(self.getFileSystemType())._sysname

    def setPartedFlags(self, flags):
        for flag in flags:
            if self.partition.isFlagAvailable(flag):
                self.partition.setFlag(flag)

    @property
    def isLogical(self):
        return self.partition.type == parted.PARTITION_LOGICAL

    @property
    def isFreespace(self):
        return self.partition.type == parted.PARTITION_FREESPACE

    @property
    def isExtended(self):
        return self.partition.type == parted.PARTITION_EXTENDED

    @property
    def isRaid(self):
        return self.partition.type == parted.PARTITION_RAID

    @property
    def isLvm(self):
        return self.partition.type == parted.PARTITION_LVM

    def getFreeMB(self):
        return self.disk.getFreeSize()

    @property
    def type(self):
        return self._type

    @property
    def partition(self):
        return self._partedPartition

    @property
    def disk(self):
        return self._disk

    @property
    def diskPath(self):
        return self.disk.path

    @property
    def path(self):
        if self.partition.type == parted.PARTITION_FREESPACE:
            return "N/A"
        if self.diskPath.find("cciss") > 0:
            # HP Smart array controller
            return "%sp%d" %(self.diskPath, self.minor)
        else:
            return "%s%d" %(self.diskPath, self.minor)

    @property
    def name(self):
        return os.path.basename(self.path)

    @property
    def minor(self):
        return self._minor

    def _getFormat(self):
        return self._format

    def _setFormat(self, _format):
        self._format = _format

    format = property(lambda p: p._getFormat(), lambda p,f:_setFormat(f))

    @property
    def resizable(self):
        try:
            return self.format.isResizable()
        except AttributeError, e:
            return False

    def _getTmpLabel(self):
        return self.tmpLabel

    def _setTmpLabel(self,label):
        self.tmpLabel = label

    tmpLabel = property(lambda p: p._getTmpLabel(), lambda p,f:p_setTmpLabel(f))

    @property
    def label(self):
        try:
            return self.format.getLabel(self)
        except AttributeError, e:
            return None

    @property
    def minResizeMB(self):
        try:
            return self.format.minResizeMB(self)
        except AttributeError, e:
            return None

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def bytes(self):
        return long(self.partition.geom.length * self.disk.device.sectorSize)

    def size(self,unit=''):
        return self._size

    def getSizeStr(self, manual=None):
        gb = self.getGB()
        if manual:
            gb = manual / parteddata.KILOBYTE
        if gb > 1:
            return "%0.2f GB" % gb
        else:
            return "%0.2f MB" % self.getMB()

    ##
    # is equal? compare the partiton start/ends
    # @param: Partition
    # returns: Boolean
    def __eq__(self, rhs):
        return self.start == rhs.start and self.end == rhs.end


class PhysicalVolume(Partition):
    _type = physicalVolume

    def __init__(self, disk, partedPartition, minor, size, start,end,format,exists):
        Partition.__init__(self, disk,
                           partedPartition,
                           minor,
                           size,
                           start,
                           end,
                           format,exists)

class RaidMember(Partition):
    _type = raidMember

    def __init__(self, disk, partedPartition, minor, size, start,end,format,exists):
        Partition.__init__(self, disk,
                           partedPartition,
                           minor,
                           size,
                           start,
                           end,
                           format,exists)



class FreeSpace(Partition):
    _type = freeSpace

    def __init__(self, disk, part, size, start, end):
        Partition.__init__(self, disk,
                           part,
                           -1,
                           size,
                           start,
                           end,
                           _("free space"))


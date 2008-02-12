# -*- coding: utf-8 -*-
#
# Copyright (C) TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# partition types that will be used in installation process

import parted

import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

import yali4.filesystem

class PartitionType:

    filesystem = None

    ##
    # is equal
    # @param rhs: PartitionType
    def __eq__(self, rhs):
        if rhs:
            return self.filesystem == rhs.filesystem
        return False

##
# not an intuitive name but need group home and root :(
class __PartitionType(PartitionType):

    def __init__(self):
        # check cmdline for reiserfs support
        cmdline = open("/proc/cmdline", "r").read()
        if cmdline.find("enable_reiserfs") >= 0:
            self.filesystem = yali4.filesystem.ReiserFileSystem()
        elif cmdline.find("enable_xfs") >= 0:
            self.filesystem = yali4.filesystem.XFSFileSystem()
        else:
            self.filesystem = yali4.filesystem.Ext3FileSystem()


class RootPartitionType(__PartitionType):
    name = _("Install Root")
    mountpoint = "/"
    mountoptions = "noatime"
    parted_type = parted.PARTITION_PRIMARY
    parted_flags = [ parted.PARTITION_BOOT ]
    label = "PARDUS_ROOT"


class HomePartitionType(__PartitionType):
    name = _("Users' Files")
    mountpoint = "/home"
    mountoptions = "noatime"
    parted_type = parted.PARTITION_PRIMARY
    parted_flags = []
    label = "PARDUS_HOME"


class SwapPartitionType(PartitionType):
    name = _("Swap")
    filesystem = yali4.filesystem.SwapFileSystem()
    mountpoint = None
    mountoptions = "sw"
    parted_type = parted.PARTITION_PRIMARY
    parted_flags = []
    label = "PARDUS_SWAP"

class ArchivePartitionType(PartitionType):
    name = _("Archive Partition")
    filesystem = yali4.filesystem.Ext3FileSystem()
    mountpoint = "/mnt/archive"
    mountoptions = "noatime"
    parted_type = parted.PARTITION_PRIMARY
    parted_flags = []
    label = "ARCHIVE"

    def setFileSystem(self, filesystem):
        if filesystem == "fat32":
            self.filesystem = yali4.filesystem.FatFileSystem()
        elif filesystem == "ext3":
            self.filesystem = yali4.filesystem.Ext3FileSystem()

##
# mountpoint'e göre custom partition oluştur.
class CustomPartitionType(PartitionType):
    def __init__(self, name, mountpoint, mountoptions, parted_type, 
                 parted_flags, filesystem=None, label=None):
        self.name = name
        if filesystem:
            self.filesystem = filesystem
        self.mountpoint = mountpoint
        self.parted_type = parted_type
        self.parted_flags = parted_flags
        if label:
            self.label = label
        else:
            self.label = "ARCHIVE"
            

class RaidPartitionType(PartitionType):
    def __init__(self, raidminor=None, raidlevel = None, raidmembers = None,
                 raidspares = None, chunksize = None, isdummy = True):
        self.name = _("Software RAID")
        self.filesystem = yali4.filesystem.RaidFileSystem()
        self.mountpoint = None
        self.mountoptions = None
        self.parted_type = parted.PARTITION_RAID
        self.parted_flags = []
        self.label = "SOFTWARE_RAID"
        
        self._isdummy = isdummy
        self._raidminor = raidminor
        # we dont need this for dummy raid partitions
        if not isdummy:
            self._raidlevel = raidlevel
            self._raidmembers = raidmembers
            self._raidspares = raidspares
            self._chunksize = chunksize
        
    def sanityCheck(self):
        minmembers = yali4.raid.get_raid_min_members(self._raidlevel)
        if len(self._raidmembers) < minmembers:
            return _("A Raid device of type %s "
                     "requires at least %s members.") % (self._raidlevel,
                                                         minmembers)
                     
        if len(self._raidmembers) > 27:
            return "Raid devices are limited to 27 members"
        
        if self._raidspares:
            if (len(self._raidmembers) - self._raidspares) < minmembers:
                return _("This Raid device can have a maximum of %s spares. "
                         "To have more spares, you should add more members "
                         "to raid device.") % ( len(self._raidmembers) - minmembers )
        
        return None
    
    def getMinor(self):
        return self._raidminor


root = RootPartitionType()
home = HomePartitionType()
swap = SwapPartitionType()
archive = ArchivePartitionType()
raid = RaidPartitionType()


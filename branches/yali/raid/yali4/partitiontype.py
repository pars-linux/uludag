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
    needsmtab = True
    ##
    # is equal
    # @param rhs: PartitionType
    def __eq__(self, rhs):
        if rhs:
            if hasattr(rhs, "filesystem"):
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
    parttype = "root"
    name = _("Install Root")
    mountpoint = "/"
    mountoptions = "noatime"
    parted_type = parted.PARTITION_PRIMARY
    parted_flags = [ parted.PARTITION_BOOT ]
    label = "PARDUS_ROOT"

class HomePartitionType(__PartitionType):
    parttype = "home"
    name = _("Users' Files")
    mountpoint = "/home"
    mountoptions = "noatime"
    parted_type = parted.PARTITION_PRIMARY
    parted_flags = []
    label = "PARDUS_HOME"

class SwapPartitionType(PartitionType):
    parttype = "swap"
    name = _("Swap")
    filesystem = yali4.filesystem.SwapFileSystem()
    mountpoint = None
    mountoptions = "sw"
    parted_type = parted.PARTITION_PRIMARY
    parted_flags = []
    label = "PARDUS_SWAP"

class ArchivePartitionType(PartitionType):
    parttype = "archive"
    name = _("Archive Partition")
    filesystem = yali4.filesystem.Ext3FileSystem()
    mountpoint = "/mnt/archive"
    mountoptions = "noatime"
    parted_type = parted.PARTITION_PRIMARY
    parted_flags = []
    label = "ARCHIVE"

    def setFileSystem(self, filesystem):
        supportedFS = {"fat32":yali4.filesystem.FatFileSystem(),
                       "ext3" :yali4.filesystem.Ext3FileSystem(),
                       "ntfs" :yali4.filesystem.NTFSFileSystem()}
        if supportedFS.has_key(filesystem):
            self.filesystem = supportedFS[filesystem]

##
#
class CustomPartitionType(__PartitionType):
    parttype = "custom"
    
    def __init__(self, name=None, parted_type=None, parted_flags=None, \
                 filesystem=None, label=None, mountpoint=None, mountoptions=None):

        self.name = name
        if filesystem:
            self.filesystem = filesystem
        self.mountpoint = mountpoint
        self.mountoptions = mountoptions
        self.parted_type = parted_type
        self.parted_flags = parted_flags
        self.label = label

    def setName(self, name):
        self.name = name
        
    def setMountPoint(self, mp):
        self.mountpoint = mp
        
    def setMountOptions(self, mo):
        self.mountoptions = mo
        
    def setFileSystem(self, fs):
        self.filesystem = filesystem
        
    def setLabel(self, label):
        self.label = label
        
    def setPartedFlags(self, flags):
        self.parted_flags = flags
        
    def setPartedType(self, pt):
        self.parted_type 
        
    def getName(self):
        return self.name
        
    def getMountPoint(self):
        return self.mountpoint
        
    def getMountOptions(self):
        return self.mountoptions
        
    def getFileSystem(self):
        return self.filesystem
        
    def getLabel(self):
        return self.label
        
    def getPartedFlags(self):
        return self.parted_flags
        
    def getPartedType(self):
        return self.parted_type
        
##            
# A partition that will be part of a raid
class RaidPartitionType(CustomPartitionType):
    parttype = "raid"
    def __init__(self):
        self.name = _("Software RAID")
        self.parted_flags = [ parted.PARTITION_RAID ]
        
        CustomPartitionType.__init__(self, self.name, parted.PARTITION_RAID,
                                     self.parted_flags, yali4.filesystem.RaidFileSystem(),
                                     "SOFTWARE_RAID" )
     

root = RootPartitionType()
home = HomePartitionType()
swap = SwapPartitionType()
archive = ArchivePartitionType()



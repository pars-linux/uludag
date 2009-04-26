# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2008, TUBITAK/UEKAE
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
            self.filesystem = yali4.filesystem.get_filesystem("reiserfs")
        elif cmdline.find("enable_xfs") >= 0:
            self.filesystem = yali4.filesystem.get_filesystem("xfs")
        else:
            # In Pardus 2009 ext4 will be default fs
            self.filesystem = yali4.filesystem.get_filesystem("ext4")

class RootPartitionType(__PartitionType):
    name = _("Install Root")
    mountpoint = "/"
    mountoptions = "noatime"
    parted_type = parted.PARTITION_NORMAL
    parted_flags = [ parted.PARTITION_BOOT ]
    label = "PARDUS_ROOT"

class HomePartitionType(__PartitionType):
    name = _("Users' Files")
    mountpoint = "/home"
    mountoptions = "noatime"
    parted_type = parted.PARTITION_NORMAL
    parted_flags = []
    label = "PARDUS_HOME"

class SwapPartitionType(PartitionType):
    name = _("Swap")
    filesystem = yali4.filesystem.get_filesystem("swap")
    mountpoint = None
    mountoptions = "sw"
    parted_type = parted.PARTITION_NORMAL
    parted_flags = []
    label = "PARDUS_SWAP"

class ArchivePartitionType(PartitionType):
    name = _("Archive Partition")
    mountpoint = "/mnt/archive"
    mountoptions = "noatime"
    needsmtab = False
    parted_type = parted.PARTITION_NORMAL
    parted_flags = []
    label = "ARCHIVE"

    def setFileSystem(self, filesystem):
        supportedFS = {"fat32":yali4.filesystem.get_filesystem("fat32"),
                       "ext4" :yali4.filesystem.get_filesystem("ext4"),
                       "ext3" :yali4.filesystem.get_filesystem("ext3"),
                       "ntfs" :yali4.filesystem.get_filesystem("ntfs")}
        if supportedFS.has_key(filesystem):
            self.filesystem = supportedFS[filesystem]

root = RootPartitionType()
home = HomePartitionType()
swap = SwapPartitionType()
archive = ArchivePartitionType()


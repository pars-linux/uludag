# -*- coding: utf-8 -*-
#
# Copyright (C) 2005 - 2007 TUBITAK/UEKAE
# Copyright 2001 - 2004 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# As of 26/02/2007, getLabel methods are (mostly) lifted from Anaconda.

# filesystem.py defines file systems used in YALI. Individual classes
# also define actions, like format...

import os
import resource
import string
import parted
import math

from yali4.exception import *
import yali4.sysutils as sysutils
import yali4.parteddata as parteddata
import yali4.storage

class FSError(YaliError):
    pass

def get_filesystem(name):
    """ Returns filesystem implementation for given filesystem name """
    # Hardcoding available filesystems like this is TOO
    # dirty... should revisit this module (and others using this)
    # later on.
    if name == "ext3":
        return Ext3FileSystem()
    elif name == "swap" or name == "linux-swap":
        return SwapFileSystem()
    elif name == "ntfs":
        return NTFSFileSystem()
    elif name == "reiserfs":
        return ReiserFileSystem()
    elif name == "xfs":
        return XFSFileSystem()
    elif name == "fat32":
        return FatFileSystem()

    return None

class FileSystem:
    """ Abstract fileSystem class for other implementations """
    _name = None
    _filesystems = []
    _implemented = False
    _resizable = False
    _mountoptions = "defaults"
    _fs_type = None  # parted fs type

    def __init__(self):
        self._fs_type = parted.file_system_type_get(self._name)

    def openPartition(self, partition):
        """ Checks if partition exists or not;
            If not,it causes YaliException """
        try:
            fd = os.open(partition.getPath(), os.O_RDONLY)
            return fd
        except OSError, e:
            err = "error opening partition %s: %s" % (partition.getPath(), e)
            raise YaliException, err

    def name(self):
        """ Get file system name """
        return self._name

    def mountOptions(self):
        """ Get default mount options for file system """
        return self._mountoptions

    def getFSType(self):
        """ Get parted filesystem type """
        return self._fs_type

    def getLabel(self, partition):
        """ Read filesystem label and return """
        return None

    def setLabel(self, partition, label):
        """ Set label for filesystem """
        return False

    def labelExists(self, label):
        """ Check label for existence """
        if not yali4.storage.devices:
            yali4.storage.init_devices()

        for dev in yali4.storage.devices:
            for part in dev.getPartitions():
                if label == part.getFSLabel():
                    return True

        return False

    def availableLabel(self, label):
        """ Check if label is available and try to find one if not """
        count = 1
        new_label = label
        while self.labelExists(new_label):
            new_label = "%s%d" % (label, count)
            count += 1
        return new_label

    def preFormat(self, partition):
        """ Necessary checks before formatting """
        e = ""
        if not self.isImplemented():
            e = "%s file system is not fully implemented." %(self.name())
        if e:
            raise YaliException, e

        import yali4.gui.context as ctx
        ctx.debugger.log("Format %s: %s" %(partition.getPath(), self.name()))

    def setImplemented(self, bool):
        """ Set if file system is implemented """
        self._implemented = bool

    def isImplemented(self):
        """ Check if filesystem is implemented """
        return self._implemented

    def setResizable(self, bool):
        """ Set if filesystem is resizable """
        self._resizable = bool

    def isResizable(self):
        """ Check if filesystem is resizable """
        return self._resizable

class Ext3FileSystem(FileSystem):
    """ Implementation of ext3 file system """

    _name = "ext3"
    _mountoptions = "defaults,user_xattr"

    def __init__(self):
        FileSystem.__init__(self)
        self.setImplemented(True)
        self.setResizable(True)

    def format(self, partition):
        """ Format the given partition """
        self.preFormat(partition)

        cmd_path = sysutils.find_executable("mke2fs")
        if not cmd_path:
            cmd_path = sysutils.find_executable("mkfs.ext3")

        if not cmd_path:
            e = "Command not found to format %s filesystem" %(self.name())
            raise FSError, e

        # bug 5616: ~100MB reserved-blocks-percentage
        reserved_percentage = int(math.ceil(100.0 * 100.0 / partition.getMB()))

        # Use hashed b-trees to speed up lookups in large directories
        cmd = "%s -O dir_index -j -m %d %s" %(cmd_path,
                                              reserved_percentage,
                                              partition.getPath())

        p = os.popen(cmd)
        o = p.readlines()
        if p.close():
            raise YaliException, "ext3 format failed: %s" % partition.getPath()

        # for Disabling Lengthy Boot-Time Checks
        self.tune2fs(partition)

    def tune2fs(self, partition):
        """ Runs tune2fs for given partition """
        cmd_path = sysutils.find_executable("tune2fs")
        if not cmd_path:
            e = "Command not found to tune the filesystem"
            raise FSError, e

        # Disable mount count and use 6 month interval to fsck'ing disks at boot
        cmd = "%s -c 0 -i 6m %s" % (cmd_path, partition.getPath())

        p = os.popen(cmd)
        o = p.readlines()
        if p.close():
            raise YaliException, "tune2fs tuning failed: %s" % partition.getPath()

    def minResizeMB(self, partition):
        """ Get minimum resize size (mb) for given partition """
        cmd_path = sysutils.find_executable("dumpe2fs")

        if not cmd_path:
            e = "Command not found to get information about %s" %(partition)
            raise FSError, e 

        lines = os.popen("%s -h %s" % (cmd_path, partition.getPath())).readlines()

        total_blocks = long(filter(lambda line: line.startswith('Block count'), lines)[0].split(':')[1].strip('\n').strip(' '))
        free_blocks  = long(filter(lambda line: line.startswith('Free blocks'), lines)[0].split(':')[1].strip('\n').strip(' '))
        block_size   = long(filter(lambda line: line.startswith('Block size'), lines)[0].split(':')[1].strip('\n').strip(' '))

        return (((total_blocks - free_blocks) * block_size) / parteddata.MEGABYTE) + 150

    def resize(self, size_mb, partition):
        """ Resize given partition as given size """
        if size_mb < self.minResizeMB(partition):
            return False

        cmd_path = sysutils.find_executable("resize2fs")

        if not cmd_path:
            e = "Command not found to format %s filesystem" %(self.name())
            raise FSError, e 

        cmd = "%s %s %sM" % (cmd_path, partition.getPath(), str(size_mb)) 

        try:
            p = os.popen(cmd)
            p.close()
        except:
            return False
        return True

    def getLabel(self, partition):
        return sysutils.e2fslabel(partition.getPath())

    def setLabel(self, partition, label):
        label = self.availableLabel(label)
        cmd_path = sysutils.find_executable("e2label")
        cmd = "%s %s %s" % (cmd_path, partition.getPath(), label)
        try:
            p = os.popen(cmd)
            p.close()
        except:
            return False
        return True

##
# reiserfs
class ReiserFileSystem(FileSystem):

    _name = "reiserfs"

    def __init__(self):
        FileSystem.__init__(self)
        self.setImplemented(True)

    def format(self, partition):
        self.preFormat(partition)

        cmd_path = sysutils.find_executable("mkreiserfs")

        if not cmd_path:
            e = "Command not found to format %s filesystem" %(self.name())
            raise FSError, e

        cmd = "%s  %s" %(cmd_path, partition.getPath())

        p = os.popen(cmd, "w")
        p.write("y\n")
        if p.close():
            raise YaliException, "reiserfs format failed: %s" % partition.getPath()


    def getLabel(self, partition):
        label = None
        fd = self.openPartition(partition)

        # valid block sizes in reiserfs are 512 - 8192, powers of 2
        # we put 4096 first, since it's the default
        # reiserfs superblock occupies either the 2nd or 16th block
        for blksize in (4096, 512, 1024, 2048, 8192):
            for start in (blksize, (blksize*16)):
                try:
                    os.lseek(fd, start, 0)
                    # read 120 bytes to get s_magic and s_label
                    buf = os.read(fd, 120)

                    # see if this block is the superblock
                    # this reads reiserfs_super_block_v1.s_magic as defined
                    # in include/reiserfs_fs.h in the reiserfsprogs source
                    m = string.rstrip(buf[52:61], "\0x00")
                    if m in ["ReIsErFs", "ReIsEr2Fs", "ReIsEr3Fs"]:
                        # this reads reiserfs_super_block.s_label as
                        # defined in include/reiserfs_fs.h
                        label = string.rstrip(buf[100:116], "\0x00")
                        os.close(fd)
                        return label
                except OSError, e:
                    # [Error 22] probably means we're trying to read an
                    # extended partition. 
                    e = "error reading reiserfs label on %s: %s" %(partition.getPath(), e)
                    raise YaliException, e

        os.close(fd)
        return label

    def setLabel(self, partition, label):
        label = self.availableLabel(label)
        cmd_path = sysutils.find_executable("reiserfstune")
        cmd = "%s --label %s %s" % (cmd_path, label, partition.getPath())
        try:
            p = os.popen(cmd)
            p.close()
        except:
            return False
        return True

##
# xfs
class XFSFileSystem(FileSystem):

    _name = "xfs"

    def __init__(self):
        FileSystem.__init__(self)
        self.setImplemented(True)

    def format(self, partition):
        self.preFormat(partition)

        cmd_path = sysutils.find_executable("mkfs.xfs")

        if not cmd_path:
            e = "Command not found to format %s filesystem" %(self.name())
            raise FSError, e

        cmd = "%s -f %s" %(cmd_path, partition.getPath())

        p = os.popen(cmd)
        if p.close():
            raise YaliException, "%s format failed: %s" % (self.name(), partition.getPath())

    def getLabel(self, partition):
        label = None
        fd = self.openPartition(partition)
        try:
            buf = os.read(fd, 128)
            os.close(fd)
        except OSError, e:
            e = "error reading xfs label on %s: %s" %(partition.getPath(), e)
            raise YaliException, e

        if len(buf) == 128 and buf[0:4] == "XFSB":
            label = string.rstrip(buf[108:120],"\0x00")

        return label

    def setLabel(self, partition, label):
        label = self.availableLabel(label)
        cmd_path = sysutils.find_executable("xfs_db")
        cmd = "%s -x -c \"label %s\" %s" % (cmd_path, label, partition.getPath())
        try:
            p = os.popen(cmd)
            p.close()
        except:
            return False
        return True


##
# linux-swap
class SwapFileSystem(FileSystem):

    _name = "linux-swap"

    def __init__(self):
        FileSystem.__init__(self)
        self.setImplemented(True)

        # override name: system wants "swap" whereas parted needs
        # linux-swap
        self._name = "swap"

    def format(self, partition):
        self.preFormat(partition)

        cmd_path = sysutils.find_executable("mkswap")
        cmd = "%s %s" %(cmd_path, partition.getPath())

        if not cmd_path:
            e = "Command not found to format %s filesystem" %(self.name())
            raise FSError, e

        p = os.popen(cmd)
        o = p.readlines()
        if p.close():
            raise YaliException, "swap format failed: %s" % partition.getPath()


    def getLabel(self, partition):
        label = None
        fd = self.openPartition(partition)

        pagesize = resource.getpagesize()
        try:
            buf = os.read(fd, pagesize)
            os.close(fd)
        except OSError, e:
            e = "error reading swap label on %s: %s" %(partition.getPath(), e)
            raise YaliException, e

        if ((len(buf) == pagesize) and (buf[pagesize - 10:] == "SWAPSPACE2")):
            label = string.rstrip(buf[1052:1068], "\0x00")
        return label

    def setLabel(self, partition, label):
        label = self.availableLabel(label)
        cmd_path = sysutils.find_executable("mkswap")
        cmd = "%s -v1 -L %s %s" % (cmd_path, label, partition.getPath())
        try:
            p = os.popen(cmd)
            p.close()
        except:
            return False
        return True


##
# ntfs
class NTFSFileSystem(FileSystem):

    _name = "ntfs"

    def __init__(self):
        FileSystem.__init__(self)

        self.setResizable(True)

    def check_resize(self, size_mb, partition):
        #don't do anything, just check
        cmd = "/usr/sbin/ntfsresize -n -f -s %dM %s" %(size_mb, partition.getPath())

        p = os.popen(cmd)
        if p.close():
            return False
        return True


    def resize(self, size_mb, partition):

        if size_mb < self.minResizeMB(partition):
            return False

        cmd = "/usr/sbin/ntfsresize -f -s %dM %s" %(size_mb, partition.getPath())

        try:
            p = os.popen(cmd, "w")
            p.write("y\n")
            p.close()
        except:
            return False

        return True


    def minResizeMB(self, partition):

        cmd = "/usr/sbin/ntfsresize -f -i %s" % partition.getPath()
        lines = os.popen(cmd).readlines()

        MB = parteddata.MEGABYTE
        _min = 0
        for l in lines:
            if l.startswith("You might resize"):
                _min = int(l.split()[4]) / MB + 140

        return _min

##
# fat file system
class FatFileSystem(FileSystem):

    _name = "fat32"
    _mountoptions = "quiet,shortname=mixed,dmask=007,fmask=117,utf8,gid=6"

    def __init__(self):
        FileSystem.__init__(self)
        self.setImplemented(True)

        # I will do it later
        self.setResizable(False)

    def format(self, partition):
        self.preFormat(partition)

        cmd_path = sysutils.find_executable("mkfs.vfat")

        if not cmd_path:
            e = "Command not found to format %s filesystem" %(self.name())
            raise FSError, e

        cmd = "%s %s" %(cmd_path,partition.getPath())

        p = os.popen(cmd)
        o = p.readlines()
        if p.close():
            raise YaliException, "fat32 format failed: %s" % partition.getPath()

    def getLabel(self, partition):
        cmd_path = sysutils.find_executable("dosfslabel")
        if not cmd_path:
            e = "Command not found to get label for %s filesystem" %(self.name())
            raise FSError, e 

        cmd = "%s %s" % (cmd_path, partition.getPath())
        p = os.popen(cmd)
        label = p.read()
        p.close()
        if not label == '':
            return label.strip(' \n')
        return False

    def setLabel(self, partition, label):
        label = self.availableLabel(label)
        cmd_path = sysutils.find_executable("dosfslabel")
        cmd = "%s %s %s" % (cmd_path, partition.getPath(), label)
        try:
            p = os.popen(cmd)
            p.close()
        except:
            return False
        return True



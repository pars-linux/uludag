# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009 TUBITAK/UEKAE
# Copyright 2001-2008 Red Hat, Inc.
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

# we need i18n
import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

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
    knownFS = {"ext3":      Ext3FileSystem,
               "ext4":      Ext4FileSystem,
               "swap":      SwapFileSystem,
               "linux-swap":SwapFileSystem,
               "ntfs":      NTFSFileSystem,
               "reiserfs":  ReiserFileSystem,
               "xfs":       XFSFileSystem,
               "fat32":     FatFileSystem}

    if knownFS.has_key(name):
        return knownFS[name]()

    return None

def getLabel(partition):
    if not os.path.exists("/dev/disk/by-label"):
        return None
    base = os.walk("/dev/disk/by-label/").next()
    path = partition.getPath()
    for part in base[2]:
        if os.path.realpath("%s%s" % (base[0],part)) == path:
            return part
    return None

def requires(command):
    cmd_path = sysutils.find_executable(command)
    if not cmd_path:
        raise FSError, "Command not found: %s " % command
    return cmd_path

class FileSystem:
    """ Abstract fileSystem class for other implementations """
    _name = None
    _sysname = None
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
        cmd_path = requires("e2label")
        cmd = "%s %s" % (cmd_path, partition.getPath())
        import yali4.gui.context as ctx
        ctx.debugger.log("Running CMD: %s" % cmd)
        try:
            p = os.popen(cmd)
            label = p.read()
            p.close()
        except Exception, e:
            ctx.debugger.log("Failed while getting label for partition %s : %s" % (partition.getPath(), e))
            return False
        return label.strip()

    def setLabel(self, partition, label):
        label = self.availableLabel(label)
        cmd_path = requires("e2label")
        import yali4.gui.context as ctx
        cmd = "%s %s %s" % (cmd_path, partition.getPath(), label)
        ctx.debugger.log("Running CMD: %s" % cmd)
        try:
            p = os.popen(cmd)
            p.close()
            res = sysutils.execClear("e2label",
                                    [partition.getPath(), label],
                                    stdout="/tmp/label.log",
                                    stderr="/tmp/label.log")
        except Exception, e:
            ctx.debugger.log("Failed while setting label for partition %s : %s" % (partition.getPath(), e))
            return False
        return label

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
        if not self.isImplemented():
            raise YaliException, "%s file system is not fully implemented." % (self.name())

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

    def preResize(self, partition):
        """ Routine operations before resizing """
        cmd_path = requires("e2fsck")

        res = sysutils.execClear("e2fsck",
                                ["-f", "-p", "-C", "0", partition.getPath()],
                                stdout="/tmp/resize.log",
                                stderr="/tmp/resize.log")

        # FIXME if res == 2 means filesystem fixed but needs reboot !
        if res >= 4:
            raise FSError, "FSCheck failed on %s" % (partition.getPath())

        return True

    def format(self, partition):
        """ Format the given partition """
        self.preFormat(partition)
        cmd_path = requires("mkfs.%s" % self.name())

        # bug 5616: ~100MB reserved-blocks-percentage
        reserved_percentage = int(math.ceil(100.0 * 100.0 / partition.getMB()))

        # Use hashed b-trees to speed up lookups in large directories
        cmd = "%s -O dir_index -j -m %d %s" %(cmd_path,
                                              reserved_percentage,
                                              partition.getPath())

        p = os.popen(cmd)
        o = p.readlines()
        if p.close():
            raise YaliException, "%s format failed: %s" % (self.name(), partition.getPath())

        # for Disabling Lengthy Boot-Time Checks
        self.tune2fs(partition)

    def tune2fs(self, partition):
        """ Runs tune2fs for given partition """
        cmd_path = requires("tune2fs")

        # Disable mount count and use 6 month interval to fsck'ing disks at boot
        cmd = "%s -c 0 -i 6m %s" % (cmd_path, partition.getPath())

        p = os.popen(cmd)
        o = p.readlines()
        if p.close():
            raise YaliException, "tune2fs tuning failed: %s" % partition.getPath()

    def minResizeMB(self, partition):
        """ Get minimum resize size (mb) for given partition """
        cmd_path = requires("dumpe2fs")

        def capture(lines, param):
            return long(filter(lambda line: line.startswith(param), lines)[0].split(':')[1].strip('\n').strip(' '))

        lines = os.popen("%s -h %s" % (cmd_path, partition.getPath())).readlines()

        try:
            total_blocks = capture(lines, 'Block count')
            free_blocks  = capture(lines, 'Free blocks')
            block_size   = capture(lines, 'Block size')
            return (((total_blocks - free_blocks) * block_size) / parteddata.MEGABYTE) + 150
        except Exception, e:
            ctx.debugger.log("Failed while getting minimum size for partition %s : %s" % (partition.getPath(), e))
            return 0

    def resize(self, size_mb, partition):
        """ Resize given partition as given size """
        if size_mb < self.minResizeMB(partition):
            return False

        cmd_path = requires("resize2fs")

        res = sysutils.execClear("resize2fs",
                                ["-f", partition.getPath(), "%sM" %(size_mb)],
                                stdout="/tmp/resize.log",
                                stderr="/tmp/resize.log")
        if res:
            raise FSError, "Resize failed on %s" % (partition.getPath())
        return True

class Ext4FileSystem(FileSystem):
    """ Implementation of ext4 file system """

    _name = "ext4"
    _mountoptions = "defaults,user_xattr"

    def __init__(self):
        FileSystem.__init__(self)
        self.setImplemented(True)
        self.setResizable(True)

class Ext3FileSystem(FileSystem):
    """ Implementation of ext3 file system """

    _name = "ext3"
    _mountoptions = "defaults,user_xattr"

    def __init__(self):
        FileSystem.__init__(self)
        self.setImplemented(True)
        self.setResizable(True)

##
# reiserfs
class ReiserFileSystem(FileSystem):

    _name = "reiserfs"

    def __init__(self):
        FileSystem.__init__(self)
        self.setImplemented(True)

    def format(self, partition):
        self.preFormat(partition)

        cmd_path = requires("mkreiserfs")
        cmd = "%s  %s" %(cmd_path, partition.getPath())

        p = os.popen(cmd, "w")
        p.write("y\n")
        if p.close():
            raise YaliException, "reiserfs format failed: %s" % partition.getPath()

    def setLabel(self, partition, label):
        label = self.availableLabel(label)
        cmd_path = requires("reiserfstune")
        cmd = "%s --label %s %s" % (cmd_path, label, partition.getPath())
        try:
            p = os.popen(cmd)
            p.close()
        except Exception, e:
            ctx.debugger.log("Failed while setting label for partition %s : %s" % (partition.getPath(), e))
            return False
        return label

    def getLabel(self, partition):
        getLabel(partition)

##
# xfs
class XFSFileSystem(FileSystem):

    _name = "xfs"

    def __init__(self):
        FileSystem.__init__(self)
        self.setImplemented(True)

    def format(self, partition):
        self.preFormat(partition)
        cmd_path = requires("mkfs.xfs")
        cmd = "%s -f %s" %(cmd_path, partition.getPath())

        p = os.popen(cmd)
        if p.close():
            raise YaliException, "%s format failed: %s" % (self.name(), partition.getPath())

    def setLabel(self, partition, label):
        label = self.availableLabel(label)
        cmd_path = requires("xfs_admin")
        cmd = "%s -L %s %s" % (cmd_path, label, partition.getPath())
        try:
            p = os.popen(cmd)
            p.close()
        except Exception, e:
            ctx.debugger.log("Failed while setting label for partition %s : %s" % (partition.getPath(), e))
            return False
        return label

    def getLabel(self, partition):
        getLabel(partition)

##
# linux-swap
class SwapFileSystem(FileSystem):

    _name = "linux-swap"
    _sysname = "swap"

    def __init__(self):
        FileSystem.__init__(self)
        self.setImplemented(True)

        # override name: system wants "swap" whereas parted needs
        # linux-swap
        self._name = "swap"

    def format(self, partition):
        self.preFormat(partition)
        cmd_path = requires("mkswap")
        cmd = "%s %s" %(cmd_path, partition.getPath())

        p = os.popen(cmd)
        o = p.readlines()
        if p.close():
            raise YaliException, "swap format failed: %s" % partition.getPath()

        # Swap on
        sysutils.swap_on(partition.getPath())

    def getLabel(self, partition):
        label = None
        fd = self.openPartition(partition)

        pagesize = resource.getpagesize()
        try:
            buf = os.read(fd, pagesize)
            os.close(fd)
        except Exception, e:
            ctx.debugger.log("Failed while getting label for partition %s : %s" % (partition.getPath(), e))
            return False

        if ((len(buf) == pagesize) and (buf[pagesize - 10:] == "SWAPSPACE2")):
            label = string.rstrip(buf[1052:1068], "\0x00")
        return label

    def setLabel(self, partition, label):
        label = self.availableLabel(label)
        cmd_path = requires("mkswap")
        cmd = "%s -v1 -L %s %s" % (cmd_path, label, partition.getPath())
        try:
            p = os.popen(cmd)
            p.close()
        except Exception, e:
            ctx.debugger.log("Failed while setting label for partition %s : %s" % (partition.getPath(), e))
            return False
        return label


##
# ntfs
class NTFSFileSystem(FileSystem):

    _name = "ntfs"
    _sysname = "ntfs-3g"
    _mountoptions = "dmask=007,fmask=117,locale=tr_TR.UTF-8,gid=6"

    def __init__(self):
        FileSystem.__init__(self)
        self.setResizable(True)
        self.setImplemented(True)

    #FIXME#
    def check_resize(self, size_mb, partition):
        # don't do anything, just check
        cmd = "/usr/sbin/ntfsresize -n -f -s %dM %s" %(size_mb, partition.getPath())
        p = os.popen(cmd)
        if p.close():
            return False
        return True

    def resize(self, size_mb, partition):
        if size_mb < self.minResizeMB(partition):
            return False

        if not self.check_resize(size_mb, partition):
            raise FSError, _("Partition is not ready for resizing. Check it before installation.")

        p = os.pipe()
        os.write(p[1], "y\n")
        os.close(p[1])

        cmd_path = requires("ntfsresize")
        res = sysutils.execClear(cmd_path,
                                ["-f","-s", "%sM" % (size_mb), partition.getPath()],
                                stdin = p[0],
                                stdout = "/tmp/resize.log",
                                stderr = "/tmp/resize.log")
        if res:
            raise FSError, "Resize failed on %s " % (partition.getPath())

        return True

    def getLabel(self, partition):
        getLabel(partition)

    def setLabel(self, partition, label):
        label = self.availableLabel(label)
        cmd_path = requires("ntfslabel")
        cmd = "%s %s %s" % (cmd_path, partition.getPath(), label)
        try:
            p = os.popen(cmd)
            p.close()
        except Exception, e:
            ctx.debugger.log("Failed while setting label for partition %s : %s" % (partition.getPath(), e))
            return False
        return label

    def format(self, partition):
        self.preFormat(partition)
        cmd_path = requires("mkfs.ntfs")
        cmd = "%s -f %s" % (cmd_path,partition.getPath())

        p = os.popen(cmd)
        o = p.readlines()
        if p.close():
            raise YaliException, "Ntfs format failed: %s" % partition.getPath()

    #FIXME#
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
    _sysname = "vfat"
    _mountoptions = "quiet,shortname=mixed,dmask=007,fmask=117,utf8,gid=6"

    def __init__(self):
        FileSystem.__init__(self)
        self.setImplemented(True)

        # FIXME I will do it later
        self.setResizable(False)

    def format(self, partition):
        self.preFormat(partition)
        cmd_path = requires("mkfs.vfat")
        cmd = "%s %s" %(cmd_path,partition.getPath())
        p = os.popen(cmd)
        o = p.readlines()
        if p.close():
            raise YaliException, "vfat format failed: %s" % partition.getPath()

    def getLabel(self, partition):
        getLabel(partition)

    def setLabel(self, partition, label):
        label = self.availableLabel(label)
        cmd_path = requires("dosfslabel")
        cmd = "%s %s %s" % (cmd_path, partition.getPath(), label)
        try:
            p = os.popen(cmd)
            p.close()
        except Exception, e:
            ctx.debugger.log("Failed while setting label for partition %s : %s" % (partition.getPath(), e))
            return False
        return label


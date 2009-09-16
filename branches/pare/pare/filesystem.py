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

import os
import resource
import string
import parted
import math

from pare.errors import PareError, FileSystemError
import pare.utils.sysutils as sysutils
import logging
log = logging.getLogger("pare")


def getFilesystem(name):
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
    _type = None  # parted fs type

    def __init__(self, device):
        self._type = parted.filesystem._ped.file_system_type_get(self.name)
        self.device = device

    def openPartition(self, partition):
        """ Checks if partition exists or not;
            If not,it causes PareError """
        try:
            fd = os.open(partition.path, os.O_RDONLY)
            return fd
        except OSError, e:
            err = "error opening partition %s: %s" % (partition.path, e)
            raise PareError, err

    def mount(self):
        #FIXME:Check how yali mount filesystems
        pass

    def umount(self):
        #FIXME:Check how yali umount filesystems
        pass

    def setup(self):
        self.mount()

    def teardown(self):
        self.umount()

    @property
    def exists(self):
        return self.status

    @property
    def status(self):
        if self.device.path in pare.syblock.detec_procMounts():
            return True
        else:
            return False

    @property
    def name(self):
        """ Get file system name """
        return self._name

    @property
    def mountOptions(self):
        """ Get default mount options for file system """
        return self._mountoptions

    @property
    def fileSystemType(self):
        """ Get parted file system type """
        return self._type

    def getLabel(self, partition):
        """ Read file system label and return """
        cmd_path = requires("e2label")
        cmd = "%s %s" % (cmd_path, partition.path)
        label = sysutils.run(cmd, capture=True)
        if not label:
            return False
        return label.strip()

    def setLabel(self, partition, label):
        label = self.availableLabel(label)
        cmd_path = requires("e2label")
        cmd = "%s %s %s" % (cmd_path, partition.path, label)
        if not sysutils.run(cmd):
            return False
        # Check label consistency
        if not self.getLabel(partition) == label:
            return False
        return label

    def islabelExists(self, label):
        """ Check label for existence """
        if not pare.storage.devices:
            pare.storage.init_devices()

        for dev in pare.storage.devices:
            for part in dev.partitions:
                if label == part.label:
                    return True
        return False

    def availableLabel(self, label):
        """ Check if label is available and try to find one if not """
        count = 1
        new_label = label
        while self.islabelExists(new_label):
            new_label = "%s%d" % (label, count)
            count += 1
        return new_label

    def preFormat(self, partition):
        """ Necessary checks before formatting """
        if not self.isImplemented():
            raise PareError, "%s file system is not fully implemented." % (self.name)


        log.info("Format %s: %s" %(partition.path, self.name))

    def _setImplemented(self, bool):
        """ Set if file system is implemented """
        self._implemented = bool


    def _getImplemented(self):
        """ Check if filesystem is implemented """
        return self._implemented

    implemented = property(lambda p: p._getImplemented(), lambda p,f: p._setImplemented(f))

    def _setResizable(self, bool):
        """ Set if filesystem is resizable """
        self._resizable = bool


    def _getResizable(self):
        """ Check if filesystem is resizable """
        return self._resizable

    resizable = property(lambda p: p._getResizable(), lambda p,f: p._setResizable(f))

    def preResize(self, partition):
        """ Routine operations before resizing """
        cmd_path = requires("e2fsck")

        res = sysutils.execClear("e2fsck",
                                ["-f", "-p", "-C", "0", partition],
                                stdout="/tmp/resize.log",
                                stderr="/tmp/resize.log")

        if res == 2:
            raise FileSystemError, _("""FSCheck found some problems on partition %s and fixed them. \
                                You should restart the machine before starting the installation process !""" % (partition.getPath()))
        elif res > 2:
            raise FileSystemError, _("FSCheck failed on %s" % (partition))

        return True

    def format(self, partition):
        """ Format the given partition """
        self.preFormat(partition)

        cmd_path = requires("mkfs.%s" % self.name)

        # bug 5616: ~100MB reserved-blocks-percentage
        reserved_percentage = int(math.ceil(100.0 * 100.0 / partition.size))

        # Use hashed b-trees to speed up lookups in large directories
        cmd = "%s -O dir_index -q -j -m %d %s" % (cmd_path,
                                                  reserved_percentage,
                                                  partition.path)

        res = sysutils.run(cmd)
        if not res:
            raise PareError, "%s format failed: %s" % (self.name, partition.path)

        # for Disabling Lengthy Boot-Time Checks
        self.tune2fs(partition)

    def tune2fs(self, partition):
        """ Runs tune2fs for given partition """
        cmd_path = requires("tune2fs")
        # Disable mount count and use 6 month interval to fsck'ing disks at boot
        cmd = "%s -c 0 -i 6m %s" % (cmd_path, partition.path)
        res = sysutils.run(cmd)
        if not res:
            raise PareError, "tune2fs tuning failed: %s" % partition.path

    def minResizeMB(self, partition):
        """ Get minimum resize size (mb) for given partition """
        cmd_path = requires("dumpe2fs")

        def capture(lines, param):
            return long(filter(lambda line: line.startswith(param), lines)[0].split(':')[1].strip('\n').strip(' '))

        lines = os.popen("%s -h %s" % (cmd_path, partition)).readlines()

        try:
            total_blocks = capture(lines, 'Block count')
            free_blocks  = capture(lines, 'Free blocks')
            block_size   = capture(lines, 'Block size')
            return (((total_blocks - free_blocks) * block_size) / parteddata.MEGABYTE) + 140
        except Exception:
            return 0

    def resize(self, size, partition):
        """ Resize given partition as given size """
        if size < self.minResizeMB(partition):
            return False

        cmd_path = requires("resize2fs")

        # Check before resize
        self.preResize(partition)

        res = sysutils.run("resize2fs",[partition, "%sM" %(size)])
        if not res:
            raise FileSystemError, "Resize failed on %s" % (partition)
        return True

class Ext4FileSystem(FileSystem):
    """ Implementation of ext4 file system """

    _name = "ext4"
    _mountoptions = "defaults,user_xattr"

    def __init__(self):
        FileSystem.__init__(self)
        self.implemented = True
        self.resizable = True

class Ext3FileSystem(FileSystem):
    """ Implementation of ext3 file system """

    _name = "ext3"
    _mountoptions = "defaults,user_xattr"

    def __init__(self):
        FileSystem.__init__(self)
        self.implemented = True
        self.resizable = True


class ReiserFileSystem(FileSystem):

    _name = "reiserfs"

    def __init__(self):
        FileSystem.__init__(self)
        self.implemented = True


    def format(self, partition):
        self.preFormat(partition)

        cmd_path = requires("mkreiserfs")
        cmd = "%s %s" % (cmd_path, partition.path)

        p = os.popen(cmd, "w")
        p.write("y\n")
        if p.close():
            raise PareError, "reiserfs format failed: %s" % partition.path

    def setLabel(self, partition, label):
        label = self.availableLabel(label)
        cmd_path = requires("reiserfstune")
        cmd = "%s --label %s %s" % (cmd_path, label, partition.path)
        if not sysutils.run(cmd):
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
        self.implemented = True

    def format(self, partition):
        self.preFormat(partition)
        cmd_path = requires("mkfs.xfs")
        cmd = "%s -f %s" %(cmd_path, partition.path)
        res = sysutils.run(cmd)
        if not res:
            raise PareError, "%s format failed: %s" % (self.name, partition.path)

    def setLabel(self, partition, label):
        label = self.availableLabel(label)
        cmd_path = requires("xfs_admin")
        cmd = "%s -L %s %s" % (cmd_path, label, partition.path)
        if not sysutils.run(cmd):
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
        self.implemented = True

        # override name: system wants "swap" whereas parted needs linux-swap
        self._name = "swap"

    def format(self, partition):
        self.preFormat(partition)
        cmd_path = requires("mkswap")
        cmd = "%s %s" %(cmd_path, partition.path)
        res = sysutils.run(cmd)
        if not res:
            raise PareError, "Swap format failed: %s" % partition.path


    def getLabel(self, partition):
        label = None
        fd = self.openPartition(partition)

        pagesize = resource.getpagesize()
        try:
            buf = os.read(fd, pagesize)
            os.close(fd)
        except:
            return False

        if ((len(buf) == pagesize) and (buf[pagesize - 10:] == "SWAPSPACE2")):
            label = string.rstrip(buf[1052:1068], "\0x00")
        return label

    def setLabel(self, partition, label):
        label = self.availableLabel(label)
        cmd_path = requires("mkswap")
        cmd = "%s -v1 -L %s %s" % (cmd_path, label, partition.path)
        if not sysutils.run(cmd):
            return False

        # Swap on
        sysutils.swap_on(partition.path)

        return label

##
# ntfs
class NTFSFileSystem(FileSystem):

    _name = "ntfs"
    _sysname = "ntfs-3g"
    _mountoptions = "dmask=007,fmask=117,locale=tr_TR.UTF-8,gid=6"

    def __init__(self):
        FileSystem.__init__(self)
        self.implemented = True
        self.resizable = True

    def check_resize(self, size, partition):
        # don't do anything, just check
        cmd_path = requires("ntfsresize")
        cmd = "%s -n -f -s %dM %s" % (cmd_path, size, partition.path)
        return sysutils.run(cmd)

    def resize(self, size, partition):
        if size_mb < self.minResizeMB(partition):
            return False

        if not self.check_resize(size_mb, partition):
            raise FileSystemError, _("Partition is not ready for resizing. Check it before installation.")

        p = os.pipe()
        os.write(p[1], "y\n")
        os.close(p[1])

        cmd_path = requires("ntfsresize")
        res = sysutils.execClear(cmd_path,
                                ["-f","-s", "%sM" % (size), partition.path],
                                stdin = p[0],
                                stdout = "/tmp/resize.log",
                                stderr = "/tmp/resize.log")
        if res:
            raise FileSystemError, "Resize failed on %s " % (partition.getPath())

        return True

    def getLabel(self, partition):
        getLabel(partition)

    def setLabel(self, partition, label):
        label = self.availableLabel(label)
        cmd_path = requires("ntfslabel")
        cmd = "%s %s %s" % (cmd_path, partition.path, label)
        if not sysutils.run(cmd):
            return False
        return label

    def format(self, partition):
        self.preFormat(partition)
        cmd_path = requires("mkfs.ntfs")
        cmd = "%s -f %s" % (cmd_path,partition.path)
        res = sysutils.run(cmd)
        if not res:
            raise PareError, "Ntfs format failed: %s" % partition.path

    def minResizeMB(self, partition):
        cmd_path = requires("ntfsresize")
        cmd = "%s -f -i %s" % (cmd_path, partition.path )
        lines = os.popen(cmd).readlines()
        _min = 0
        for l in lines:
            if l.startswith("You might resize"):
                _min = int(l.split()[4]) / parteddata.MEGABYTE + 140

        return _min

##
# fat file system
class FatFileSystem(FileSystem):

    _name = "fat32"
    _sysname = "vfat"
    _mountoptions = "quiet,shortname=mixed,dmask=007,fmask=117,utf8,gid=6"

    def __init__(self):
        FileSystem.__init__(self)
        self.implemented = True

        # FIXME I will do it later
        self.setResizable(False)

    def format(self, partition):
        self.preFormat(partition)
        cmd_path = requires("mkfs.vfat")
        cmd = "%s %s" %(cmd_path,partition.path)
        res = sysutils.run(cmd)
        if not res:
            raise PareError, "vfat format failed: %s" % partition.path

    def getLabel(self, partition):
        getLabel(partition)

    def setLabel(self, partition, label):
        label = self.availableLabel(label)
        cmd_path = requires("dosfslabel")
        cmd = "%s %s %s" % (cmd_path, partition.path, label)
        if not sysutils.run(cmd):
            return False
        return label


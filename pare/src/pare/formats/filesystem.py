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
#import tempfile
import logging
log = logging.getLogger("pare")

from pare.errors import *


from pare.sysutils import notify_kernel, get_sysfs_path_by_name
from pare.utils.dm import dm_node_from_name


import gettext
_ = lambda x: gettext.ldgettext("pare", x)

        
    

class StorageFormat(object):
    """Generic Storage Format"""

    _type = None
    partedFlag = None
    _resizable = False
    _bootable = False
    _migratable = False
    _maxSize = 0
    _minSize = 0
    _dump = False
    _check = False

    def __init__(self, *args, **kwargs):
        """
        device -- path to the underlying device (To be easy for resize or format arg list) 
        exists -- whether this is existing format
        uuid -- format's UUID 
        """
        self._device = kwargs.get("device")
        self.uuid = kwargs.get("uuid")
        self.exists = kwargs.get("exists")
        self._migrate = False
        
    def _setDevice(self, dev):
        if dev and not dev.starwith("/") :
            raise ValueError("device must be fully qualified path")
        
        self._device = dev
    
    def _getDevice(self):
        return self._device
    
    device = property(lambda p: p._getDevice(), lambda p:p._setDevice)
    
    @property
    def type(self):
        return self._type

    @property
    def resizable(self):
        return self._resizable

    @property
    def bootable(self):
        self._bootable

    @property
    def migratable(self):
        return self._migratable

    @property
    def migrate(self):
        return self._migrate
    @property
    def dump(self):
        return self._dump

    @property
    def check(self):
        return self._check

    @property
    def minSize(self):
        return self._minSize

    @property
    def maxSize(self):
        return self._maxSize

    def create(self, *args, **kwargs):
        dev = kwargs.get("device")
        
        if not os.path.exists(dev):
            raise FormatCreateError("invalid device")
        else:
            self.device = dev
    
    def destroy(self):
        #FIXME
        #Anaconda uses zeroing begining and end of the device for 
        #any meta data wiping in the future
        pass
    
    def notifyKernel(self):
        if not self.device:
            return 
        
        if self.device.startwith("/dev/mapper/"):
            try:
                name = dm_node_from_name(os.path.basename(self.device))
            except Exception as e:
                log.warning("failed dm node from device" ,self.device)
                return
        elif self.device:
            name = os.path.basename(self.device)
        
        path = get_sysfs_path_by_name(name)
        
        try:
            notify_kernel(path, action="changed")
        except Exception, e:
            log.warning("failed to notify the kernel change:%s" % e )
                



class FileSystem(StorageFormat):
    _type = "generic"
    _mkfs = ""
    _resizefs = ""
    _labelfs = ""
    _fsck = ""
    _migratefs = ""
    _defaultFormatOptions = []
    _defaultMountOptions = ["defaults"]
    _defaultLabelOptions = []
    _defaultCheckOptions = []
    _defaultMigrateOptions = []
    _migrationTarget = None
    
    def __init__(self, *args, **kwargs):
        """
            mountpoint -- filesystem mountpoint
            mountoptions -- filesystem mount options
            uuid -- filesystem uuid
            label -- filesystem label
            size -- filesystem size(filesytem size doesn't equal device size)
            exists -- if fileystem is already exists
        """
        
        StorageFormat.__init__(self, *args, **kwargs)
        
        self._targetMountpoint = kwargs.get("mountpoint") # target mount point
        self._mountoptions = kwargs.get("mountoptions")
        self._uuid = kwargs.get("uuid")
        self._label = kwargs.get("label")
        self._size = kwargs.get("size")
        self._minSize = None
        self._currentMountpoint = None # current mountpoint when mounted
        
        if self.exists:
            #FIXME - determine actual filesystem size
            self._size =  self._getExistingSize()
        
        self._targetSize = self._size
        
        
    def _setTargetSize(self, newsize):
        """Set target size for filesystem"""
        if not self.exists:
            raise FileSystemError("File System hasnot been created")
        
        if newsize is None:
            self._targetSize = None
            return
        
        if not self.minSize() < newsize < self.maxSize():
            raise ValueError("Invalid target size")
        
        self._targetSize = newsize
        
    def _getSize(self):
        """Get filesytem size"""
        size = self._size
        if self._resizable and self.targetSize != size:
            size = self.targetSize
            
        return size
    
    size = property(lambda p: p._getSize())
        
    def _getTargetSize(self):
        """Get this filesystem target size"""
        return self._targetSize
        
    targetSize = property(lambda p: p._getTargetSize(), lambda p: p._setTargetSize())
        
    def _getTargetSize(self):
        pass
    
    def currentSize(self):
        """File System current actual size"""
        size = 0
        if self.exists :
            size = self._size
            
        return float(size)
        
    def _getExistingSize(self):
        """Determine the size of FileSystem"""
        size = 0
        origMount = self._currentMountpoint
#        tmp = tempfile.mkdtemp(prefix="getsize-", dir="/tmp")
#        self.mount(mountpoint=tmp, options="ro")
#        buf = os.statvfs(tmp)
#        os.rmdir(tmp)
#        self._currentMountpoint = origMount
#        
#        size = (buf.f_frsize * buf.f_blocks) / 1024.0 / 1024.0 
        
        return size
    
    def _getFormatOptions(self, options=None):
        args = []
        if options and isinstance(options, list):
            args.extend(options)
        args.extend(self._defaultFormatOptions)
        args.append(self.device)
        
        return args
    
    @property
    def mkfsCMD(self):
        return self._mkfs
    
    @property
    def resizeCMD(self):
        return self._resizefs
    
    @property
    def labelCMD(self):
        return self._labelfs
    
    @property
    def fsckCMD(self):
        return self._fsck
    
    @property
    def migrateCMD(self):
        return self._migratefs
    
    @property
    def migrationTarget(self):
        return self._migrationTarget
    
    
    def migratable(self):
        return bool(self._migratable and self.migrationTarget())
    
    def _setMigrate(self, migrate):
        if not migrate:
            self._migrate = migrate
            return
        
        if self.migratable() and self.exists:
            self._migrate = migrate
        else:
            raise ValueError("cannot migrate non-migratable filesystem")
    
    migrate = property(lambda p: p._migrate, lambda p: p._setMigrate())
            
    @property
    def defaultFormatOption(self):
        return self._defaultFormatOptions[:]
    
    @property
    def defaultMountOptions(self):
        return self._defaultMountOptions[:]
    
    @property
    def defaultCheckOptions(self):
        return self._defaultCheckOptions[:]
    
    @property
    def defaultLabelOptions(self):
        return self._defaultLabelOptions[:]
    
    @property
    def defaultMigrateOptions(self):
        return self._defaultMigrateOptions[:]
    
    def _getOptions(self):
        options = ",".join(self.defaultMountOptions())
        if self._mountoptions:
            options = self._mountoptions
        return options
    
    def _setOptions(self,options):
        self._mountoptions = options
        
    options = property(lambda p: p._getOptions(), lambda p: p._setOptions())

    @property
    def mountpoint(self):
        return self._targetMountpoint
    
    @property
    def type(self):
        type = self._type
        if self.migrate:
            type = self.migrationTarget()
        return type
    
    def doFormat(self, *args, **kwargs):
        """Create FileSystem
            
            options -- list of options to pass mkfs
        
        """
        
        options = kwargs.get("options")
        
        if self.exists:
            raise FormatCreateError("This filesystem already exists")
            return
        
        if not self.mkfsCMD():
            return
        
        argv = self._getFormatOptions(options)

        try:
            return_code = sysutils.execClear(self.mkfsCMD(), argv, stdout="/dev/tty5", stderr="/dev/tty5")
        except OSError as e:
            raise FormatCreateError(e ,self.device)
        
        if return_code:
            self.exists = True
            self.notifyKernel()
            
    def doMigrate(self):
        if not self.exists:
            raise FileSystemError("Filesystem has not been created")
        
        if not self.migratable() or not self.migrate:
            return
        
        if not os.path.exists(self.device):
            raise FileSystemError("File doesnt exist")
        
        #FIXME:May be check ext2HasJournal?
        
        argv = self.defaultCheckOptions()
        argv.append(self.device)
        
        try:
            return_code = sysutils.execClear(self.migrateCMD(), argv, stdout="/dev/tty5", stderr="/dev/tty5")
        except Exception, e:
            raise FileSystemMigrateErrorystemError("filesystem migration failed %s" % e, self.device)
        
        if return_code:
            self._type = self._migrationTarget
        else:
            raise FileSystemMigrateErrorystemError("filesystem migration failed %s" % e, self.device)
    
    @property    
    def resizeArgs(self):
        argv = [self.device, "%d" % (self.targetSize,)]
        return argv
    
    def doResize(self, *args, **kwargs):
        """Resize the filesystem to the new size"""
        
        if not self.exists:
            raise FileSystemResizeError("FileSystem doesnt exist")
        
        if not self.resizable():
            raise FileSystemResizeError("FileSytem isnt resizable")
        
        if self.targetSize == self.currentSize():
            return
        
        if not self.resizeCMD():
            return
        
        if not os.path.exists(self.device):
            raise FileSystemResizeError("FileSsystem underlying device doesnt exist")
        
        
        
    def _getCheckArgs(self):
        argv = []
        argv.extend(self.defaultCheckOptions())
        argv.append(self.device)
        return argv
    
    def doCheck(self):
        if not self.exists:
            raise FileSystemError("FileSystem hasnt been created")
        
        if not self.fsckCMD():
            return
        
        if not os.path.exists(self.device):
            raise FileSystemError("FileSystem underlying device doesnt exist")
        
        try:
            return_code = sysutils.execClear(self.fsckCMD(), self._getCheckArgs(), stdout="/dev/tty5", stderr="/dev/tty5")
        except Exception, e:
            raise FileSystemError("FileSystem check failed",e)
        
        if not return_code:
            raise FileSystemError("FileSystem check failed")
     
     
    def tearDown(self, *args, **kwargs):
        return self.umount(*args, **kwargs)
    
    def mount(self, *args, **kwargs):
        """
            options -- overrides other self.options params
            mountpoint --overrides other self.mountpoint
            chroot --prefix to apply to mountpoint
        """
        
        options = kwargs.get("options")
        mountpoint = kwargs.get("mountpoint")
        chroot = kwargs.get("chroot")
        
        if not self.exists:
            raise FileSystemError("Filesystem doesnt exist")
        
        if not mountpoint:
            mountpoint =  self._targetMountpoint
            
        if not mountpoint:
            raise FileSystemError("no mountpoint given")
        
        if self.status():
            return
        
        if not os.path.exists(self.device):
            raise FileSystemError("device %s not exists" % self.device )
        
        #FIXME:os.path.join is fubar :) (TEST it)
        mountpoint = os.path.normpath("%s%s" % (chroot, mountpoint))
        
        if not options and isinstance(options, str):
            options = self.options
        
        try:
            return_code = sysutils.mount(source, target, fs, needs_mtab)
        except Exception, e:
            raise FileSystemError("mount failed!", e)
        
        if not return_code:
            raise FileSystemError("mount failed!", e)
        
        self._currentMountpoint =  mountpoint
        
    def umount(self):
        if not self.exists:
            raise FileSystemError("Filesystem has not been created")
        
        if not self._currentMountpoint:
            return 
        
        if not os.path.exists(self._currentMountpoint):
            raise FileSystemError("Mount point doesnt exist")
        try:
            return_code = sysutils.umount(self._currentMountpoint)
        except Exception, e:
            raise FileSystemError("umount failed!", e)
        
        if not return_code:
            FileSystemError("umount failed!", e)
            
        self._currentMountpoint = None
        
        
    def _getLabelArgs(self, label):
        argv = []
        argv.extend(self.defaultLabelOptions())
        argv.extend([self.device, label])
        return argv
    
    @property
    def label(self):
        return self._label
    
    def writeLabel(self):
        if not self.exists:
            raise FileSystemError("Filesystem has not been created")
        
        if not self.labelCMD():
            return
        
        if not os.path.exists(self.device):
            raise FileSystemError("underlying device doesnt exist")
        
        argv = self._getLabelArgs(label)
        try:
            return_code = sysutils.execClear(self.labelCMD(), argv, stdout="/dev/tty5", stderr="/dev/tty5")
        except Exception, e:
            raise FileSystemError("Writing label failed!")
        
        if not return_code:
            raise FileSystemError("Writing label failed!")
        
        self._label = label
        self.notifyKernel()
        
    def status(self): 
        #FIXME:check /proc/mount or similar
        pass
    
    
class EXT2(FileSystem):
    """Ext2 File System"""
    _type = "ext2"
    _mkfs = "mke2fs"
    _resizefs = "resize2fs"
    _labelfs = "e2label"
    _fsck = "e2fsck"
    _resizable = True
    _bootable = True
    _maxsize = 8 * 1024 * 1024
    _minsize = 0
    _defaultFormatOptions = []
    _defaultMountOptions = ["default"]
    _defaultCheckOptions = ["-f", "-p", "-C", "O"]
    _dump = True
    _check = True
    _migratable = True
    _migrationTarget = "ex3"
    _migratefs = "tunefs"
    _defaultMigrateOptions = ["-j"]
    
    @property
    def minSize(self):
        """ Minimum size for this filesystem in MB. """
        if self._minInstanceSize is None:
            size = self._minSize
            if self.exists and os.path.exists(self.device):
                buf = sysutils.execWithCapture(self.resizeCMD(), ["-P", self.device], stderr="/dev/tty5")
                for line in buf.splitlines():
                    if "minimum size of the filesystem:" not in line:
                        continue

                    (text, sep, minSize) = line.partition(": ")

                    size = int(minSize) / 1024.0

                if size is None:
                    log.warning("failed to get minimum size for %s filesystem "
                                "on %s" % (self.type, self.device))

            self._minInstanceSize = size

        return self._minInstanceSize
    
class EXT3(EXT2):
    """Ext3 File System"""
    _type = "ext3"
    _defaultFormatOptions = ["-t", "ext3"]
    _migrationTarget = "ext4"
    _defaultMigrationOptions = ["-O","extends"]
    
class EXT4(EXT3):
    """Ext4 File System"""
    _type = "ext4"
    _bootable = False
    _defaultFormatOptions = ["-t", "ext4"]
    _migratable = False
    
    
class FAT(FileSystem):
    """ FAT filesystem. """
    _type = "vfat"
    _mkfs = "mkdosfs"
    _labelfs = "dosfslabel"
    _fsck = "dosfsck"
    _maxSize = 1024 * 1024
    _defaultMountOptions = ["umask=0077", "shortname=winnt"]
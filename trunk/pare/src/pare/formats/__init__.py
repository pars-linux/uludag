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
from pare.sysutils import notify_kernel, get_sysfs_path_by_name
from pare.utils.dm import dm_node_from_name
from pare.errors import FormatCreateError

import logging
log = logging.getLogger("pare")

import gettext
_ = lambda x: gettext.ldgettext("pare", x)

from filesystem import *
from pare.formats import FileSystem, EXT2, EXT3, EXT4, FAT


def get_format(type=None, *args, **kwargs):
    """
        type -- Format Class type
        device -- path to the device which resides
        uuid -- the UUID of (preexisting) formatted Device
        exists -- whether or not format exists on device
        
    """
    
    if type == "ext2":
        return EXT2(*args, **kwargs)
    elif type == "ext3":
        return EXT3(*args, **kwargs)
    elif type == "ext4":
        return EXT4(*args, **kwargs)
    elif type == "vfat":
        return FAT(*args, **kwargs)
    else:
        return FileSystem(*args, **kwargs)
        

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
                

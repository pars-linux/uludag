from pisi import Exception
import os.path
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

from libs.dm import dm_node_from_name
from errors import DeviceFormatError
import sysutils
import errors
import logging
log = logging.getLogger("storage")

import gettext
_ = lambda x: gettext.ldgettext("storage", x)

#
#device_formats = {}
#
#def register_device_format(format):
#    if not issubclass(format, DeviceFormat):
#        raise ValueError("arg1 must be a subclass of DeviceFormat")
#
#    device_formats[format._type] = format
#    log.debug("registered device format class %s as %s" % (format.__name__, format._type))
#
#default_fstypes = ("ext4", "ext3", "ext2")
#default_boot_fstypes = ("ext3", "ext2")

#def get_default_filesystem_type(boot=None):
#    if boot:
#        fstypes = default_boot_fstypes
#    else:
#        fstypes = default_fstypes
#
#    for fstype in fstypes:
#        try:
#            supported = get_device_format_class(fstype).supported
#        except AttributeError:
#            supported = None
#
#        if supported:
#            return fstype
#
#    raise DeviceFormatError(_("None of %s is supported by your kernel" % ",".join(fstypes)))

class DeviceFormat(object):
    """Generic Device Format"""

    partedFlag = None
    __formattable = False
    __native = False
    __supported = False
    __resizeable = False
    __bootable = False
    __maxSize = 0
    __minSize = 0
    __dump = False
    __check = False

    def __init__(self, *args, **kwargs):
        """Create DeviceFormat Instance
        
                device -- path to the underlying device
                uuid -- this format's UUID
                exists -- indicates whether this is an existing format
                
        """

        self.device = kwargs.get("device")
        self.uuid = kwargs.get("uuid")
        self.exists = kwargs.get("exists")
        self.options = kwargs.get("options")
        self._migrate =  kwargs.get("migrate")

    def notifyKernel(self):

        if not self.device:
            return

        if self.device.startswith("/dev/mapper"):
            try:
                name = dm_node_from_name(os.path.basename(self.device))
            except Exception, e:
                log.warning("failed to get dm node for %s" % self.device)
                return
        elif self.device:
            name = os.path.basename(self.device)

        path = sysutils.get_sysfs_path_by_name(name)
        try:
            notify_kernel(path)
        except Exception, e:
            log.warning("failed to notify kernel of change: %s" % e)

    def create(self, *args, **kwargs):
        device = kwargs.get("device")

        if device:
            self.device = device

        if not os.path.exists(self.device):
            raise FormatCrateError(_("invalid device specification"))

    def destroy(self, *args, **kwargs):
        self.exists = False

    def 





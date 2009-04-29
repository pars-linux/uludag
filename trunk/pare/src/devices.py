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


_type = ("disk", "partition", "luks", "vg", "lv", "pv", "raidarray", "raidmember")

import parted
import _ped
from syutils import notify_kernel
import logging
log = logging.getLogger("storage")

import gettext
_ = lambda x :gettext.ldgettext("storage", x)

class Storage(object):
    """A generic device"""
    _type = ""
    _sysfsBlockDir = "class/block"
    _devDir = "/dev"
    _resizable = False

    def __init__(self, device, format = None, size = None, major = None,
            minor = None, sysfsPath = '', exists = None, parents = None):

        self._uuid = None
        self._name = device
        self._format = format
        self._size = size
        self._major = major
        self._minor = minor
        self._sysfsPath = sysfsPath
        self._exists = exists
        self._disklabel = None
        self._fstab = None
        self._partedDevice = None
        self._targetSize = self._size

        self._diskLabel = None

        if parents = None:
            parents = []
        elif not isinstance(parents, list):
            raise ValueError("parents must be Device instances")
        self._parents = parents
        self_kids = 0

        for parent in self.parents:
            parent.addChild()

    def addChild(self):
        self._kids += 1

    def removeChild(self):
        self._kids -= 1

    def createParents(self):
        """Run create method for all parent devices."""
        for parent in self.parents:
            if not parent.exists:
                raise DeviceError("Parent device does not exist")

    def create(self):
        """Create the device"""
        pass

    def destroy(self):
        """Remove the device"""
        pass

    def teardown(self):
        """Close or tear down a device"""
        pass

    def setup(self):
        """Open or setup a device"""
        pass

    def setupParents(self):
        """Setup all parent devices"""
        pass

    def dependsOn(self, dependency):
        """True if device depends on dependency"""
        if dependency in self._parents:
            return True

        for parent in self._parents:
            if parent.dependsOn(dependency):
                return True

        return False

    @property
    def partedDevice(self):
        if self.exists and self.status and not self._partedDevice:
            log.debug("looking parted device %s" % self.path)

            try:
                self._partedDevice = parted.Device(path=self.path)
            except _ped.DeviceException:
                pass

            return self._partedDevice

    @property
    def getTargetSize(self):
        return self._targetSize

    @property
    def setTargetSize(self, newsize):
        return self._targetSize = newsize

    def resize(self, newsize):
        self.setTargetSize(newsize)

    def getSize(self):
        """ Get the device's size in MB, accounting for pending changes. """
        if self._exists and not self.mediaPresent:
            return 0
        if self._exists and self.partedDevice:
            self._size = self.currentSize

        size = self._size
        if self._exists and self.resizable and self.getTargetSize != size:
            size = self.getTargetSize
        return size


    def setSize(self, newsize):
        if newsize > self.maxSize:
            raise DeviceError("Device can not be larger than %d MB" % (self.maxSize(),))

    def currentSize(self):
        size = 0
        if self._exists and self.partedDevice:
            size = self.partedDevice.getSize()
        elif self._exists:
            size = self._size
        return size

    def getMaxSize(self):
       """The maximum size of the device can be"""
       if self.format.maxSize > self.currentSize:
            return self.currentSize
        else:
            return self.format.maxSize


    def getMinSize(self):
        """The minumum size of the device can be"""
        if self._exists:
            self.setup

        if self.format.minSize:
            return self.format.minSize
        else:
            self._size

    def path(self):
        """Device node representing this device"""
        return "%s/%s" % (self._devDir, self.name)

    def name(self):
        return self._name

    def status(self):
        """ The Device's status
            True is device open and ready for use
            False is device is not open
        """
        if not self.exists:
            return False
        return os.access(self.path, os.W_OK)

    def type(self):
        """Device Type"""
        return self._type

    def mediaPresent(self):
        return True

    def updateSysfsPath(self):
        """Update this device sysfs path"""
        sysfname = self.name.replace("/","!")
        path = os.path.join("/sys",sysfsBlockDir,sysfname)
        self.sysfsPath = os.path.realpath(path)[4:]
        log.debug("%s sysfs path %" % (self.name, self.e_sysfsPath))

    def notifyKernel(self):
        if not self.exists:
            log.debug("not sending change uevent for non-existing device")

        if not self.status:
            log.debug("not sending change uevent for inactive device")

        path = os.path.normpath("/sys%s" % self._sysfsPath)

        try:
            notify_kernel(path, action=change)
        except Exception, e:
            log.warning("failed to notify kernel of changed: %s" % e)

    def fstab(self):
        spec = self.path
        if self.format and self.format.uuid:
            spec ="UUID=%s" % self.format.uuid

        return spec

    def formatArgs(self):
        """Device specific arguments to format creation program."""
        return []

    def resizeable(self):
        return self._resizable and self._exists

class Disk(Storage):
    """A disk"""

    def __init__(self, device, format=None, size=None, major=None, minor=None, \
            sysfsPath='', parents=None, initCB=None, initLabel=None)
        """
        Create Disk instance
            device -- generally a device node basename
            size -- the device's size (units/format TBD)
            major -- device major
            minor -- device minor
            sysfsPath -- sysfs path
            parents -- a list of required Device instances
            format -- Device Format instances

            initCB -- a callback to be used for initiating disk
            initLabel --  whether to start a fresh disk
        """
        Storage.__init__(device, format=format, size=size, major=major, minor=minor \
                exists=True, sysfsPath=sysfsPath, parents=parents)

        self._partedDisk = None

        log.debug("looking up parted Device %s" % self.path)

        if self.partedDevice:
            log.debug("creating parted Disk: %s" % self.path)
            if initLabel:
                self._partedDisk = self.freshPartedDisk()
            else:
                try:
                    self._partedDisk = parted.Disk(device=self.partedDevice)
                except _ped.DeviceException:
                    if initcb in not None and initcb():
                        self._partedDisk = parted.freshDisk(device=self.partedDevice,\
                            ty = platform.getPlatform(None).diskType)
                    else:
                        DeviceUserDeniedFormatError("User prefered to not format.")

        #Set the actual state of the disk here before the fist modification
        if self._partedDisk:
            self._origPartedDisk = self._partedDisk.duplicate()
        else:
            self._origPartedDisk = None

    def mediaPresent(self):
        return self.partedDevice is not None

    def model(self):
        return getattr(self.partedDevice, "model", None)

    def freshPartedDisk(self):
        #FIXME
        labelType = ''
        return parted.freshDisk(device=self.partedDevice, ty=labelType)

    def resetPartedDisk(self):
        self._partedDisk = self._origPartedDisk

    def addPartition(self, device):
        if not self.mediaPresent:
            raise DeviceError("cannnot add media to disk with no media", self.path)

       geometry = device.partedPartition.geometry
       constraint = parted.Constraint(exactGeom=geometry)
       partition = parted.Partition(disk=self.partedDisk, type=device.partedPartition.type, geometry=geometry)

       self.partedDisk.addPartition(partition,constraint=constraint)

    def removePartiton(self, device):
        if not self.mediaPresent:
            raise DeviceError("cannot remove media from disk %s which has no media %s" % (self.name, self.path))

        partition = self.partedDisk.getPartitionByPath(device.path)

        if partition:
            self.partedDisk.removePartition(partition)

    def probe(self):
        """Probe for any missing information about thiss device"""
        if not self._disklabel:
            log.debug("setting %s diskLabel to %s" % (self.name, self.path))
            self._diskLabel = self._partedDisk.type

    def commit(self):
        """Commit changes to the device"""
        if not self.mediaPresent:
            raise DeviceError(" %s cannot commit to disk with no media" % self.path)

        self.setupParents()
        self.setup()

        attempt = 1
        max = 5
        keepTrying = True

        while keepTrying and (attempt <= max):
            try:
                self.partedDisk.commit()
                keepTrying = False
            except parted.DiskException as msg:
                log.warning(msg)
                attempt +=1

        if keepTrying:
            raise DeviceError("cannot commit to disk after %d attempts" % (max,), self.path)

        #FIXME
        #Udev_Settle may be used after commit

    def destroy(self):
        """Destroy the device"""
        if not self.mediaPresent:
            raise DeviceError("cannot destroy disk with no media", self.path)

        self.partedDisk.deleteAllPartitions()
        self.partedDisk.clobber()
        self.partedDisk.commit()
        self.teardown()

class Partition(Storage):
    """A disk partition"""

    _resizable = True

    def __init__(self, name, format=None, size=None, grow=False, maxsize=None\
                major=None, minor=None, bootable=None, sysfsPath='', parents=None\
                exists=None, partType=None):
        """
            name -- device node base name

            exists -- indicates whether this is an existing device
            format -- device format

            *** For existing partitions ***
                parents -- the disk that contains this partition
                major -- device major
                minor -- device minor
                sysfsPath -- sysfs device path

            *** For new partitions ***
               partType -- primary, extended
               grow -- whether or not to grow the partition
               maxsize -- max size of the growable partition
               size -- the device's size (in MB)
               bootable -- whether the partition is bootable
               parents -- a list of potential containing disk

        """

        self._req_disks = []
        self._req_parType = None
        self._req_primary = None
        self._req_grow = None
        self._req_bootable = None
        self._req_size = 0
        self._req_base_size = 0
        self._req_max_size = 0

        self._bootable = False

        Storage.__init__(self, name, format=format, size=size, major=major, minor=minor, \
                        exists=exists, sysfsPath=sysfsPath, parents=parents)
        if not exists:
            self._req_disks = self.parents[:]

        for parent in parents:
            parent.removeChild()
        self.parents = []



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
from errors import *
from storage import Disk, Partition
from formats import StorageFormat
from udev import *

import gettext
_ = lambda x: gettext.ldgettext("pare", x)

import logging
log = logging.getLogger("pare")

class StorageList(oject):
    def __init__(self, ignoredDisk = [], reinitializeDisks=None, clear=[], protected=[]):
        self._devices = []
        self._actions = []
        
        self.clearPartDisks = clear
        self.protectedPartitions = protected
        self.reinitializeDisks = reinitializeDisks
        self._ignoredDisks = []
        for disk in ignoredDisk:
            self.addIgnoredDisk(disk)
        
    def _add(self, new):
        
        if new.path in  [d.path for d in self._devices]:
            raise ValueError("new device is already in storage list")
        
        for parent in new.parents:
            if parent not in self._devices:
                raise StorageListError("new device parent not in storage list")
        
        self._devices.append(new)
        log.debug("%s is added to storage list" % (new.name,))
    
    def _remove(self, dev, force=None):
        if dev not in self._devices:
            raise ValueError("Device '%s' is not in storage list" % dev.name)
        
        if not dev.isLeaf and not force:
            log.debug("%s has %d kids" % (dev.name, dev.kids) )
            raise ValueError("Device %s hasnt been removed" % dev.name)
        
        if isinstance(dev, Partition) and devi.disk is not None:
            if dev.partedPartition.type == parted.PARTITION_EXTENDED and len(dev.disk.partedDisk.getLogicalPartitions() > 0 ):
                raise ValueError("Can not remove %s extended Partitions. logical Partitons present" % dev.name)
            
            dev.disk.partedDisk.removePartition(dev.partedPartition)
            
        
        self._devices.remove(dev)
        log.debug("removed %s '%s' in storage list" % (dev.name, dev.type))
    
    def _checkInconsistenceDevices(self):
        
        #FIXME: Check inconsistences also lvm & raid
        
        for part in self.getDevicesByInstance(Partition):
            if part.parents[0].format.type is not None:
                disk = part.parents[0]
                format = StorageFormat(device=disk.path, exists=True)
        
                log.warning("Automatically corrected fomrat error on %s. Changed from %s to %s." % (disk.name, disk.format, format))
                disk.format = format
                
    def addIgnoredDisk(self, disk):
        self._ignoredDisks.append(disk)
        #FIXME: when lvm is came up add this lvmm filtering ;)
        
    def isIgnored(self, info):
        name = udev_device_get_name(info)
        sysfs_path = udev_device_get_sysfs_path(info)
        if not sysfs_path:
            return None
        
        if name in self._ignoredDisks:
            return True
        
        for ignored in self._ignoredDisks:
            if ignored == os.path.basename(os.path.dirname(sysfs_path)):
                return True
            
        #FIXME:May be check dmraid device if we think to use
        
        # we ignored loop* and ram* in enumarete_disk but this recheck :)
        if name.startswith("loop") or name.startswith("ram"):
            return True
    
    def addDevice(self, info):
        name = udev_device_get_name(info)
        uuid = udev_device_get_uuid(info)
        sysfs_path = udev_device_get_sysfs_path(info)
        
        if self.isIgnored(info):
            log.debug("ignoring %s (%s)" % (name, sysfs_path))
            return
        
        device = udev_device_get_name(info)
        
        #FIXME:Later handle other storage subclasses like lvm & raid
        if udev_device_is_disk(info):
            if device is None:
                device = self.addDisk(info)
        elif udev_device_is_partition(info):
            if device is None:
                device = self.addPartition(info)
        
    def addPartition(self, info):
        name = udev_device_get_name(info)
        uuid = udev_device_get_uuid(info)
        sysfsPath =  udev_device_get_sysfs_path(info)
        device = None
        
        diskName = os.path.basename(os.path.dirname(sysfsPath))
        disk = self.getDeviceByName(diskName)
        
        if disk is None:
            path = os.path.dirname(os.path.realpath(sysfsPath))
            newInfo = udev_get_block_device(path)
            if newInfo:
                self.addDevice(newInfo)
                disk = self.getDeviceByName(diskName)
                
            #if the current device is still not in the storage list, something has gone wrong
            if disk is None:
                raise StorageError("something goes wrong")
            
        try:
            device = Partition(name, 
                               major=udev_device_get_major(info), 
                               minor=udev_device_get_minor(info), 
                               sysfsPath=sysfsPath, parents=[disk],
                               exists=True)
        except StorageError:
            raise StorageFormatError("Partition creation failed")
        
        self._add(device)
        return device
            
            
    
    def addDisk(self, info):
        name = udev_device_get_name(info)
        uuid = udev_device_get_uuid(info)
        sysfsPath =  udev_device_get_sysfs_path(info)
        device = None
        
        # if the disk contains protected partitions we will not wipe the disklabel
        if not self.clearPartDisks or name not in self.clearPartDisks:
            # Default self.reinitializeDisks is False
            initLabel = self.reinitializeDisks
            
            for protected in self.protectedPartitions:
                p = "/sys/%s/%s" % (sysfsPath, protected)
                if os.path.exists(os.path.normpath(p)):
                    initLabel = False
                    break
        else:
            initLabel = False
            
        try:
            device = Disk(name, major=udev_device_get_major(info), 
                          minor=udev_device_get_minor(info), 
                          sysfsPath=sysfsPath,initLabel=initLabel)
        except StorageFormatError:
            self.addIgnoredDisk(name)
        
        self._add(device)
        return device
    
    def handleDeviceFormat(self):
        pass
        
    def getDeviceByName(self, name):
        logging.debug("looking for device %s" % name)
        found = None
        for device in self._devices:
            if device.name == name:
                found = device
                break
            elif (device.type == "lvmlv" or device.type == "lvmvg") and device.name == name.replace("--","-"):
                found = device
                break

        log.debug("found %s" % found)
        return found
    
    def getDeviceBySysfsPath(self, path):
        logging.debug("looking for device %s" % path)
        found = None
        for device in self._devices:
            if device.sysfsPath == path:
                found = device
                break
        
        return found
    
    def getDeviceByUUID(self, uuid):
        logging.debug("looking for device %s" % uuid)
        found = None
        for device in self._devices:
            if device.uuid == uuid:
                found = device
                break
            elif device.format.uuid == uuid:
                found = device
                break
            
        return found
    
    def getDeviceByLabel(self, label):
        logging.debug("looking for device %s" % label)
        found = None
        for device in self._devices:
            if not device.label:
                continue
            
            if device.label == label:
                found = device
                break
            
        return found
    
    def getDevicesByType(self, type):
        logging.debug("looking for device %s" % type)
        
        return [d for d in self._devices if d.type == type]
        
    def getDevicesByInstance(self, device_class):
        
        return [d for d in self._devices if isinstance(d, device_class)]
    
    @property
    def devices(self):
        devices = {}
        
        for device in self._devices:
            if device.path in devices:
                raise StorageListError("duplicate path in storage list")
            else:
                devices[device.path] = devices
        
        return devices
    
    @property
    def filesystems(self):
        filesystems = []
        for device in self.leaves():
            if device.format and device.format.mountpoint:
                filesystems.append(device.format)
                
        return filesystems
    
    @property
    def leaves(self):
        return [d for d in self._devices if d.isLeaf]
    
    @property
    def labels(self):
        labels = {}
        for device in self._devices:
            if device.format:
                labels[device.format.label] = device
        
        return labels
    
    @property
    def uuids(self):
        uuids = {}
        for device in self._devices:
            if device.uuid :
                uuids[uuid] = device
            elif device.format.uuid:
                uuids[uuid] = device
            
        return uuids
    
    def getKid(self, device):
        return [d for d in self._devices if device in d.parents ]
    
    
    def populate(self):
        old = []
        ignored = []
        
        while True:
            devices = []
            new = udev_get_block_devices()
            
            for _new_dev in new:
                found = False
                for _old_dev in old:
                    if _old_dev["name"] == _new_dev["name"]:
                        found = True
                        break
                if not found:
                    devices.append(_new_dev)
                
                if len(devices == 0):
                    break
                
            old =  new 
            log.info("devices to scan: %s" % [d['name'] for d in devices])
            for dev in devices:
                self.addDevice(dev)
        
        self._checkInconsistenceDevices()
        self.tearDownAll()
        
        
    def tearDownAll(self):
        for device in self.leaves():
            try:
                device.tearDown()
            except StorageError, StorageFormatError:
                log.info("teardown failed")
                
    def setupAll(self):
        for device in self.leaves():
            try:
                device.setup()
            except StorageError, StorageFormatError:
                log.info("setup failed")
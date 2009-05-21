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
import parted
from errors import *
from pare.storage import Disk, Partition
from pare.formats import StorageFormat, FileSystem, get_format
from pare.storageactions import *
from udev import *

import gettext
_ = lambda x: gettext.ldgettext("pare", x)

import logging
log = logging.getLogger("pare")

class StorageList(object):
    def __init__(self, ignored=[], reinitializeDisks=None, clear=[], protected=[]):
        self._devices = []
        self._actions = []
        
        self.clearPartDisks = clear
        self.protectedPartitions = protected
        self.reinitializeDisks = reinitializeDisks
        self.ignoredDisks = []
        for disk in ignored:
            self.addIgnoredDisk(disk)
        
    def _add(self, new):
        
        if new.path in  [d.path for d in self._devices]:
            raise ValueError("new device is already in storage list")
        
        for parent in new._parents:
            if parent not in self._devices:
                raise StorageListError("new device parent not in storage list")
        
        self._devices.append(new) 
        log.debug("%s is added to storage list" % (new.name,))
    
    def _remove(self, device, force=None):
        if device not in self._devices:
            raise ValueError("Device '%s' is not in storage list" % device.name)
        
        if not device.isLeaf and not force:
            log.debug("%s has %d kids" % (device.name, device.kids) )
            raise ValueError("Device %s hasnt been removed" % device.name)
        
        if isinstance(device, Partition) and device.disk is not None:
            if device.partedPartition.type == parted.PARTITION_EXTENDED and len(device.disk.partedDisk.getLogicalPartitions() > 0 ):
                raise ValueError("Can not remove %s extended Partitions. logical Partitons present" % device.name)
            
            device.disk.partedDisk.removePartition(device.partedPartition)
            
        
        self._devices.remove(device)
        log.debug("removed %s '%s' in storage list" % (device.name, device.type))
    
    def _checkInconsistenceDevices(self):
        
        #FIXME: Check inconsistences also lvm & raid
        
        for part in self.getDevicesByInstance(Partition):
            if part._parents[0].format is not None:
                disk = part._parents[0]
                format = FileSystem(device=disk.path, exists=True)
        
                log.warning("Automatically corrected format error on %s. Changed from %s to %s." % (disk.name, disk.format, format))
                disk.format = format
                
    def addIgnoredDisk(self, disk):
        self.ignoredDisks.append(disk)
        #FIXME: when lvm is came up add this lvm filtering ;)
        
    def isIgnored(self, info):
        name = udev_device_get_name(info)
        sysfs_path = udev_device_get_sysfs_path(info)
        if not sysfs_path:
            return None
        
        if name in self.ignoredDisks:
            return True
        
        for ignored in self.ignoredDisks:
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
        
        device = self.getDeviceByName(name)
        
        #FIXME:Later handle other storage subclasses like lvm & raid
        if udev_device_is_disk(info):
            if device is None:
                device = self.addDisk(info)
        elif udev_device_is_partition(info):
            if device is None:
                device = self.addPartition(info)

                
        self.handleDeviceFormat(info, device)
    
    def addFreePartition(self, part):
        pass
       
    def addPartition(self, info):
        name = udev_device_get_name(info)
        uuid = udev_device_get_uuid(info)
        sysfsPath =  udev_device_get_sysfs_path(info)
        #print "syspath:%s" % sysfsPath
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
                               sysfsPath=sysfsPath,exists=True, parents=[disk])
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
    
    def handleDeviceFormat(self, info, device):
        name = udev_device_get_name(info)
        sysfs_path = udev_device_get_sysfs_path(info)
        uuid = udev_device_get_uuid(info)
        label = udev_device_get_label(info)
        format_type = udev_device_get_format(info)
        
        
        #FIXME:Control block device or CDROM device? Arent they IDS_FS_TYPE variable on udev dict
        #FIXME: this probably needs something special for disklabels
        if (not device) or (not format_type) :
            log.debug("no type or existing type for %s, bailing" % (name,))
        
        format = None
        args = [format_type]
        kwargs = {"uuid": uuid,
                  "label": label,
                  "device": device.path,
                  "exists": True}
        
        
        try:
            log.debug("type detected on '%s' is '%s'" % (name, format_type))
            #FIXME: Change wrong device.format assignment on disk type devices. It gives warning
            if format_type:
               format = get_format(format_type, *args, **kwargs)
            else:
                format = get_format()
                  
            device.format = format
        except FileSystemError:
            log.debug("type '%s' on '%s' invalid, assuming no format" % (format_type, name,))
            device.format = get_format()
              
        
    def getDeviceByName(self, name):
        logging.debug("looking for device %s" % name)
        found = None
        for device in self._devices:
            if str(device.name) == name:
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
    
    def getDependencies(self, dependency):
        dependencies = []
        logicals = []
        
        if isinstance(dependency, Partition) and dependency.partType and dependency.isExtended:
            for part in self.getDevicesByInstance(Partition):
                if part.partType and part.isLogical and part.disk == dependency.disk:
                    logicals.append(part)
        
        for device in self.devices().values():
            if device.dependsOn(dependency):
                dependencies.append(devicependency)
            else:
                for logical in logicals:
                    device.dependsOn(logical)
                    dependencies.append(device)
                    break
        
        return dependencies
            
    @property
    def devices(self):
        devices = {}
        for device in self._devices:
            if device.path in devices:
                raise StorageListError("duplicate path in storage list")
            else:
                devices[device.path] = device
        
        return devices
    
    @property
    def filesystems(self):
        filesystems = []
        for device in self.leaves:
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
        old_devices = []
        ignored_devices = []
        
        while True:
            devices = []
            new_devices = udev_get_block_devices()
            for new_device in new_devices:
                found = False
                for old_device in old_devices:
                    if old_device["name"] == new_device["name"]:
                        found = True
                        break
                    
                if not found:
                    devices.append(new_device)
                
            if len(devices) == 0:
                break
                
            old_devices =  new_devices
            log.info("devices to scan: %s" % [d['name'] for d in devices])
            for dev in devices:
                self.addDevice(dev)
        
        self._checkInconsistenceDevices()
        self.tearDownAll()
        
        #FIXME:os.unlink("/etc/mdadm.conf")
    
    def tearDownAll(self):
        for device in self.leaves:
            try:
                device.tearDown()
            except StorageError, StorageFormatError:
                log.info("tearDown failed")
                
    def setupAll(self):
        for device in self.leaves:
            try:
                device.setup()
            except StorageError, StorageFormatError:
                log.info("setup failed")
    
    
    def process(self):
        """
            Not rely rules of registration! Be careful check again! 
        """
        
        def _cmp(action1, action2):
            ret = 0
            
            ###Destroy Action Compare StartPoint
            if action1.isDestroy() and action2.isDestroy():
                if action1.device.path == action2.device.path:
                    # if the same device, destroy the format first
                    if action1.isFormat() and action2.isFormat():
                        ret = 0
                    elif action1.isFormat() and not action2.isFormat():
                        ret = -1
                    elif not action1.isFormat() and action2.isFormat():
                        ret = 1
                elif action1.device.dependsOn(action2.device):
                    ret = -1
                elif action2.device.dependsOn(action1.device):
                    ret = 1
                
                elif isinstance(action1.device, Partition) and isinstance(action2.device, Partition):
                    ret = cmp(action2.device.name, action1.device.name)
                # destroy partitions after lv, vgs
                elif isinstance(action1, Partition) and not isinstance(action2, Disk):
                    ret = 1
                elif isinstance(action2, Partition) and not isinstance(action1, Disk):
                    ret = -1
            elif action1.isDestroy():
                ret = -1
            elif action2.isDestroy():
                ret = 1
            
            ###Resize Action Compare StartPoint
            elif action1.isResize() and action2.isResize():
                if action1.device.path == action2.path:
                    #same path
                    if action1.obj and action2.obj:
                        #same device
                        ret = 0
                    elif action1.isFormat() and not action2.isFormat():
                        if action1.isGrow():
                            ret = 1
                        else:
                            ret = -1
                    elif not action1.isFormat() and action2.isFormat():
                        if action1.isGrow():
                            ret = -1
                        else:
                            ret = 1
                    else:
                        ret = cmp(action1.device.name, action2.device.name)
                
                elif action1.device.dependsOn(action2.device):
                    if action1.isGrow():
                        ret = 1
                    else:
                        ret = -1
                elif action2.device.dependsOn(action2.device):
                    if action2.isGrow():
                        ret = -1
                    else:
                        ret = 1
                elif isinstance(action1.device, Partition) and isinstance(action2.device, Partition):
                    ret = cmp(action2.device.name, action1.device.name)
                # resize partitions after lv, vgs
                elif isinstance(action1, Partition) and not isinstance(action2, Disk):
                    if action1.isGrow():
                        ret = -1
                    else:
                        ret = 1
                elif isinstance(action2, Partition) and not isinstance(action1, Disk):
                    if action2.isGrow():
                        ret = 1
                    else:
                        ret = -1
                else:
                    ret = 0
            elif action1.isResize():
                ret = -1
            elif action2.isResize():
                ret = 1
            
            ###Create Action Compare StartPoint
            elif action1.isCreate() and action2.isCreate():
                if action1.device.path == action2.device.path:
                    if action1.obj == action2.obj:
                        ret = 0
                    elif action1.isFormat():
                        ret = 1
                    elif action2.isFormat():
                        ret = -1
                    else:
                        ret = 0
                elif action1.device.dependsOn(action2.device):
                    ret = 1
                elif action2.device.dependsOn(action1.device):
                    ret = -1
                # create partition before other types like lv,vg,pv
                elif isinstance(action1.device, Partition) and isinstance(action2.device, Partition):
                    ret = cmp(action1.device.name, action2.device.name)
                elif isinstance(action1.device, Partition) and not isinstance(action2.device, Disk):
                    ret = -1
                elif isinstance(action2.device, Partition) and not isinstance(action1.device, Disk):
                    ret = 1
                else:
                    ret = 0
            
            elif action1.isCreate():
                ret = -1
            elif action2.isCreate():
                ret = 1
            
            ###Migrate Action Compare StartPoint
            elif action1.isMigrate() and action2.isMigrate():
                if action1.device.path == action2.device.path:
                    ret = 0
                elif action1.device.dependsOn(action2.device):
                    ret = 1
                elif action2.device.dependsOn(action1.device):
                    ret = -1
                elif isinstance(action1.device, Partition) and isinstance(action2.device, Partition):
                    ret = cmp (action1.device.name, action2.device.name)
                else:
                    ret = cmp (action1.device.name, action2.device.name)
            
            else:
                ret = 0
            
            log.debug("_cmp %d -- %s | %s" % (ret, action1, action2))
            
            return ret            

        log.debug("sorting actions")
        self._actions.sort(cmp=_cmp)                   
        for action in self._actions:
            log.debug("action:%s" % action)
        
        log.debug("resetting parted disks")
        for device in self.devices.itervalues():
            if isinstance(device, Disk):
                device.resetPartedDisk()
        
        for action in self._actions:
            log.info("executing action: %s" % action)
            action.execute()
            udev_settle()
                
                
    def register(self, action):
        """ Registered action can be performed later!
            Modifications to the Device are handled before we get there :) 
        """
        if(action.isDestroy() or action.isResize() or (action.isCreate() and action.isFormat())) and action.device not in self._devices:
            raise StorageListError("Device isnt in the list")
        elif (action.isCreate() and action.isDevice()):
            if action.device in self._devices:
                self._remove(action.device)
            for dev in self._devices:
                if action.device.path == dev.path:
                    self._remove(action.device)
        
        if action.isCreate() and action.isDevice():
            self._add(action.device)
        elif action.isDestroy() and action.isDevice():
            self._remove(action.device)
        elif action.isCreate() and action.isFormat():
            if isinstance(action.device.format, FileSystem) and action.device.format.mountpoint in self.filesystems:
                raise StorageListError("mount point already in use")
        
        log.debug("registered action %s" % action)
        self._actions.append(action)

    def cancel(self, action):
        if action.isCreate() and action.isDevice():
            self._remove(action.device)
        elif action.isDestroy() and action.isDevice():
            self._add(action.device)
        elif action.isFormat() and (action.isCreate() or action.isMigrate() or action.isResize()):
            action.cancel()
            self._actions.remove(action)
    
    def find(self, device=None, type=None, object=None, path=None):
        """
            device -- 
            type -- 
            object --
            path --
        """
        # return full action list
        if device is None and type is None and object is None and path is None:
            self._actions[:]
        
        _type = type_from_string(type)
        _object = object_from_string(object)
        
        actions = []
        for action in self._actions:
            if device is not None and action.device != device:
                continue
            
            if type is not None and action.type != type:
                continue
            
            if object is None and action.obj != object:
                continue
            
            if path is not None and action.device.path != device.path:
                 continue
            
            actions.append(action)
            
        return actions
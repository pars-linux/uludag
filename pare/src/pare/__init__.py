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

import parted
import udev
from storagelist import StorageList
from storage import Storage,Disk,Partition
from storageactions import CreateDevice, CreateFormat, DestroyDevice, DestroyFormat


    

class Pare(object):
    def __init__(self):
        """
        """
        self.ignoredDisks = []
        self.reinitializeDisks = []
        self.clearPartdisks = []
        self.protectedPartitions = []
        
        self.storageList = StorageList(ignored=self.ignoredDisks,
                                       reinitializeDisks=self.reinitializeDisks,
                                       clear=self.clearPartdisks,
                                       protected=self.protectedPartitions)
    
        self.rawPartitionList = []
        self._id = 0 # use for requested and free space partition
        
    
    def _getPartedPartition(self, part, size, type):
        geom = part.geometry
        dev = geom.device
        len = long(size * 1024 * 1024) / dev.sectorSize

        newGeom = parted.Geometry (device = dev, start=geom.start, length=len)
        partedPartition = parted.Partition(disk=part.disk, type=type, geometry=newGeom)
        
        return partedPartition
    
    def _getNextPartitionType(self, disk, noprimary=None):
        type = None
        extented = disk.getExtendedPartition()
        hasExtendedSupport = disk.supportsFeature(parted.DISK_TYPE_EXTENDED)
        logicals = len(disk.getLogicalPartitions())
        maxlogicals = disk.getMaxLogicalPartitions()
        primaries = disk.primaryPartitionCount
        maxprimaries = disk.maxPrimaryPartitionCount
        
        if primaries == maxprimaries and extented and logicals < maxlogicals:
            type = parted.PARTITION_LOGICAL
        elif primaries == (maxprimaries - 1) and not extented and hasExtendedSupport:
            type = parted.PARTITION_EXTENDED
        elif noprimary and extented and logicals < maxlogicals:
            type = parted.PARTITION_LOGICAL
        elif not noprimary:
            type = parted.PARTITION_NORMAL
            
        return type
    
    def addFreePartitions(self, disks):
        for disk in disks:
            if isinstance(disk, Disk):
                part = disk.partedDisk.getFirstPartition()
                while part:
                    if not part.type & parted.PARTITION_FREESPACE:
                        part = part.nextPartition()
                        continue
                    
                    if part.getSize(unit="MB") > 10:
                        freepart =  Partition(name=part.getDeviceNodeName(), minor=part.number, parents=[disk])
                        freepart.partedPartition = part
                        self.storageList._add(freepart)
                        
                    part = part.nextPartition()
                
                
            
    
    def done(self):
        self.storageList.process()
    
    def nextID(self):
        self._id +=1
        return self._id
        
    def initialize(self):
        self.storageList.populate()
        self.addFreePartitions(self.disks)
        #for disk in self.disks:
        #    freeParts = self._getFreePartitions(disk)
        #    for free in freeParts:
        #        part = self.newPartition(name=free.getDeviceNodeName(), minor=free.number, parents=[disk])
        #        part.partedPartition = free
        #        self.storageList._add(part)
        
    @property
    def devices(self):
        devices = self.storageList.devices.values()
        #devices.sort(key=lambda d: d.path)
        return devices
    
    @property
    def list(self):
        return self.storageList
    
    @property
    def disks(self):
        disks = []
        devices = self.storageList.devices
        for dev in devices:
            if isinstance(devices[dev], Disk):
                disks.append(devices[dev])
        disks.sort(key=lambda d:d.name)
        return disks
    
    @property
    def partitions(self):
        partitions = self.storageList.getDevicesByInstance(Partition)
        partitions.sort(key=lambda d:d.name)
        return partitions
    
    @property
    def swaps(self):
        pass
    
    @property
    def dependentDevices(self, device):
        return self.storageList.getDependencies(device)
            
    def newPartition(self, part, *args, **kwargs):
        #format -- device format must be already added
        #name -- device node base name must be already added
        
        if kwargs.has_key("disks"):
            parents = kwargs.pop("disks")
            if isinstance(parents, Storage):
                kwargs["parents"] = [parents]
            else:
                kwargs["parents"] = parents
        if kwargs.has_key("name"):
            name = kwargs.pop("name")
        else:
            name = "req%d" % self.nextID()
            
        type = self._getNextPartitionType(part.disk)
        partition = Partition(name,exists=False, partType=type, *args, **kwargs)
        partition.partedPartition = self._getPartedPartition(part, size=partition.size, type=partition.partType)
        
        return partition
    
    def createDevice(self, device):
        self.storageList.register(CreateDevice(device))
        if device.format.type:
            self.storageList.register(CreateFormat(device))
            
    def destroyDevice(self, device):
        if device.format.exists and device.format.type:
            print "device.format.exists :%s device.format.type :%s" % (device.format.exists, device.format.type) 
            self.storageList.register(DestroyFormat(device))
            
        self.storageList.register(DestroyDevice(device))
    
    def formatDevice(self, device, format):
        self.storageList.register(DestroyFormat(device))
        self.storageList.register(CreateFormat(device, format))
        
    def isProtected(self, device):
        return device.name in self.protectedPartitions
    
        
        
        
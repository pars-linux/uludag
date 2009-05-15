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
    def setup(self):
        self.storageList.process()
    
    def storageInitialize(self):
        self.storageList.populate()
        
    @property
    def devices(self):
        devices = self.storageList.devices.values()
        #devices.sort(key=lambda d: d.path)
        return devices
    
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
    
    def newPartition(self, *args, **kwargs):
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
            
        return Partition(name, *args, **kwargs)
    
    def createDevice(self, device):
        self.storageList.register(CreateDevice(device))
        if device.format.type:
            self.storageList.register(CreateFormat(device))
            
    def destroyDevice(self, device):
        if device.format.exists and device.format.type:
            self.storageList.register(DestroyFormat(device))
            
        self.storageList.register(DestroyDevice(device))
    
    def formatDevice(self, device, format):
        self.storageList.register(DestroyFormat(device))
        self.storageList.register(CreateFormat(device, format))
        
    def isProtected(self, device):
        return device.name in self.protectedPartitions
    
        
        
        
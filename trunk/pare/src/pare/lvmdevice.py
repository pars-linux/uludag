# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
# Copyright 1999-2008 Gentoo Foundation
#
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
#

import math
import os
from pare.utils import lvm 
from pare.partition import PhysicalVolume
import pare.parteddata 
from pare.errors import *

         
class VolumeGroup(object):
    _type = volumeGroupType 
    _devBlockDir = "/dev" # FIXME:ReCheck VG path not to give acces_isSetups error
    _pvs = []
    _lvs = []
    _exists = None
    
    def __init__(self, name, size=None, uuid=None, 
                 pvs=None, maxPV=None, pvCount=None, 
                 peSize=None, peCount=None, peFree=None,
                 lvNames=[], maxLV=None, existing=0):
        
        """
            name -- device node's basename
            peSize -- Physical extents Size (in MB) Must be power power 2!
            existing -- indicates whether this is a existing device
            
        Existing VG
            size -- size of VG (in MB)
            uuid -- Volume Group UUID
            pvs -- a list of physical volumes. Parents of this VG
            maxPV -- max number of PVs in this VG
            pvCount -- number of PVs in this VG
            peCount -- number of PE in this VG
            peFree -- number of free PE in this VG
            lvNames -- list of LVs in this VG
            maxLV -- max number of LVs in this VG
        """
        
        self._exists = existing
        self._name = name
        self._size = size
        self._uuid = uuid
        self._maxPV = maxPV
        self._maxLV = maxLV
        self._pvCount = pvCount
        self._peSize = peSize
        self._peCount = peCount
        self._peFree = peFree
        self._maxLV = maxLV
        
        if pvs is not None:
            if isinstance(pvs, list):
                for pv in physicalVolumes:
                    self._pvs.append(pv)
              
        if self._peSize is None:
            self._peSize = 4 # MB units 
    
    def create(self):
        if self.exists:
            raise VolumeGroupError("Device is already exist")
        
        pvs = []
        for pv in self.pvs:
            if not pv.exists:
                raise PhysicalVolumeError("Volume Group Physical doesnt exist!")
            else:
                pvs.append(pv)
        
        lvm.vgcreate(self.name, pvs, self._peSize)
        self._exists =True
        
    def destroy(self):
        if not self.exists:
            raise LVMError("Device doesnt exist!" , self.path)
        
        try:
            lvm.vgreduce(self._name, [], rm=True)
            lvm.vgremove(self._name)  
        except LVMError:
            raise VolumeGroupError("Could not complete remove VG", self.path)
        finally:
            self._exists = True
    
    
    def reduce(self, pvs):
        if not self.exists:
            raise VolumeGroupError("Device has not been created!", self.path)
        
        lvm.vgreduce(self._name, pvs)
    
    def _addDevice(self, device):
        self.pvs.append(device)

    def _removeDevice(self, device):
        try:
            self.pvs.remove(device)
        except:
            raise VolumeGroupError("Couldnt remove non-member PV device from VG")    
    
    def addPV(self, pv):
        """
            Add PV to this VG. Used to add PV to requested VG.
        """
        if pv in self.pvs:
            raise ValueError("device is already in VG")
        
        #Cannot allow vg.extend
        if self.exists:
            raise VolumeGroupError("Volume Group already exist and can not add pv to existing VG")
        
        self.pvs.append(pv)
                
    def removePV(self, pv):
        """
            Remove PV to this VG. Used to remove PV to requested VG.
        """        
        if not pv in self.pvs:
            raise ValueError("Specified PV is not part of VG")
        
        #Cannot allow vg.reduce
        if self.exists:
            raise VolumeGroupError("Volume Group already exist and can not remove pv to existing VG")
        
        self.pvs.remove(pv)
    
    def addLV(self, lv):
        if lv in self.lvs:
            raise ValueError("Logical Volume is part of this Volume Group")
        
        if not lv.exists and lv.size > self.freeSpace:
            raise VolumeGroupError("Requested Logical Volume is too large to fit in free space", self.path)
        
        self.lvs.append(lv)
        
    def removeLV(self, lv):
        if lv not in self.lvs:
            raise ValueError("Specified lv is not part of VG")
        
        self.lvs.remove(lv)
    
    def setupParents(self):
        for pv in self._pvs:
            pv.create()
    
    def setup(self):
        pass
        
    @property
    def name(self):
        return self._name
    
    @property
    def path(self):
        return "%s/%s" % (self._devBlockDir, self.name)
    
    @property
    def exists(self):
        if not self._exists:
            return False
        
        for lv in self._lvs:
            if lv.status:
                return True 
        
        for pv in self._pvs:
            if not pv.status:
                return False
    
        return  True
        
    @property
    def status(self):
        if not self.exists:
            return False
        return os.access(self.path, os.W_OK)
        
    @property
    def pvs(self):
        return self._pvs[:]
    
    @property
    def lvs(self):
        return self._lvs[:]
    
    @property
    def size(self):
        size = 0
        for pv in self.pvs:
            size += pv.size
        
        return size
    
    @property
    def isModified(self):
        """
            Return True if VG has changes queued that LVM is aware of
        """
        
        modified = True
        if self.exists and not filter(lambda d: d.exists, self.pvs):
            modified = False
        
        return modified
        
    @property
    def extents(self):
        return self.size / self._peSize
    
    @property
    def freeSpace(self):
        used = 0
        size = self.size
        for lv in self.lvs:
            used += self._align(lv.size, roundup=True)
            
        free = size - used
        
        return free
    
    @property
    def freeExtents(self):
        return self.freeSpace / self._peSize
    
    def _align(self, size, roundup=None):
        
        if roundup:
            round = math.ceil
        else:
            round = math.floor
        
        size *= 1024
        peSize = self._peSize * 1024
        
        return long((round(size / pesize) * pesize) / 1024)

class LogicalVolume():
    _vg = None
    _name = ''
    _size = 0
    
    def __init__(self, name, volumeGroup, size):
        self._name =  name
        self._size = size
        self._vg.createLV(self)

    def create(self):
        pass
    
    def destroy(self):
        pass
    
    @property
    def path(self):
        pass
    
    @property
    def volumeGroup(self):
        return self._vg
    
    @property
    def size(self):
        return self._size
    
    @property
    def name(self):
        return self._name
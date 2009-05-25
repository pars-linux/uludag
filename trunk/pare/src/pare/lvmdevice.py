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

from pare.utils import lvm 
from pare.partition import LVM
import os
import pare.parteddata 


class PhysicalVolume():
    _type = physicalVolumeType
    _exists = False
    _vg = None
    _child = 0
    _partition = None
    
    def __init__(self, partition):
        self._exists = False
        self._partition =  partition
    
    def create(self):
        lvm.pvcreate(partition.path)
        self._exists = True
    
    def destroy(self):
        lvm.pvremove(partition.path)
    
    @property
    def exists(self):
       return (self._exists and os.path.exists("/dev/mapper/%s" % self._vg))

    def setupParent(self):
        if not self._partition.exists:
            self._partition.disk.setup()
         
    @property
    def parent(self):
        return  self._partition.path
    
    @property
    def addChild(self):
        self._child += 1
    
    def removeChild(self):
        self._child -= 1
         
class VolumeGroup():
    _type = volumeGroupType 
    _devBlockDir = "/dev/mapper"
    _name = ''
    _pvs = []
    _lvs = []
    _exists = False
    _peSize = 4.0
    _free = 0
    
    def __init__(self,name, physicalVolumes=None, peSize=None):
        self._isSetup = False
        self._name = name
        
        if physicalVolumes is not None:
            if isinstance(physicalVolumes, list):
                for pv in physicalVolumes:
                    self._pvs.append(pv)
                    pv.addChild()
              
    
    def addPV(self, pv):
        if isinstance(pv, PhysicalVolume):
            self._pvs.append(pv)
        
        pv.addChild()
    
    def removePV(self, pv):
        if isinstance(pv, PhysicalVolume):
            self._pvs.remove(pv)
            pv.removeChild()
    
    def addLV(self, logicalVolume):
        if logicalVolume in self._lvs:
            raise ValueError("Logical Volume is part of this Volume Group")
        
        #FIXME:Check Volume Group free size not smaller than logical volume requested size
    
    def removeLV(self, logicalVolume):
        pass
    
    def setupParents(self):
        for pv in self._pvs:
            pv.create()
    
    def create(self):
        self.createParents()
        pv_list = [pv.path for pv in self.pvs]
        lvm.vgcreate(self._name, pv_list, self._peSize)
        self._exists =True
        
    def destroy(self):
        lvm.vgreduce(self._name, [], rm=True)
        lvm.vgremove(self._name)
    
    def reduce(self, pvs):
        lvm.vgreduce(self._name, pvs)
    
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
    def pvs(self):
        return self._pvs[:]
    
    @property
    def lvs(self):
        return self._lvs[:]
    

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
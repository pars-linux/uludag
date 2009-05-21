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

class VolumeGroupDevice():
    _type = volumeGroupType 
    _devBlockDir = "/dev/mapper"
    _name = ''
    _pvs = []
    _lvs = []
    _exists = False
    _peSize = 4.0
    _free = 0
    
    def __init__(self,name, physicalVolumes=None, peSize=None):
        
        self._name = name
        if isinstance(physicalVolumes, list):
            for pv in physicalVolumes:
              self._pvs.append(pv)
              
    
    def _addPV(self, pv):
        if isinstance(pv, PhysicalVolume):
            self._pvs.append(pv)
        
        pv.addChild()
    
    def _removePV(self, pv):
        if isinstance(pv, PhysicalVolume):
            self._pvs.remove(pv)
        
        pv.removeChild()
    
    def _addLV(self):
        pass
    
    def _removeLV(self):
        pass
    
    def createParents(self):
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
    def status(self):
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
    
    @property
    def iscomplete(self):
        pass

class PhysicalVolume():
    _type = physicalVolumeType
    _exists = False
    _vg = None
    _child = 0
    
    def __init__(self, partition):
        pass
    
    def create(self):
        lvm.pvcreate(partition.path)
        self._exists = True
    
    def destroy(self):
        lvm.pvremove(partition.path)
    
    def status(self):
       return (self._exists and os.path.exists("/dev/mapper/%s" % self._vg))
    
    def addChild(self):
        self._child += 1
        
    def removeChild(self):
        self._child -= 1

# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
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
import yali4.lvmutils as lvm
from yali4.partition import LVMPartition
from yali4.parteddata import physicalVolume, volumeGroup, logicalVolume 
from yali4.exception import *


class PhysicalVolume(object):
    _type = physicalVolume
    
    def __init__(self, device, size, existing=0):
        """
            device   -- device node's basename
            peSize -- Physical extents size (in MB) Must be power of 2!
            existing -- indicates whether this is a existing device
            
        Existing PV
            
            size -- size of VG (in MB)
            uuid -- Physical Volume UUID
            peCount -- number of PE in this PV
            peFree -- number of free PE in this PV
        """
        
        self._exists = existing
        self._device = device
    
    @property
    def type(self):
        return self._type
    
    def setup(self):
        if self.exists:
            raise PhysicalVolumeError("Physical Volume already exists!")
        
        lvm.pvcreate(self.path)
        self._exists = True
        
    def destory(self):
        if not self.exists:
            raise PhysicalVolumeError("Physical Volume doesnt exists!")
        
        try:
            lvm.pvremove(self.path)
        except LVMError:
            raise PhysicalVolumeError("Couldnt destroy physical volume!")
        finally:
            self._exists = False

    @property
    def path(self):
        return self._device
    
    @property
    def exists(self):
        return self._exists

class VolumeGroup(object):
    _type = volumeGroup 
    _devBlockDir = "/dev" # FIXME:ReCheck VG path not to give acces_isSetups error

    def __init__(self, name, pvs=None, peSize=None, existing=0):

        """
            name -- device node's basename
            peSize -- Physical extents Size (in MB) Must be power power 2!
            existing -- indicates whether this is a existing device
            pvs -- a list of physical volumes. Parents of this VG
        """
        
        self._name = name
        self._pvs = pvs
        self._exists = existing

        if self._peSize is None:
            self._peSize = 4 # MB units 
        
    @property
    def type(self):
        return self._type
    
    def setup(self):
        if self.exists:
            raise VolumeGroupError("Device is already exist")
        
        for pv in self.pvs:
            if not pv.exists:
                pv.setup()
                
        lvm.vgcreate(self.name, pvs, self._peSize)
        self._exists =True

    def destroy(self):
        if not self.exists:
            raise LVMError("Volume Group doesnt exist!" , self.path)

        try:
            lvm.vgreduce(self.name, [], rm=True)
            lvm.vgremove(self.name)
        except LVMError:
            raise VolumeGroupError("Could not complete remove VG", self.path)
        finally:
            self._exists = False

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return "%s/%s" % (self._devBlockDir, self.name)

    @property
    def pvs(self):
        return self._pvs[:]
    
    @property
    def exists(self):
        return self._exists

    @property
    def size(self):
        size = 0
        for pv in self.pvs:
            size += pv.size

        return size


class LogicalVolume():
    _devBlockDir = "/dev/mapper"

    def __init__(self, name, vg, size=None, existing=0):
        if not isinstance(vg, VolumeGroup):
            raise ValueError("Requires a VolumeGroupDevice instance")
        
        self._name =  name
        self._vg = vg
        self._size = size
        self._exists = existing
        


    @property
    def type(self):
        return self._type
    
    def setup(self):
        if self.exists:
            raise LogicalVolumeError("logical volume already exists!")
        if not self.vg.exists:
            self.vg.setup()

        lvm.lvcreate(self.vg.name, self.name(), self.size)
        self._exists = True

    def destroy(self):
        if not self.exists:
            raise LogicalVolumeError("logical volume has not been created!",self.path)
        else:
            lvm.lvremove(self.vg.name, self.name())
            self._exists = False
            
    @property
    def exists(self):
        return self._exists

    @property
    def path(self):
        return "%s/%s-%s" % (self._devBlockDir, self.vg.name.replace("-", "--"), self.name().replace("-", "--"))
    
    def getPath(self):
        return self.path
    
    def getMB(self):
        return self.size
        
    @property
    def vg(self):
        return self._vg
    
    @property
    def size(self):
        return self._size
    
    @property
    def lvName(self):
        return "%s-%s" % (self.vg.name, self.name())

    def name(self):
        return self._name

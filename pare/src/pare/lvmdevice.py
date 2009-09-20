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
from pare.parteddata import physicalVolume, volumeGroup, logicalVolume 
from pare.errors import *

class PhysicalVolume(object):
    _type = physicalVolume

    def __init__(self, parent, size=None, uuid=None, peSize=None, peCount=None, peFree=None, existing=0):
        """
            name   -- device node's basename
            peSize -- Physical extents size (in MB) Must be power of 2!
            existing -- indicates whether this is a existing device

        Existing PV

            size -- size of VG (in MB)
            uuid -- Physical Volume UUID
            peCount -- number of PE in this PV
            peFree -- number of free PE in this PV
        """

        self._exists = existing
        self._parent = parent
        self._size = size
        self._uuid = uuid
        self._peSize = peSize
        self._peCount = peCount
        self._peFree = peFree

        if self._peSize is None:
            self._peSize = 4

    @property
    def type(self):
        return self._type

    def create(self):
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

    def setup(self):
        if self.exists:
            raise PhysicalVolumeError("Physical Volume already exists!")

        if not self._parent.status:
            self._parent.setup()

    def teardown(self):
        if not self.exists:
            raise PhysicalVolumeError("Physical Volume doesnt exists!")

        if self._parent.status:
            self._parent.teardown()

    @property
    def path(self):
        return self._parent.path

    @property
    def exists(self):
        return self._exists

    @property
    def status(self):
        if not self.exists:
            return False
        return os.access(self.path, os.W_OK)

    @property
    def freeExtents(self):
        return self._peFree

class VolumeGroup(object):
    _type = volumeGroup 
    _devBlockDir = "/dev" # FIXME:ReCheck VG path not to give acces_isSetups error
    _pvs = []
    _lvs = []
    _exists = None

    def __init__(self, name, size=None, uuid=None, 
                 pvs=None, maxPV=None, pvCount=None, 
                 peSize=None, peCount=None, peFree=None,
                 freespace=None, maxLV=None, existing=0):

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
        self._freeSpace = freespace
        self._maxLV = maxLV

        if pvs is not None:
            if isinstance(pvs, list):
                for pv in physicalVolumes:
                    self._pvs.append(pv)

        if self._peSize is None:
            self._peSize = 4 # MB units 

        self._update()

    def _update(self):
        lvs = lvm.lvlist(self.name)
        for lv in lvs:
            info = lvm.lvinfo("%s/%s" % (self.path, lv))
            if info:
                self._lvs.append(LogicalVolume(name=info['lv_name'], vg=self, size=info['lv_size'], uuid=info['lv_uuid'], existing=1))
    @property
    def type(self):
        return self._type

    def create(self):
        if self.exists:
            raise VolumeGroupError("Device is already exist")

        pvs = []
        for pv in self.pvs:
            if not pv.status:
                raise PhysicalVolumeError("Volume Group Physical doesnt exist!")
            else:
                pvs.append(pv)

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
        print "vg.setupParents"
        for parent in self.pvs:
            parent.setup()

    def setup(self):
        if not self.exists:
            raise VolumeGroupError("Volume Group has not been created!")

        if self.status:
            return

        if len(self.pvs) < self._pvCount:
            raise ValueError("Cannot activate Volume Group with missing PVs")

        self.setupParents()


    def teardown(self):
        if not self.exists:
            raise VolumeGroupError("Volume Group has not been created!")

        if self.status:
            lvm.vgdeactivate(self.name)

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
        return self._freeSpace

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
    _devBlockDir = "/dev/mapper"
    _vg = None

    def __init__(self, name, vg, size=None, uuid=None, format=None, existing=0):
        if isinstance(vg, list):
            if len(vg) != 1:
                raise ValueError("Requires a single VolumeGroupDevice instance")
            elif not isinstance(vg, VolumeGroup):
                raise ValueError("Requires a VolumeGroupDevice instance")
        elif not isinstance(vg, VolumeGroup):
            raise ValueError("Requires a VolumeGroupDevice instance")

        self._name =  name
        self._size = size
        self._uuid = uuid
        self._format = format
        self._exists = existing
        self._vg = vg

        if self._exists:
            self.vg.addLV(self)

    @property
    def type(self):
        return self._type
    
    def create(self):
        if self.exists:
            raise LogicalVolumeError("logical volume already exists!")
        #FIXME:fix self.setupParents()
        self.setupParents()

        lvm.lvcreate(self.vg.name, self.name, self.size)
        self._exists = True
        self.setup()

    def destroy(self):
        if not self.exists:
            #raise LogicalVolumeError("logical volume has not been created!",self.path)
            #It is a remove request
            self.vg.removeLV(self)
            return True
        elif self.exists and self.status:
            self.teardown()
            #Setup Parents( maybe raid parts) so lvm can remove lv
            #FIXME:fix self.setupParents()
            self.vg.setupParents()
            if lvm.lvremove(self.vg.name, self.name):
                self._exists = False
                return True
        return False

    def resize(self):
        if not self.exists:
            raise LogicalVolumeError("logical volume has not been created!",self.path)

        #May be vg has some raid parts
        self.vg.setupParents()

        if self.format.exists:
            self.format.teardown()

        #FIXME:add udev_settle()
        #udev_settle(timeout=10)

        lvm.lvresize(self.vg.name, self.name, self.size)


    @property
    def format(self):
        return self._format

    def setup(self):
        if not self.exists:
            raise LogicalVolumeError("logical volume has not been created!",self.path)

        if self.status:
            return

        self.setupParents()
        lvm.lvactivate(self.vg.name, self.name)

    def teardown(self):
        if not self.exists:
            raise LogicalVolumeError("logical volume has not been created!", self.path)

        #FIXME:Add exists func to filesystem to check if filesystem mounted
        #FIXME:Add teardown and setup fun c to filesystem to mount or unmount system
        if self.status and self.format and self.format.exists:
            self.format.teardown()

        if self.status:
            print "Burada"
            lvm.lvdeactivate(self.vg, self.name)

    def setupParents(self):
        self.vg.setup() 

    @property
    def exists(self):
        return self._exists

    @property
    def status(self):
        #if not self.exists:
        #    return False
        return os.access(self.path, os.W_OK)

    @property
    def path(self):
        return "%s/%s-%s" % (self._devBlockDir, self.vg.name.replace("-", "--"), self.name.replace("-", "--"))

    @property
    def vg(self):
        return self._vg

    def _setSize(self, size):
        size = self.vg._align(size)
        if size <= (self.vg.freeSpace + self._size):
            self._size = size
        else:
            raise ValueError("not enough free space in VG")

    def _getSize(self):
        return self._size

    size = property(lambda p: p._getSize(), lambda pi,f: p._setSize(f))

    @property
    def lvName(self):
        return "%s-%s" % (self.vg.name, self.name)

    @property
    def name(self):
        return self._name

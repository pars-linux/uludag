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

# partitionrequest.py defines requests (format, mount) on the partitions.

import os

import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

from yali4.exception import *
from yali4.constants import consts
import yali4.lvm as lvm
import yali4.sysutils

class RequestException(YaliException):
    pass

# poor man's enum ;)

REQUEST_FORMAT, REQUEST_MOUNT, REQUEST_LABEL, REQUEST_SWAP_AS_FILE, REQUEST_PHYSICAL_VOLUME, REQUEST_VOLUME_GROUP, REQUEST_LOGICAL_VOLUME= range(5)

##
# requests object holds the list of requests
class RequestList(list):

    ##
    # apply all requests
    def applyAll(self):
        pass
    def searchPartAndReqTypeIterate(self, p, rt):
        i = self.__iter__()
        try:
            cur = i.next()
            while True:
                if cur.partition().getPath() == p.getPath() and cur.requestType() == rt:
                    # FOUND
                    yield cur

                cur = i.next()
        except StopIteration:
            # end of list
            pass

    ##
    # function searches for a request by partition and request type
    #
    # @return: [Partition]
    #
    # @param p: Partition (defined in partition.py)
    # @param t: request Type (eg. formatRequestType)
    def searchPartAndReqType(self, p, rt):
        req = [x for x in self.searchPartAndReqTypeIterate(p, rt)]
        return req


    ##
    # Iterator function searches for a request 
    # by request type
    #
    # @return: generator returns a request type in each turn.
    #
    # @param t: request Type (eg. formatRequestType)
    def searchReqTypeIterate(self, rt):
        i = self.__iter__()
        try:
            cur = i.next()
            while True:
                if cur.requestType() == rt:
                    # FOUND
                    yield cur

                cur = i.next()
        except StopIteration:
            # end of list
            pass


    ##
    # Iterator function searches by partition type and request type
    #
    # @return: generator returns a request type in each turn.
    #
    # @param pt: Partition Type (defined in partitiontype.py)
    # @param rt: Request Type
    def searchPartTypeAndReqTypeIterate(self, pt, rt):
        i = self.__iter__()
        try:
            cur = i.next()
            while True:
                if cur.partitionType() == pt and cur.requestType() == rt:
                    # FOUND
                    yield cur

                cur = i.next()
        except StopIteration:
            # end of list
            pass


    ##
    # Search for a given partition type and request type.
    #
    # @return: if found returns the PartRequest else None.
    #
    # @param pt: Partition Type (defined in partitiontype.py)
    # @param rt: Request Type
    def searchPartTypeAndReqType(self, pt, rt):
        req = [x for x in self.searchPartTypeAndReqTypeIterate(pt, rt)]
        # this should give (at most) one result
        # cause we are storing one request for a partitionType()
        assert(len(req) <= 1)

        if not req:
            return None
        else:
            # return the only request found.
            return req.pop()


    ##
    # add/append a request
    def append(self, req):
        self.removeRequest(req.partition(), req.requestType())

        rt = req.requestType()
        pt = req.partitionType()
        found = self.searchPartTypeAndReqType(pt, rt)

        # RequestList stores only one request for a requestType() -
        # partitionType() pair.
        if found:
            e = _("There is a request for the same Partition Type.")
            raise RequestException, e

        list.append(self, req)


    ##
    # remove request matching (partition, request type) pair
    # @param p: Partition
    # @param t: request Type (eg. formatRequestType)
    def removeRequest(self, p, rt):
        found = [x for x in self.searchPartAndReqTypeIterate(p, rt)]
        # this should give (at most) one result
        # cause we are storing one request for a (part, reqType) pair
        assert(len(found) <= 1)

        for f in found:
            self.remove(f)


    ##
    # remove a request
    def remove(self, i):
        list.remove(self, i)


    ##
    # remove all requests
    def remove_all(self):
        def _iter_remove():
            i = self.__iter__()
            try:
                while True:
                    cur = i.next()
                    self.remove(cur)
            except StopIteration:
                # end of list
                pass

        # the code above doesn't removes all. so bruteforce it...
        while True:
            if len(self):
                _iter_remove()
            else:
                return

uniqueId = 0
def uniqueID():
    global uniqueId
    return uniqueId+1
##
# Abstract Partition request class
class RequestSpec:  
    def __init__(self, device, requesttype=None, existing=0):
        self._requestID = uniqueID()
        self._device = device
        self._requestType = requesttype
        self._preexists = existing
        self._isapplied = False   
        self.dev = None    
    ##
    # apply the request to the partition
    def apply(self):
        self._isapplied = True

    
    @property
    def isApplied(self):
        return self._isapplied
    
    @property
    def id(self):
        return self._requestID
    
    @property
    def type(self):
        return self._requestType
    
    @property
    def exists(self):
        return self._preexists
    
    def device(self):
        pass
    def __str__(self):
        pass
    
    
class FormatRequest(RequestSpec):
    
    def __init__(self, device, filesystem, preexist=0):
        
        RequestSpec.__init__(self, device=device, requesttype=REQUEST_FORMAT, existing=preexist)
        self._filesystem = filesystem
        
    @property
    def device(self):
        if self.dev:
            for dev in yali4.storage.devices:
                if dev.getPath() == self._device[0:-1]:
                    self.dev = dev.getPartition(self._device[-1])
        
        return self.dev
            
    def apply(self):
        fs = self._filesystem
        fs.format(self.device)
        
        RequestSpec.apply(self)


class MountRequest(RequestSpec):
    
    def __init__(self, device, filesystem, mountpoint, needsmtab, preexist=0):
        
        RequestSpec.__init__(self, device=device, requesttype=REQUEST_MOUNT, existing=preexist)
        self._filesystem = filesystem
        self._mountpoint = mountpoint
        self._needsMTAB = needsmtab
        
    @property
    def device(self):
        if self.dev:
            for dev in yali4.storage.devices:
                if dev.getPath() == self._device[0:-1]:
                    self.dev = dev.getPartition(self._device[-1])
        
        return self.dev
            
    def apply(self):
        if not self._mountpoint: # do nothing
            return

        source = self.device.getPath()
        target = consts.target_dir + self._mountpoint
        filesystem = self._filesystem._sysname or self._filesystem._name

        if not os.path.isdir(target):
            os.makedirs(target)

        params = ["-t", filesystem, source, target]
        if not self._needsMTAB:
            params.insert(0,"-n")

        yali4.sysutils.run("mount", params)
        
        RequestSpec.apply(self)

class LabelRequest(RequestSpec):
    
    def __init__(self, device, filesystem, label, preexist=0):
        RequestSpec.__init__(self, device, requesttype=REQUEST_LABEL, existing=preexist)
        self._filesystem = filesystem
        self._label = label
    
    @property
    def device(self):
        if self.dev:
            for dev in yali4.storage.devices:
                if dev.getPath() == self._device[0:-1]:
                    self.dev = dev.getPartition(self._device[-1])
        
        return self.dev
    
    def apply(self):
        if not self._label:
            return

        label = self._filesystem.setLabel(self.device, self._label)
        self.device.setTempLabel(label)

        RequestSpec.apply(self)
        
##
# swap file request
class SwapFileRequest(RequestSpec):

    def __init__(self,):
        RequestSpec.__init__(self, requesttype=REQUEST_SWAP_AS_FILE)
        

    def __str__(self):
        pass
    
    def apply(self):

        # see #832
        if yali4.sysutils.mem_total() > 512:
            yali4.sysutils.swap_as_file(consts.swap_file_path, 300)
        else:
            yali4.sysutils.swap_as_file(consts.swap_file_path, 600)

        yali4.sysutils.swap_on(consts.swap_file_path)

        RequestSpec.apply(self)


class PhysicalVolumeRequest(RequestSpec):
    def __init__(self, device, size, preexist=0):
        RequestSpec.__init__(self, requesttype=REQUEST_PHYSICAL_VOLUME, filesystem=fs("lvm"), existing=preexist)
        self._size = size
        self._device = device
        
    def __str__(self):
        pass
    
    def device(self):
        if self.dev:
            return self.dev
        
        self.dev = lvm.PhysicalVolume(self._device, self._size, existing=self.exists)
        
        return self.dev
    
    def apply(self):
        self.device.setup()
    
class VolumeGroupRequest(RequestSpec):
    
    def __init__(self, device, pvs = None, peSize=4, preexist=0, preexist_size=0):
        RequestSpec.__init__(self, fs=fs("lvm"), existing=preexists)
        
        self._device = device
        self._pvs = pvs
        self._peSize = peSize
        self._free
        
        if self.exist and preexist_size:
            self._preexist_size = preexist_size
        else:
            self._preexist_size = None
    
    def __str__(self):
        pass

    
    def device(self, partitions):
        if self.dev:
            return self.dev
        pvs = []
        for pv in self._pvs:
            _pv = partitions.getRequestByID(pv)
            if (_pv.size > 0) or (_pv.device is not None):
                pvs.append(_pv.device)
        
        self.dev = lvm.VolumeGroup(self._device, pvs=pvs, peSize=self._peSize, existing=self.exist)
        
    def apply(self):
        self.__device.setup()


class LogicalVolumeRequest(RequestSpec):
    
    def __init__(self, device, volumeGroup,size, filesystem=None, filesystemlabel=None, mountpoint=None, isformat=None, existing=0):
        RequestSpec.__init__(self, requesttype=REQUEST_LOGICAL_VOLUME, filesystem=filesystem, filesystemlabel=filesystemlabel, mountpoint=mountpoint, isformat=isformat, existing=existing)
        
        self._device = device
        self._volumeGroup = volumeGroup
        self._size = size 
        
    def __str__(self):
        passs
    
    def device(self, partitions):
        vg = partitions.getRequestByID(self._volumeGroup)
        self.dev = lvm.LogicalVolume(self._device, vg, self._size, existing=self.exists)
        
        return self.dev
        
    def apply(self):
        self.device.setup()
    
    
# partition requests singleton.
partrequests = RequestList()


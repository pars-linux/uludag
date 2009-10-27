# -*- coding: utf-8 -*-
#
# Copyright (C) TUBITAK/UEKAE
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
import yali4.partitiontype as parttype
import yali4.sysutils
import yali4.raid

class RequestException(YaliException):
    pass

# poor man's enum ;)
formatRequestType, mountRequestType, \
    swapFileRequestType, labelRequestType, \
    raidRequestType = range(5)

##
# requests object holds the list of requests
class RequestList(list):

    ##
    # apply all requests
    def applyAll(self):

        # first apply format requests
        for r in self.searchReqTypeIterate(formatRequestType):
            r.applyRequest()

        # label filesystems
        for r in self.searchReqTypeIterate(labelRequestType):
            r.applyRequest()

        # we need to trigger udev for our new labels
        yali4.sysutils.run("/sbin/udevtrigger")
        yali4.sysutils.run("/sbin/udevsettle", "--timeout=180")


        # then mount request
        # but mount root (/) first
        pt = parttype.root
        rootreq = self.searchPartTypeAndReqType(pt, mountRequestType)
        if not rootreq:
            raise RequestException, "Desired partition request not found: root partition request."
        rootreq.applyRequest()

        # mount others
        for r in self.searchReqTypeIterate(mountRequestType):
            if r.partitionType() != rootreq.partitionType():
                r.applyRequest()

        # apply swap requests if any...
        for r in self.searchReqTypeIterate(swapFileRequestType):
            r.applyRequest()


    ##
    # iterator function searches for a request by partition and
    # request type
    #
    # @return: generator returns a request type in each turn.
    #
    # @param p: Partition (defined in partition.py)
    # @param t: request Type (eg. formatRequestType)
    def searchPartAndReqTypeIterate(self, p, rt):
        i = self.__iter__()
        try:
            cur = i.next()
            while True:
                if cur.partition() == p and cur.requestType() == rt:
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
        reqList = []
        for x in self.searchPartTypeAndReqTypeIterate(pt, rt):
            # if request type is a custom request type
            # we'll allow multiple pt/rt instances
            reqList.append(x)
            if ( x.requestType() in range(4) ):
                # this should give (at most) one result
                # cause we are storing one request for a partitionType()
                assert(len(reqList) <= 1)
        return reqList

    ##
    # add/append a request
    def append(self, req):
        # whats this for ?
        self.removeRequest(req.partition(), req.requestType())

        rt = req.requestType()
        pt = req.partitionType()
        found = self.searchPartTypeAndReqType(pt, rt)

        # RequestList stores only one request for a 
        # requestType() - partitionType() pair for root, home and swap partitions
        # RequestList stores one request for a partition
        
        if found:
            # deneme
            if ( pt.parttype in ["root", "home", "swap", "archive"] ):
                # request - type pair that should exist once
                e = _("There is already this request for %s partition" % pt.parttype)
                raise RequestException, e
            for request in found:
                # now check if there's the same request for this partition
                # example, a format request on a partition
                f = searchPartAndReqType(req.partition(), rt)
                if f:
                    e = _("There is already this request for this partition")
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


##
# Abstract Partition request class
class PartRequest:

    ##
    # empty initializeer
    def __init__(self):
        self._partition = None
        self._partition_type = None
        self._request_type = None
        self._isapplied = False

    ##
    # apply the request to the partition
    def applyRequest(self):
        self._isapplied = True

    ##
    # is the request applied on partition?
    def isApplied(self):
        return self._isapplied

    ##
    # set the partition to apply request
    def setPartition(self, partition):
        self._partition = partition

    ##
    # get partition
    def partition(self):
        return self._partition

    ##
    # set the type of the request
    def setRequestType(self, t):
        self._request_type = t

    ##
    # get the type of the request
    def requestType(self):
        return self._request_type

    ##
    # set partition type
    def setPartitionType(self, t):
        self._partition_type = t

    ##
    # get partition type
    def partitionType(self):
        return self._partition_type


##
# format partition request
class FormatRequest(PartRequest):

    ##
    # initialize format request
    # @param partition: Partition
    # @param part_type: partition type (defined in partitiontype.py)
    def __init__(self, partition, part_type):
        PartRequest.__init__(self)

        self.setPartition(partition)
        self.setPartitionType(part_type)
        self.setRequestType(formatRequestType)

    def applyRequest(self):
        t = self.partitionType()
        fs = t.filesystem
        fs.format(self.partition())

        PartRequest.applyRequest(self)


##
# mount partition request
class MountRequest(PartRequest):

    _options = ""

    def __init__(self, partition, part_type, options=None):
        PartRequest.__init__(self)

        self.setPartition(partition)
        self.setPartitionType(part_type)
        self.setRequestType(mountRequestType)

        self._options = options

    def applyRequest(self):

        pt = self.partitionType()

        if not pt.mountpoint: # do nothing
            return

        source = self.partition().getPath()
        target = consts.target_dir + pt.mountpoint
        filesystem = self.partition().getFSName()

        # print ">>>>>>",target
        if not os.path.isdir(target):
            os.makedirs(target)

        yali4.sysutils.mount(source, target, filesystem)


        if pt.needsmtab:
            mtab_entry = "%s %s %s rw 0 0\n" % (source,
                                                target,
                                                filesystem)
            open("/etc/mtab", "a").write(mtab_entry)

        PartRequest.applyRequest(self)


##
# swap file request
class SwapFileRequest(PartRequest):

    def __init__(self, partition, part_type):
        PartRequest.__init__(self)

        self.setPartition(partition)
        self.setPartitionType(part_type)
        self.setRequestType(swapFileRequestType)


    def applyRequest(self):

        # see #832
        if yali4.sysutils.mem_total() > 512:
            yali4.sysutils.swap_as_file(consts.swap_file_path, 300)
        else:
            yali4.sysutils.swap_as_file(consts.swap_file_path, 600)

        PartRequest.applyRequest(self)


##
# partition/filesystem labeling request
class LabelRequest(PartRequest):

    def __init__(self, partition, part_type):
        PartRequest.__init__(self)

        self.setPartition(partition)
        self.setPartitionType(part_type)
        self.setRequestType(labelRequestType)

    def applyRequest(self):

        pt = self.partitionType()
        if not pt.label:
            return
        pt.filesystem.setLabel(self.partition(), pt.label)

        PartRequest.applyRequest(self)

##
# raid partition request
class RaidRequest(PartRequest):
    def __init__(self, partition, part_type):
        PartRequest.__init__(self)
        self.setPartition(partition)
        self.setPartitionType(part_type)
        self.setRequestType(raidRequestType)
    def applyRequest(self):
        pass
        # PartRequest.applyRequest(self)

##
# @param drive is the drive to remove
# @param start is the start sector of deleted partition
# @param end is the end sector of deleted partition
class DeletePartitionRequest:
    """ A preexisting partition which will be removed """
    def __init__(self, drive, start, end):
        self.drive = drive
        self.start = start
        self.end = end

class DeleteRaidRequest:
    """ A preexisting Raid device which will be removed """
    def __init__(self, minor):
        self.minor = minor

# partition requests singleton.
partrequests = RequestList()


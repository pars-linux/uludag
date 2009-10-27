# -*- coding: utf-8 -*-
#
# Copyright (C) TUBITAK/UEKAE
# Copyright 2001 - 2004 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

def getRaidLevels():
    avail = []
    try:
        f = open("/proc/mdstat", "r")
    except:
        pass
    else:
        for l in f.readlines():
            if not l.startswith("Personalities"):
                continue

            lst = l.split()

            for lev in ["RAID0", "RAID1", "RAID5", "RAID6", "RAID10", "linear"]:
                if "[" + lev + "]" in lst or "[" + lev.lower() + "]" in lst:
                    avail.append(lev)

        f.close()

    avail.sort()
    return avail

availRaidLevels = getRaidLevels()

import parted, os
import yali4.partedutils
import yali4.mdutils
import yali4.storage

# these arches can have their /boot on RAID
# only raid1 works for boot partitions
raidBootArches = [ "x86", "amd64", "ppc" ]

def scanForRaid():
    """ Scans for raid devices on drives list.
        Returns the tuple ( mdMinor, devices, level, totalDisks )
    """
    raidSets = {}
    raidDevices = {}
     
    devs = yali4.storage.detect_devices()
    
    for i in devs:
        try:
            dev = parted.PedDevice.get(i)
            disk = parted.PedDisk.new(dev)
        except:
            print "parted error handling %s" % i
        
        parts = []
        
        try:
            raidParts = yali4.partedutils.get_raid_partitions(disk)
            for part in raidParts:
                parts.append(yali4.partedutils.get_partition_name(part))
        except:
            pass
        
        for dev in parts:
            try:
                (major, minor, raidSet, level, nrDisks, totalDisks, mdMinor) = yali4.mdutils.raidsbFromDevice("/dev/%s"%dev)
            except ValueError:
                print "reading raid superblock failed for %s", dev
                continue
            
            if raidSets.has_key(raidSet):
                (knownLevel, knownDisks, knownMinor, knownDevices) = raidSets[raidSet]
                
                if knownLevel != level or knownDisks != totalDisks or knownMinor != mdMinor:
                    print " raid set inconsistency for md%d: " \
                          "all drives in this raid set do not " \
                          "agree on raid parameters. Skipping raid device" % mdMinor
                    continue

                knownDevices.append(dev)
                raidSets[raidSet] = (knownLevel, knownDisks, knownMinor, knownDevices)
            else:
                raidSets[raidSet] = (level, totalDisks, mdMinor, [dev,])
                
            if raidDevices.has_key( mdMinor ):
                if( raidDevices[mdMinor] != raidSet ):
                    print "raid set inconsistency for md%d: "\
                          "found members of multiple raid sets "\
                          "that claims to be md%d. Using only the first "\
                          "array found." % (mdMinor, mdMinor)
                    continue
            else:
                raidDevices[mdMinor] = raidSet

    raidList = []

    for key in raidSets.keys():
        (level, totalDisks, mdMinor, devices) = raidSets[key]
        if len(devices) < totalDisks:
            print "missing components of raid device md%d.\n The " \
                  "raid device needs %d drive(s) and only %d (was/were) " \
                  "found. \nThis raid device will not be started." % (mdMinor, totalDisks, len(devices))
            continue
        raidList.append((mdMinor, devices, level, totalDisks))

    return raidList

def startAllRaid(dev_list=None):
    """ Give a startraid on raid devices """
    if dev_list:
        for mdDevice, deviceList, level, numActive in dev_list:
            yali4.mdutils.raidstart("md%d"%mdDevice, deviceList[0])

def stopAllRaid(dev_list=None):
    """ Stop all raid devices in tuple dev_list """
    if dev_list:
        for dev, devices, level, numActive in dev_list:
            yali4.mdutils.raidstop(dev.split('/')[-1:][0])

def isRaid10(raidlevel):
    """ Return whether raidlevel is a valid descriptor of RAID10. """
    if raidlevel in ("RAID10", "10", 10):
        return True
    return False

def isRaid6(raidlevel):
    """ Return whether raidlevel is a valid descriptor of RAID6. """
    if raidlevel in ("RAID6", "6", 6):
        return True
    return False

def isRaid5(raidlevel):
    """ Return whether raidlevel is a valid descriptor of RAID5. """
    if raidlevel in ("RAID5", "5", 5):
        return True
    return False

def isRaid1(raidlevel):
    """ Return whether raidlevel is a valid descriptor of RAID1. """
    if raidlevel in ("mirror", "RAID1", "1", 1):
        return True
    return False

def isRaid0(raidlevel):
    """ Return whether raidlevel is a valid descriptor of RAID0. """
    if raidlevel in ("stripe", "RAID0", "0", 0):
        return True
    return False

def isLinear(raidlevel):
    """ Return whether raidlevel is a valid descriptor of linear raid """
    if raidlevel == "linear":
        return True
    return False

def get_raid_min_members(raidlevel):
    """ Return the minimum number of raid members required for raid level """
    if isRaid0(raidlevel):
        return 2
    elif isRaid1(raidlevel):
        return 2
    elif isLinear(raidlevel):
        return 2
    elif isRaid5(raidlevel):
        return 3
    elif isRaid6(raidlevel):
        return 4
    elif isRaid10(raidlevel):
        return 4
    else:
        raise ValueError, "invalid raidlevel in get_raid_min_members"

def get_raid_max_spares(raidlevel, nummembers):
    """ Return the max number of raid spares for raidlevel """
    if isRaid0(raidlevel):
        return 0
    elif isRaid1(raidlevel) or isRaid5(raidlevel) or \
            isRaid6(raidlevel) or isRaid10(raidlevel) or isLinear(raidlevel):
        return max(0, nummembers - get_raid_min_members(raidlevel))
    else:
        raise ValueError, "invalid raidlevel in get_raid_max_spares"


def lookup_raid_device(mdname, raidList=None):
    """ Return raid device information """
    if not raidList:
        rl = scanForRaid()
    else:
        rl = raidList
    for dev, devices, level, numActive in rl:
        if mdname == "md%d"%dev:
            return (dev, devices, level, numActive)
    raise KeyError, "md device not found"

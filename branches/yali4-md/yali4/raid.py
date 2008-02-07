# -*- coding: utf-8 -*-
#
# Copyright (C) 2008, TUBITAK/UEKAE
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

import parted
import partedutils
import os
import mdutils
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

    if not yali4.storage.devices:
        yali4.storage.init_devices()
    devs = yali4.storage.devices

    for d in devs:
        # scan for Device objects
        parts = []
        try:
            raidParts = partedutils.get_raid_partitions(d._disk)
            for part in raidParts:
                parts.append(partedutils.get_partition_name(part))
        except:
            pass

        # now parts is a list of raid partitions on disk d like 'hdc5','hdc6' ..
        for dev in parts:
            try:
                # get the superblock from raid device
                (major, minor, raidSet, level, nrDisks, totalDisks, mdMinor) = mdutils.raidsbFromDevice("/dev/%s"%dev)
            except ValueError:
                # cant be part of raid set
                print "reading raid sb failed for %s", dev
                continue

            if raidSets.has_key(raidSet):
                (knownLevel, knownDisks, knownMinor, knownDevices) = raidSets[raidSet]

                if knownLevel != level or knownDisks != totalDisks or knownMinor != mdMinor:
                    print " raid set inconsistency for md%d: "\
                          "all drives in this raid set do not ",\
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
                      "array found.", mdMinor, mdMinor
                    continue
            else:
                raidDevices[mdMinor] = raidSet

    raidList = []

    for key in raidSets.keys():
        (level, totalDisks, mdMinor, devices) = raidSets[key]
        if len(devices) < totalDisks:
            print "missing components of raid device md%d. The "\
                  "raid device needs %d drive(s) and only %d (was/were) "\
                  "found. This raid device will not be started.", mdMinor, totalDisks, len(devices)
            continue
        raidList.append((mdMinor, devices, level, totalDisks))

    return raidList

def startAllRaid():
    """ Start raid on raid devices, returns same struct as scanForRaid """
    rc = []
    mdList = scanForRaid()
    for mdDevice, deviceList, level, numActive in mdList:
        devName = "md%d" % (mdDevice,)
        mdutils.raidstart(devName, deviceList[0])
        rc.append((devName, deviceList, level, numActive))
    return rc

def stopAllRaid(mdList):
    """ Stop all raid devices in tuple mdList """
    for dev, devices, level, numActive in mdList:
        mdutils.raidstop(dev)

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




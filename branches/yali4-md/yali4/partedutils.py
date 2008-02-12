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

import os, sys
import string
import os.path
import subprocess
import parted

import yali4.mdutils

def get_partition_name(partition):
    """ Return the device name for the PedPartition partition """
    if( partition.geom.dev.type == parted.DEVICE_DAC960
        or partition.geom.dev.type == parted.DEVICE_CPQARRAY ):
        return "%sp%d" % ( partition.geom.dev.path[5:],
                           partition.num )

    if( parted.__dict__.has_key("DEVICE_SX8") and
        partition.geom.dev.type == parted.DEVICE_SX8 ):
        return "%sp%d" % ( partition.geom.dev.path[5:],
                           partition.num )

    drive = partition.geom.dev.path[5:]
    if( drive.startswith("cciss") or drive.startswith("ida") or
        drive.startswith("rd") or drive.startswith("sx8") or
        drive.startswith("mapper") ):
        sep = "p"
    else:
        sep = ""
    return "%s%s%d" % (partition.geom.dev.path[5:], sep, partition.num)

# filter disks in a PedDisk obj with function func
def filter_partitions(disk, func):
    rc = []
    part = disk.next_partition()
    while part:
        if func(part):
            rc.append(part)
        part = disk.next_partition(part)

    return rc

# @param disk is parted.PedDisk obj
def get_raid_partitions(disk):
    """ Return a list of RAID-type PedPartition objects on disk. """
    func = lambda part: (part.is_active()
                         and part.get_flag( parted.PARTITION_RAID ) == 1)
    return filter_partitions(disk, func)

# returns raid info for drives
# if its raidDevice itself, instead of members, call with raidDevice=True
def _getRaidInfo(drive, raidDevice=False):
    try:
        if raidDevice:
            lines = yali4.mdutils._mdadm("--detail", drive)
        else:
            lines = yali4.mdutils._mdadm("-E", drive)
    except yali4.mdutils.MdadmError:
        ei = sys.exc_info()
        ei[1].name = drive
        raise ei[0], ei[1], ei[2]

    info = {
        'major': "-1",
        'minor': "-1",
        'uuid' : "",
        'level': -1,
        'nrDisks': -1,
        'totalDisks': -1,
        'mdMinor': -1,
    }

    for line in lines:
        vals = string.split(string.strip(line), ' : ')
        if len(vals) != 2:
            continue
        if vals[0] == "Version":
            vals = string.split( vals[1], ".")
            info['major'] = vals[0]
            info['minor'] = vals[1]
        elif vals[0] == "UUID":
            info['uuid'] = vals[1]
        elif vals[0] == "Raid Level":
            if vals[1] != "linear":
                info['level'] = int(vals[1][4:])
            else:
                info['level'] = vals[1]
        elif vals[0] == "Raid Devices":
            info['nrDisks'] = int(vals[1])
        elif vals[0] == "Total Devices":
            info['totalDisks'] = int(vals[1])
        elif vals[0] == "Preferred Minor":
            info['mdMinor'] = int(vals[1])
        else:
            continue

    if info['uuid'] == "":
        raise ValueError, info

    return info



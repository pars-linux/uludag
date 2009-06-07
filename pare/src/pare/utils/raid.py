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

from errors import MDRaidError
import logging
import sysutils

log = logging.getLogger("storage")

#Raid levels

RAID0 = 0
RAID1 = 1
RAID5 = 5
RAID6 = 6
RAID10 = 10

def getRaidLevels():
    avail = []

    try:
        file = open("/proc/mdstat", "r")
    except IOError:
        pass
    else:
        for line in file.readlines():
            if not line.startswith("Personalities"):
                continue
            _list = line.split()

            for level in ["RAID0" , "RAID1" , "RAID5" , "RAID6" , "RAID10"]:
                if "[" + level + "]" in _list or "[" + level.lower() + "]" in _list:
                    avail.append(level)

        file.close()

    avail.sort()

    return avail

raidlevels = getRaidLevels()

def isRaid(raid, raidlevel):
    """Return whether level is a valid descriptor of raid"""

    descriptor = {RAID10:("RAID10" , "10" , 10),
                  RAID6:("RAID6" , "6" , 6),
                  RAID5:("RAID5" , "5" , 5),
                  mirror:("RAID1" , "1" ,1),
                  stripe:("RAID0", "0" , 0)
                }

    if raid in descriptor:
        return raidlevel in descriptor[raid]
    else:
        raise ValueError, "invalid raid level %d" % raid

def getRaidMinimumMembers(raidlevel):
    """Return the minumum number of raid members required for raid level"""

    minumum_members = {RAID10: 2,
                       RAID6: 4,
                       RAID5: 3,
                       RAID1: 2,
                       RAID0: 2}

    for raid, min_members in minumum_members.items():
        if isRaid(raid, raidlevel):
            return min_members

    raise ValueError, "invalid raid level %d " % raidlevel

def getRaidMaxSpares(raidlevel, member_num):
    """Return the maximum number of raid spares for raid level"""

    max_spares = {RAID10: lambda: max(0, member_num - getRaidMinimumMembers(RAID10)),
                  RAID6: lambda: max(0, member_num - getRaidMinimumMembers(RAID6)),
                  RAID5: lambda: max(0, member_num - getRaidMinimumMembers(RAID5)),
                  RAID1: lambda: max(0, member_num - getRaidMinimumMembers(RAID1)),
                  RAID0: lambda: 0}

    for raid, max_spares_function in max_spares.items():
        if isRaid(raid, raidlevel):
            return max_spares_function()

    raise ValueError, "invalid raid level %d" % raidlevel


def create(device, level, disks, spares=0):
    """Create MdRaid device"""

    argv = ["--create", device, "--run", "--levels=%s" % level]
    raid_devs = len(disks) - spares

    argv.append("--raid-devices=%d" % raid_devs)
    if spares:
        argv.append("--spare-devices=%d" % spares)

    return_code  = sysutils.execClear("mdadm", argv, stdout="/dev/tty5", stderr="/dev/tty5")

    if return_code == 0:
        raise MDRaidError("raid.create failed for %s" % device)

def destroy(device):
    return_code = sysutils.execClear("mdadm",
                                ["--zero-sperblock", device],
                                stdout="/dev/tty5",
                                stderr="/dev/tty5")

    if return_code == 0:
        raise MDRaidError("raid.destroy failed for %s" % device)

def add(device):
    return_code = sysutils.execClear("mdadm",
                                 ["--incremental",
                                  "--quiet",
                                  "--auto=md",
                                  device],
                                 stderr = "/dev/tty5",
                                 stdout = "/dev/tty5")
    if return_code:
        raise MDRaidError("raid.add failed for %s" % device)

def activate(device, members=[], super_minor=None, uuid=None):
    if super_minor is None and not uuid:
        raise ValueError("raid.activate requires either a uuid or a super-minor")

    if uuid:
        identifier = "--uuid=%s" % uuid
    elif super_minor is not None:
        identifier = "--super-minor=%d" % super_minor
    else:
        identifier = ""

    return_code = sysutils.execClear("mdadm",
                                ["--assemble",
                                 device,
                                 identifier,
                                 "--auto=md",
                                 "--update=super-minor"] + members,
                                stderr = "/dev/tty5",
                                stdout = "/dev/tty5")

    if return_code:
        raise MDRaidError("raid.activate failed for %s" % device)

def deactivate(device):
    return_code = sysutils.execClear("mdadm",
                                ["--stop", device],
                                stderr = "/dev/tty5",
                                stdout = "/dev/tty5")

    if return_code:
        raise MDRaidError("raid.deactivate failed for %s" % device)
    
def examine(device):
    # XXX NOTUSED: we grab metadata from udev, which ran 'mdadm -E --export'
    #
    # FIXME: this will not work with version >= 1 metadata
    #
    # We should use mdadm -Eb or mdadm -E --export for a more easily
    # parsed output format.
    lines =   sysutils.execWithCapture("mdadm",
                                  ["--examine", device],
                                  stderr="/dev/tty5").splitlines()

    info =  {
            'major': "-1",
            'minor': "-1",
            'uuid' : "",
            'level': -1,
            'nrDisks': -1,
            'totalDisks': -1,
            'mdMinor': -1,
            }

    for line in lines:
        (key, sep, val) = line.strip().partition(" : ")
        if not sep:
            continue
        if key == "Version":
            (major, sep, minor) = val.partition(".")
            info['major'] = major
            info['minor'] = minor
        elif key == "UUID":
            info['uuid'] = val.split()[0]
        elif key == "Raid Level":
            info['level'] = int(val[4:])
        elif key == "Raid Devices":
            info['nrDisks'] = int(val)
        elif key == "Total Devices":
            info['totalDisks'] = int(val)
        elif key == "Preferred Minor":
            info['mdMinor'] = int(val)
        else:
            continue

    if not info['uuid']:
        raise MDRaidError("UUID missing from device info")

    return info

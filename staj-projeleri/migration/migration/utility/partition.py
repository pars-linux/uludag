#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

import os

import registry

def getPartitions():
    "get all partitions in the form: '/mnt/hda9'"
    partitions=[]
    try:
        f = open("/proc/mounts")
    except:
        return []
    for line in f:
        part = line.split(" ")
        if not len(part) == 6:
            continue
        mountdir = part[1]
        if os.access(mountdir, os.R_OK):
            partitions.append(mountdir)
    return partitions

def isWindowsPart(partition):
    "Checks which partitions have windows installed"
    possible_files=["boot.ini","command.com","bootmgr"]
    for a in possible_files:
        if os.path.exists(os.path.join(partition,a)):
            return True
    return False

def getWindowsUsers(partition):
    "Returns regular users in the partition which has windows installed"
    users = []      # User: (partition, parttype, username, userdir)
    # Try to find a hive file which includes software information:
    possiblehivefiles = ["Windows/System32/config/SOFTWARE", "WINDOWS/system32/config/software"]
    hivefile = ""
    for possiblehivefile in possiblehivefiles:
        possiblehivefile = os.path.join(partition,possiblehivefile)
        if os.path.isfile(possiblehivefile):
            hivefile = possiblehivefile
            break
    # If found, get users:
    if hivefile != "":
        hive = registry.Hive(os.path.join(partition, hivefile))
        # Get profile list:
        try:
            key = hive.getKey("Microsoft\\Windows NT\\CurrentVersion\\ProfileList")
            subkeys = key.subKeys()
        except:
            return []
        # Control each profile:
        for subkey in subkeys:
            # Check correctness of profile:
            values = {}
            try:
                key2 = key.getSubKey(subkey)
                values = key2.valueDict()
            except:
                continue
            if not (values.has_key("ProfileImagePath") and values.has_key("Flags")):
                continue
            path = values["ProfileImagePath"]
            if values["Flags"] == 0:
                path = path.split("\\",1)[1]
                path = path.replace("\\", "/")
                path = os.path.join(partition, path)
                if os.path.isfile(os.path.join(path, "NTUSER.DAT")):
                    # User exists, append to list:
                    username = os.path.basename(path)
                    if os.path.isfile(os.path.join(partition, "bootmgr")):
                        users.append((partition, "Windows Vista", username, path))
                    else:
                        users.append((partition, "Windows XP", username, path))
    return users

def allUsers():
    "Searches partitions and returns users"
    users = []      # user1 = (partition, parttype, username, userdir)
    partitions = getPartitions()
    for part in partitions:
        if isWindowsPart(part):
            users.extend(getWindowsUsers(part))
    return users

#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import os
import logging

from migration.utils import registry

def getPartitions():
    "get all partitions in the form: '/mnt/hda9'"
    partitions=[]
    try:
        f = open("/etc/fstab")
        logging.debug("/etc/fstab :\n" + f.read())
        f.close()
        f = open("/proc/mounts")
        logging.debug("/proc/mounts :\n" + f.read())
        f.seek(0)
    except:
        return []
    for line in f:
        part = line.split(" ")
        if not len(part) == 6:
            continue
        mountdir = part[1]
        if os.access(mountdir, os.R_OK):
            partitions.append(mountdir)
            logging.debug("access ok: " + mountdir)
        else:
            logging.debug("no access: " + mountdir)
    return partitions


def isWindows(partition):
    "Checks which partitions have windows installed"
    possible_files=["boot.ini","command.com","bootmgr"]
    for a in possible_files:
        if os.path.exists(os.path.join(partition,a)):
            logging.debug("windows part: " + partition)
            return True
    logging.debug("not windows part: " + partition)
    return False

def getWindowsUsers(partition):
    "Returns regular users in the partition which has windows installed"
    users = []      # User: (partition, parttype, username, userdir)
    # Try to find a hive file which includes software information:
    possibleHiveFiles = ["Windows/System32/config/SOFTWARE", "WINDOWS/system32/config/software"]
    hivefile = ""
    for possibleHiveFile in possibleHiveFiles:
        possibleHiveFile = os.path.join(partition,possibleHiveFile)
        if os.path.isfile(possibleHiveFile):
            hivefile = possibleHiveFile
            logging.debug("registry exists: " + hivefile)
            break
    # If found, get users:
    if hivefile != "":
        hive = registry.Hive(hivefile)
        # Get profile list:
        try:
            key = hive.getKey("Microsoft\\Windows NT\\CurrentVersion\\ProfileList")
            subkeys = key.subKeys()
            logging.debug("registry opened: " + hivefile)
        except:
            logging.debug("registry cannot be opened: " + hivefile)
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
                logging.debug("not a user: " + subkey)
                continue
            path = values["ProfileImagePath"]
            path = path.split("\\",1)[1]
            path = path.replace("\\", "/")
            path = os.path.join(partition, path)
            if os.path.isfile(os.path.join(path, "NTUSER.DAT")):
                # User exists, append to list:
                username = os.path.basename(path)
                logging.info("User Found: " + path)
                if os.path.isfile(os.path.join(partition, "bootmgr")):
                    users.append((partition, "Windows Vista", username, path))
                else:
                    users.append((partition, "Windows XP", username, path))
            else:
                logging.debug("user registry does not exists: " + path)
    else:
        logging.debug("registry does not exists on: " + partition)
    return users

def allUsers():
    "Searches partitions and returns users"
    users = []      # user1 = (partition, parttype, username, userdir)
    partitions = getPartitions()
    for part in partitions:
        if isWindows(part):
            users.extend(getWindowsUsers(part))
    return users
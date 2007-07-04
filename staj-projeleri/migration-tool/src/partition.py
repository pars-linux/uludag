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

import string
import commands
import os

import registry

def getPartitions():
	"get all partitions in the form: '/mnt/hda9'"
	partitions=[]
	df = commands.getoutput("df")
	df = string.split(df,"\n")
	for i in df[1:]:
		i = string.split(i," ")
		partitions.append(i[-1])
	return partitions

def isWindowsPart(partition):
	"check which partitions have windows installed"
	possible_files=["boot.ini","command.com","bootmgr"]
	for a in possible_files:
		if os.path.exists(os.path.join(partition,a)):
			return True
	return False

def getWindowsUsers(partition):
    # User: (partition, parttype, username, userdir)
    
    users = []
    
    possiblehivefiles = ["Windows/System32/config/SOFTWARE", "WINDOWS/system32/config/software"]
    hivefile = ""
    for possiblehivefile in possiblehivefiles:
        possiblehivefile = os.path.join(partition,possiblehivefile)
        if os.path.isfile(possiblehivefile):
            hivefile = possiblehivefile     # registry dosyasi bulundu
            break
    
    if hivefile != "":      # kullanicilari bulmaya calisiyorum
        try:
            hive = registry.Hive(os.path.join(partition, hivefile))
            key = hive.getKey("Microsoft\\Windows NT\\CurrentVersion\\ProfileList")
            subkeys = key.subKeys()
            for subkey in subkeys:
                key2 = key.getSubKey(subkey)
                values = key2.valueDict()
                if not (values.has_key("ProfileImagePath") and values.has_key("ProfileImagePath")):
                    continue
                path = key2.getValue("ProfileImagePath")
                if key2.getValue("Flags") == 0:
                    path = path.split("\\",1)[1]
                    path = path.replace("\\", "/")
                    path = os.path.join(partition, path)
                    if os.path.isfile(os.path.join(path, "NTUSER.DAT")):        # bir kullanici buldum
                        username = os.path.basename(path)
                        if os.path.isfile(os.path.join(partition, "bootmgr")):
                            users.append((partition, "Windows Vista", username, path))
                        else:
                            users.append((partition, "Windows XP", username, path))
        except:     # hata durumunda bir seyler yap
            raise
    
    return users

def allUsers():
    "Search partitions and find users"
    users = []      # user1 = (partition, parttype, username, userdir)
    partitions = getPartitions()
    for part in partitions:
        if isWindowsPart(part):
            users.extend(getWindowsUsers(part))
    return users

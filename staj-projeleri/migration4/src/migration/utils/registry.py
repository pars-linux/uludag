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


import struct
import string


class Hive:
    "Class for reading windows registry hives"
    def __init__(self, filename):
        hivefile = open(filename)      # open hive file
        self.data = hivefile.read()
        hivefile.close()
        hivedata = struct.unpack("36s2i4052s", self.data[:4096])        # unpack hive structure
        self.__firstKeyIndex__ = hivedata[1]
    
    def firstKey(self):
        "Returns the root key of hive"
        return Key(self.data, self.__firstKeyIndex__ + 4096)
    
    def getKey(self, path):
        "Returns the key corresponding to path given"
        key = self.firstKey()
        pathlist = path.split("\\")
        for item in pathlist:
            key = key.getSubKey(item)
        return key
    
    def getValue(self, path, field):
        "Returns the value corresponding to path and field given"
        key = self.getKey(path)
        return key.getValue(field)


class Key:
    "Class for windows registry keys"
    
    def __init__(self, data, position):
        self.data = data
        self.__index__ = position
        
        keydata = struct.unpack("19i2h", self.data[position:(position + 80)])
        
        self.numSubKeys = keydata[6]
        lfIndex = keydata[8]
        self.numValues = keydata[10]
        self.__valueListIndex__ = keydata[11]
        namesize = keydata[19]
        
        self.name = self.data[(position + 80):(position + 80 + namesize)]      # read the name of the key
        
        self.__children__ = []
        position = 4096 + lfIndex
        for x in range(self.numSubKeys):
            position += 8
            subkeydata = struct.unpack("2i", self.data[position:(position + 8)])
            subkeyindex = subkeydata[0]
            self.__children__.append(subkeyindex)
        
    def getChild(self, childno):
        "Get subkey by index"
        if (childno < 0) or (childno >= self.numSubKeys):
            raise IndexError, "list index out of range"
        return Key(self.data, self.__children__[childno] + 4096)
    
    def getSubKey(self, keyname):
        "Get subkey by name"
        for x in range(self.numSubKeys):
            key = self.getChild(x)
            if key.name == keyname:
                return key
        raise KeyError, keyname
    
    def subKeys(self):
        "Return a list of subkey names of the key"
        keys = []
        for x in range(self.numSubKeys):
            key = self.getChild(x)
            keys.append(key.name)
        return keys
    
    def valueDict(self):
        "Returns a dictionary of fields and values of the key"
        fields = []
        dictionary = {}
        position = 4096 + self.__valueListIndex__ + 4
        
        for x in range(self.numValues):
            valuedata = struct.unpack("i", self.data[position:(position + 4)])
            fields.append(valuedata[0])
            position += 4
        
        for fieldindex in fields:
            position = 4096 + fieldindex
            valuekey = struct.unpack("i2sh3i2h", self.data[position:(position + 24)])
            
            vk = valuekey[1]
            namesize = valuekey[2]
            datasize = valuekey[3]
            dataindex = valuekey[4]
            valtype = valuekey[5]
            flag = valuekey[5]
            
            if (0 < valtype < 3 and vk == "vk"):        # valuetype = REG_SZ or REG_EXPAND_SZ
                field = self.data[(position + 24):(position + 24 + namesize)]
                position = 4096 + dataindex + 4
                data = self.data[position:(position + datasize)]
                
                dictionary[field] = data.decode("utf-16").replace("\x00","")
            
            if valtype == 4 and vk == "vk":     # valuetype = REG_DWORD
                field = self.data[(position + 24):(position + 24 + namesize)]
                dictionary[field] = dataindex
        
        return dictionary
    
    def getValue(self, field):
        "Returns the value of the corresponding field of the key"
        dictionary = self.valueDict()
        return dictionary[field]

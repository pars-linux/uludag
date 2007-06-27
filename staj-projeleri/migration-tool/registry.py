import struct
import string


class Hive:
    "Class for reading windows registry hives"
    def __init__(self, filename):
        self.__file__ = open(filename)      # open hive file
        data = self.__file__.read(4096)     # load binary data
        hivedata = struct.unpack("36s2i4052s", data)        # unpack hive structure
        self.__firstKeyIndex__ = hivedata[1]
    
    def firstKey(self):
        "Returns the root key of hive"
        return Key(self.__file__, self.__firstKeyIndex__ + 4096)
    
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
    
    def __init__(self, thefile, position):
        self.__file__ = thefile
        self.__index__ = position
        
        self.__file__.seek(position)
        data = self.__file__.read(80)
        keydata = struct.unpack("19i2h", data)
        
        self.numSubKeys = keydata[6]
        lfIndex = keydata[8]
        self.numValues = keydata[10]
        self.__valueListIndex__ = keydata[11]
        namesize = keydata[19]
        
        self.name = self.__file__.read(namesize)       # read the name of the key
        
        self.__children__ = []
        self.__file__.seek(4096 + lfIndex + 8)
        for x in range(self.numSubKeys):
            data = self.__file__.read(8)
            subkeydata = struct.unpack("2i", data)
            subkeyindex = subkeydata[0]
            self.__children__.append(subkeyindex)
        
    def getChild(self, childno):
        "Get subkey by index"
        if (childno < 0) or (childno >= self.numSubKeys):
            raise IndexError, "list index out of range"
        return Key(self.__file__, self.__children__[childno] + 4096)
    
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
        self.__file__.seek(4096 + self.__valueListIndex__ + 4)
        
        for x in range(self.numValues):
            data = self.__file__.read(4)
            valuedata = struct.unpack("i", data)
            fields.append(valuedata[0])
        
        for fieldindex in fields:
            self.__file__.seek(4096 + fieldindex)
            data = self.__file__.read(24)
            valuekey = struct.unpack("i2sh3i2h", data)
            
            vk = valuekey[1]
            namesize = valuekey[2]
            datasize = valuekey[3]
            dataindex = valuekey[4]
            valtype = valuekey[5]
            flag = valuekey[5]
            
            if (0 < valtype < 3 and vk == "vk"):        # FIXME: hata kontrolu genisletilebilir
                field = self.__file__.read(namesize)
                self.__file__.seek(4096 + dataindex + 4)
                data = self.__file__.read(datasize)
                
                mylist = data.split("\x00")
                value = "".join(mylist)
                dictionary[field] = value
        
        return dictionary
    
    def getValue(self, field):
        "Returns the value of the corresponding field of the key"
        dictionary = self.valueDict()
        return dictionary[field]
    
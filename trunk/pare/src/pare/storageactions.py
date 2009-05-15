# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file

from storage import Storage, Partition
from udev import *

import gettext
_ = lambda x:gettext.ldgettext("pare", x)

import logging
log = logging.getLogger("pare")
 

TYPE_DESTROY = 1000
TYPE_RESIZE = 500
TYPE_MIGRATE = 250
TYPE_CREATE = 100
TYPE_NONE = 0

_type = {TYPE_NONE:"None",
         TYPE_CREATE:"Create",
         TYPE_MIGRATE:"Migrate",
         TYPE_RESIZE:"Resize",
         TYPE_DESTROY:"Destroy"
         }

OBJECT_NONE = 0
OBJECT_STORAGE = 1
OBJECT_FORMAT = 2

_object  = {OBJECT_NONE:"None",
            OBJECT_STORAGE:"Storage",
            OBJECT_FORMAT:"Format"
            }

RESIZE_SHRINK = 88
RESIZE_GROW = 89

_resize = {RESIZE_SHRINK: "Shrink",
           RESIZE_GROW: "Grow"}

def type_from_string(type):
    if type is None:
        return None

    for (key,value) in _type.items():
        if value.lower() == type.lower():
            return k

    return resize_type_from_string(type_string)

def object_from_string(type):
    if type is None:
        return None

    for (key,value) in _object.items():
        if value.lower() == type.lower():
            return k

def resize_type_from_string(type):
    if type is None:
        return None

    for (key,value) in _resize.items():
        if value.lower() == type.lower():
            return k


class Action(object):
    type = TYPE_NONE
    obj = OBJECT_NONE
    
    def __init__(self, device):
        if not isinstance(device, Storage):
            raise ValueError("device is not Storage")
        
        self.device = device
    
    def execute(self):
        pass
    
    def cancel(self):
        pass
    
    def isDestroy(self):
        return self.type == TYPE_DESTROY
    
    def isResize(self):
        return self.type == TYPE_RESIZE
    
    def isMigrate(self):
        return self.type == TYPE_MIGRATE
    
    def isShrink(self):
        return (self.type == TYPE_RESIZE and self.dir == RESIZE_SHRINK)
    
    def isGrow(self):
        return (self.type == TYPE_RESIZE and self.dir == RESIZE_GROW)
    
    def isDevice(self):
        return self.obj == OBJECT_STORAGE
    
    def isFormat(self):
        return self.obj == OBJECT_FORMAT
    
    def __str__(self):
        s = "%s %s" %(type_from_string(self.type), object_from_string(self.obj))
        if self.isResize():
            s+= " %s" % resize_type_from_string(self.dir)
        if self.isFormat():
            if self.device.format.type:
                class_type = self.device.format.type
            else:
                class_type = None
            s += " %s on" % class_type
        
        s += " %s (%s)" % (self.device.name, self.device.type)
        
        return s
    
class CreateDevice(Action):
    type = TYPE_CREATE
    obj = OBJECT_STORAGE
    
    def __init__(self, device):
        Action.__init__(self, device)
        
    def execute(self):
        self.device.create()
    
class DestroyDevice(Action):
    type = TYPE_DESTROY
    obj = OBJECT_STORAGE
    
    def __init__(self, device):
        Action.__init__(self, device)
        if device.exists:
            device.tearDown()
            
    def execute(self):
        self.device.destroy()
          
class ResizeDevice(Action):
    type = TYPE_RESIZE
    obj = OBJECT_STORAGE
    
    def __init(self, device, newsize):
        if device.currentsize == newsize:
            raise ValueError("new size is the same as old size")
        
        if not device.resizable:
            raise ValueError(" device is not resizable")
            
        Action.__init__(self, device)
        
        if newsize > self.device.size:
            self.dir == RESIZE_GROW
        else:
            self.dir == RESIZE_SHRINK
        
        self.origSize = device.targetSize
        self.device.targetSize = newsize
    
    def execute(self):
        self.device.resize()
    
    def cancel(self):
        self.device.targetSize = self.origSize

class CreateFormat(Action):
    type = TYPE_CREATE
    obj = OBJECT_FORMAT
    
    def __init__(self, device, format=None):
        Action.__init__(self, device)
        self.origFormat = device.format
        if self.device.format.exists:
            self.device.format.tearDown()
            self.device.format = format
    
    def execute(self):
        if isinstance(self.device, Partition):
            if self.device.format.partedFlag is not None:
                self.device.setFlag(self.device.format.partedFlag)
                self.device.disk.commit()
        
        udev_settle()
        self.device.setup()
        self.device.format.create(device=self.device.path, options=self.devie.formatArgs)
        
        udev_settle()
        self.device.updateSysfsPath()
        info = udev_get_block_device("/sys%s" % self.device.sysfsPath)
        self.device.format.uuid = udev_device_get_uuid(info)
        
    def cancel(self):
        self.device.format = self.origFormat

class DestroyFormat(Action):
    type = TYPE_CREATE
    obj = OBJECT_FORMAT
    
    def __init__(self, device):
        Action.__init__(self, device)
        
        if self.device.format.exists:
            self.origFormat = self.device.format
            self.device.format.tearDown()
        
        self.device.format = None
        
    def execute(self):
        if self.origFormat:
            if isinstance(self.device, Partition) and self.device.partedFlag is not None:
                self.device.unsetFlag(self.origFormat.partedFlag)
                self.device.disk.commit()
                udev_settle()
            
            self.device.setup()
            self.origFormat.destroy()
            udev_settle()
            self.device.destroy()
    
    def cancel(self):
        self.device.format = self.origFormat
    
class ResizeFormat(Action):
    type = TYPE_RESIZE
    obj = OBJECT_FORMAT
    
    def __init__(self, device, newsize):
        if device.targetSize == newsize:
            raise ValueError("new size same as the old size")
        
        Action.__init__(self, device)
        if newsize > device.format.currentSize:
            self.dir = RESIZE_GROW
        else:
            self.dir =  RESIZE_SHRINK
            
        self.origSize = self.device.format.targetSize
        self.device.format.targetSize = newsize
    
    def execute(self):
        self.device.setup()
        self.device.format.doResize()
    
    def cancel(self):
        self.device.format.targetSize = self.origSize
    
class MigrateFormat(Action):
    type = TYPE_MIGRATE
    obj = OBJECT_STORAGE
    
    def __init__(self, device):
        if not device.format.migratable or not device.format.exists:
            raise ValueError("device format not migratable")
        
        Action.__init__(self, device)
        self.device.format.migrate = True
        
    def execute(self):
        self.device.setup()
        self.device.format.doMigrate()
    
    def cancel(self):
        self.device.format.migrate = False
                
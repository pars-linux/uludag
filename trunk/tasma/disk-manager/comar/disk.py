# -*- coding: utf-8 -*-

import fnmatch
import glob
import os

def getDevices():
    if not os.path.exists("/sys/block"):
        return fail("sysfs not found!")

    devices = []
    for sysfs_dev in os.listdir("/sys/block"):
        if filter(lambda x: fnmatch.fnmatch(sysfs_dev, x), ["fd*", "loop*", "ram*", "sr*"]):
            continue
        dev_name = os.path.basename(sysfs_dev)
        dev_name = dev_name.replace("!", "/")
        devices.append("/dev/" + dev_name)
    devices.sort()
    return devices

def getDeviceByLabel(label):
    return

def getDeviceParts(device):
    return

def getMounted():
    return

def mount(device, path):
    return

def umount(device):
    return

def listEntries():
    return

def addEntry(device, path):
    return

def getEntry(device):
    return

def removeEntry(device):
    return

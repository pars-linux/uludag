# -*- coding: utf-8 -*-

import glob
import os

def getDevices():
    if not os.path.exists("/sys/block"):
        return fail("sysfs not found!")
    return glob.glob("/sys/block/*")

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

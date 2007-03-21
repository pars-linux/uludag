import os
from subprocess import *
from nvidia_ids import *

def value(path, dir, file_):
    return open(os.path.join(path, dir, file_)).read().rstrip("\n")

def findPciCards():
    sysDir = "/sys/bus/pci/devices"
    nvidia_vendor_ids = ["0x1092", "0x10de", "0x12d2"]
    pci_ids = []

    if os.path.isdir(sysDir):
        for _dev in os.listdir(sysDir):
            try:
                if value(sysDir, _dev, "class").startswith("0x03"):
                    vendorId = value(sysDir, _dev, "vendor")
                    if vendorId in nvidia_vendor_ids:
                        deviceId = value(sysDir, _dev, "device")
                        pci_ids.append(deviceId)
            except:
                pass
    return pci_ids

for card in findPciCards():
    if nvidia_dict_3.has_key(card):
        print "Found a 3rd generation nvidia card: %s" % nvidia_dict_3[card]
    elif nvidia_dict_2.has_key(card):
        print "Found a 2nd generation nvidia card: %s" % nvidia_dict_2[card]
    elif nvidia_dict_1.has_key(card):
        print "Found a 1st generation nvidia card: %s" % nvidia_dict_1[card]

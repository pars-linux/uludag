#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import glob

class PCIDevice(object):
    """Class which implements a hardware device."""
    def __init__(self, sysfs_path, ids={}):
        """PCIDevice constructor."""
        self.vendor = ""
        self.device = ""
        self.driver = ""
        self.module = ""
        self.product = ""
        self.manufacturer = ""
        self.subsystem_vendor = ""
        self.subsystem_device = ""
        self.bus_id = os.path.basename(sysfs_path)
        for k in ("vendor", "device", "subsystem_vendor", "subsystem_device"):
            try:
                self.__dict__[k] = \
                        open(os.path.join(sysfs_path, k), "r").read().strip()
            except IOError:
                pass

        try:
            self.manufacturer, self.product = ids["%s:%s" % (self.vendor, self.device)]
        except KeyError:
            pass

        # Detect the driver
        try:
            self.driver = os.path.basename(os.readlink(os.path.join(sysfs_path, "driver")))
            self.module = os.path.basename(os.readlink("/sys/bus/pci/drivers/%s/module" % self.driver))
        except OSError:
            pass

    def __str__(self):
        """Human readable str representation."""
        return "%s [%s:%s]  %s %s\n  Subsystem: [%s:%s]\n  Driver in use: %s %s\n"  % (self.bus_id,
                                                                                       self.vendor, self.device,
                                                                                       self.manufacturer, self.product,
                                                                                       self.subsystem_vendor,
                                                                                       self.subsystem_device,
                                                                                       self.driver,
                                                                                       "(%s)" % self.module if self.module else "")

class PCIBus(object):
    """Class which abstracts the PCI Bus and the devices."""
    def __init__(self):
        """PCIBus constructor."""
        self.__sysfs_path = "/sys/bus/pci/devices"
        self.devices = {}

        self.__ids = self.__populate_id_db()
        self.detect()

    def __populate_id_db(self):
        """Returns a dictionary representing the pci.ids file."""
        id_dict = {}
        last_vendor = []
        with open("/usr/share/misc/pci.ids", "r") as _file:
            for line in _file.read().strip().split("\n"):
                if line and not line.startswith(("#", "C ")) and line.count("\t") < 2:
                    if "\t" in line:
                        # Device, subdevice
                        product_id, product_name = line.strip("\t").split(" ", 1)
                        id_dict["0x%s:0x%s" % (last_vendor[0], product_id)] = [last_vendor[1], product_name.strip()]
                    else:
                        # Manufacturer
                        last_vendor = [line[:4], line[6:]]

        return id_dict

    def detect(self):
        """Detect currently available PCI devices."""
        for device in glob.glob("%s/*" % self.__sysfs_path):
            self.devices[os.path.basename(device)] = PCIDevice(device, self.__ids)


##############
# Unit tests #
##############

def test_pci_bus():
    """Unit test for PCIBus class."""
    print "Testing PCIBus class..\n"
    for device in PCIBus().devices.values():
        print device

def test_pci_device_informations():
    """Unis test for checking the PCIDevice correctness."""
    def check(lspci, pcidevice):
        """Compares the PCIDevice class and lspci -kn output."""
        ret = (lspci[0] == pcidevice.vendor and lspci[1] == pcidevice.device)
        try:
            exp_1 = lspci[2] == pcidevice.subsystem_vendor
            exp_2 = lspci[3] == pcidevice.subsystem_device
        except IndexError:
            pass
        else:
            ret = ret and exp_1 and exp_2
        try:
            ret = (ret and lspci[4] == pcidevice.driver)
        except IndexError:
            pass

        return ret

    print "Testing class PCIDevice's coherence with lspci -kn output..\n"

    # Parse lspci -kn output for expected values
    devices = {}
    for line in os.popen("lspci -kn").read().strip().split("\n"):
        if not line.startswith(("\t", " ")):
            # device
            fields = line.split()
            bus_id = fields[0]
            #devclass = fields[1].strip(":")
            (vendor, device) = fields[2].split(":")
            vendor = "0x%s" % vendor
            device = "0x%s" % device
            devices[bus_id] = [vendor, device]
        elif "Subsystem" in line:
            (subvendor, subdevice) = line.split(":", 1)[-1].strip().split(":")
            subvendor = "0x%s" % subvendor
            subdevice = "0x%s" % subdevice
            devices[bus_id].extend([subvendor, subdevice])
        elif "driver in use" in line:
            devices[bus_id].append(line.split(":")[-1].strip())

    for dev in glob.glob("/sys/bus/pci/devices/*"):
        pci_device = PCIDevice(dev)
        bus_id = os.path.basename(dev).replace("0000:", "")
        if check(devices[bus_id], pci_device):
            print "%s -> PASSED" % bus_id
        else:
            print "%s -> FAILED" % bus_id
            print devices[bus_id]
            print pci_device
            print

if __name__ == "__main__":
    import sys
    if "--test" in sys.argv:
        test_pci_device_informations()
        test_pci_bus()

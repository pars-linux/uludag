#!/usr/bin/python
# -*- coding: utf-8 -*-

from pci import PCIBus, PCIDevice

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
    test_pci_device_informations()
    test_pci_bus()

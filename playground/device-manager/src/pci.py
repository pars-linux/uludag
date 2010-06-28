#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2010 Ozan Çağlayan <ozan@pardus.org.tr>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


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

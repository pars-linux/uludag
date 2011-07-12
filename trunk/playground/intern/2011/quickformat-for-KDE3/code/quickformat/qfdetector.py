##!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 TUBITAK/BILGEM
# Batuhan Bayrakçı  <batuhanbayrakci at gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
# (See COPYING)

import dbus

BUSES = ["usb","firewire","platform"]

class DeviceProperties:
    """Gets properties of device through dbus system"""

    def __init__(self, device):
        bus = dbus.SystemBus()
        self.pr = bus.get_object("org.freedesktop.UDisks",device)
        self.i = dbus.Interface(self.pr,"org.freedesktop.DBus.Properties")

    def get_property(self,prob):
        """gets a property of device"""

        return self.i.Get("org.freedesktop.UDisks.Device",prob)

    def get_all_properties(self):
        """gets all properties of device"""
        return self.i.GetAll("org.freedesktop.UDisks.Device")


class DeviceDetector:
    """Gets all storage devices which plugged on the system"""

    def __init__(self):
        self.bus = dbus.SystemBus()
        self.proxy = self.bus.get_object("org.freedesktop.UDisks", "/org/freedesktop/UDisks")
        self.iface = dbus.Interface(self.proxy, "org.freedesktop.UDisks")

    def get_all_devices(self):
        devices = []
        enum_devs = self.iface.EnumerateDevices()

        for dev in enum_devs:
            d = DeviceProperties(dev)
            if d.get_property("DeviceIsPartition") and (d.get_property("DriveConnectionInterface") in BUSES):
                devices.append(dev)
        return devices

#!/usr/bin/python
# -*- coding: utf-8 -*-

import dbus

BUSES = ["usb","firewire","platform"]

class Device:

    def __init__(self, device):
        bus = dbus.SystemBus()
        self.pr = bus.get_object("org.freedesktop.UDisks",device)
        self.i = dbus.Interface(self.pr,"org.freedesktop.DBus.Properties")

    def get_property(self,prob):
        return self.i.Get("org.freedesktop.UDisks.Device",prob)
    
    def get_all_properties(self):
        return self.i.GetAll("org.freedesktop.UDisks.Device")


class QFDetector:
    
    def __init__(self):

        self.bus = dbus.SystemBus()
        self.proxy = self.bus.get_object("org.freedesktop.UDisks", "/org/freedesktop/UDisks")
        self.iface = dbus.Interface(self.proxy, "org.freedesktop.UDisks")

    def get_all_devices(self):
        devices = []
        enum_devs = self.iface.EnumerateDevices()
        for dev in enum_devs:
            d = Device(dev)
            if d.get_property("DeviceIsMounted") and (d.get_property("DriveConnectionInterface") in BUSES):
                devices.append(dev)
        print devices
        return devices


i = QFDetector()


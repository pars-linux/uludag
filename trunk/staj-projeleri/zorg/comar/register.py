#!/usr/bin/python
# -*- coding: utf-8 -*-

import os.path

import dbus.bus

if __name__ == "__main__":
    bus = dbus.SystemBus()
    object = bus.get_object("tr.org.pardus.comar", "/system", introspect=False)
    iface = dbus.Interface(object, "tr.org.pardus.comar")

    iface.register("atidrivers", "Xorg.Driver", os.path.abspath("xorg.driver_fglrx.py"))

#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import comar
import dbus

from PyQt4.QtCore import *
from PyKDE4.kdecore import *
from PyKDE4 import plasmascript

# it is very important to check if there is an active mainloop
# before creating a new one, it may cause to crash plasma itself
if not dbus.get_default_main_loop():
    dbus.mainloop.qt.DBusQtMainLoop(set_as_default = True)

net_packages = ["net_tools", "wireless_tools"]
link = comar.Link()

def asString(lst, pkg):
    return map(lambda x:'%s.%s' % (pkg, str(x)), lst)

class NMEngine(plasmascript.DataEngine):
    def __init__(self, parent, args=None):
        plasmascript.DataEngine.__init__(self, parent)

    def init(self):
        self.setMinimumPollingInterval(333)
        link.listenSignals("Net.Link", self.handler)

    def handler(self, package, signal, args):
        self.updateSourceEvent("%s.%s" % (package, args[0]))

    def sources(self):
        sources = []
        for package in net_packages:
            profiles = asString(list(link.Net.Link[package].connections()), package)
            for profile in profiles:
                sources.append(profile)
        return sources

    def sourceRequestEvent(self, name):
        return self.updateSourceEvent(name)

    def updateSourceEvent(self, _name):
        pkg, name = _name.split('.')
        _st = link.Net.Link[str(pkg)].connectionInfo(str(name))
        self.setData(_name, "State", QVariant(str(_st['state'])))
        self.setData(_name, "Device", QVariant(str(_st['device_id'])))
        return True

def CreateDataEngine(parent):
    return NMEngine(parent)

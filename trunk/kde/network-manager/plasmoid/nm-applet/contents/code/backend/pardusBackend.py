#!/usr/bin/python
# -*- coding: utf-8 -*-

import dbus
import comar
import pardus.netutils

# it is very important to check if there is an active mainloop
# before creating a new one, it may cause to crash plasma itself
if not dbus.get_default_main_loop():
    from dbus.mainloop.qt import DBusQtMainLoop
    DBusQtMainLoop(set_as_default=True)

class NetworkIface:
    """ Network Interface """

    def __init__(self):
        self.link = comar.Link()
        self.link.useAgent()
        self.link.setLocale()

    def connections(self, package):
        return list(self.link.Network.Link[package].connections())

    def connect(self, package, profile):
        self.setState(package, profile, "up")

    def disconnect(self, package, profile):
        self.setState(package, profile, "down")

    def toggle(self, package, profile):
        info = self.info(package, profile)
        if str(info['state']) == "down":
            self.connect(package, profile)
        else:
            self.disconnect(package, profile)

    def setState(self, package, profile, state):
        self.link.Network.Link[package].setState(profile, state, async=self.handler)

    def info(self, package, profile):
        return self.link.Network.Link[package].connectionInfo(str(profile))

    def getMaxQuality(self, device):
        try:
            return int(self.link.Network.Link['wireless_tools'].scanRemote(device)[0]['quality_max'])
        except:
            return 100

    def handler(self, *args):
        pass

    def listen(self, func):
        self.link.listenSignals("Network.Link", func)

    def stat(self, device):
        return pardus.netutils.findInterface(device).getStats()

    def strength(self, device):
        return int(pardus.netutils.findInterface(device).getSignalQuality())



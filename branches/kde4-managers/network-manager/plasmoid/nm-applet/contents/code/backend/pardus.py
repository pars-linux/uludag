#!/usr/bin/python
# -*- coding: utf-8 -*-

import dbus
import comar

class NetworkIface:
    """ Network Interface """

    def __init__(self):
        # it is very important to check if there is an active mainloop
        # before creating a new one, it may cause to crash plasma itself
        if not dbus.get_default_main_loop():
            from dbus.mainloop.qt import DBusQtMainLoop
            DBusQtMainLoop(set_as_default=True)

        self.link = comar.Link()

    def connections(self, package):
        return list(self.link.Net.Link[package].connections())

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
        self.link.Net.Link[package].setState(profile, state, async=self.handler)

    def info(self, package, profile):
        return self.link.Net.Link[package].connectionInfo(str(profile))

    def handler(self, *args):
        pass

    def listen(self, func):
        self.link.listenSignals("Net.Link", func)



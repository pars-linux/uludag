#!/usr/bin/python
# -*- coding: utf-8 -*-

# D-Bus
import dbus

# Solid
from PyKDE4.solid import Solid

# KDE
from PyKDE4.kdecore import i18n

class Notifier:

    def __init__(self, loop):
        self.bus = dbus.SessionBus(mainloop=loop)
        self.proxy = None
        self.solid = None
        self.lastMessage = ''
        self.lastId = None
        self.init()
        self.init('network')

    def init(self, path='notify'):
        if path == 'notify':
            try:
                self.proxy = self.bus.get_object('org.kde.VisualNotifications', '/VisualNotifications')
                self.notifier = dbus.Interface(self.proxy, "org.kde.VisualNotifications")
            except:
                self.proxy = None
        elif path == 'network':
            try:
                self.solid = self.bus.get_object('org.kde.kded', '/modules/networkstatus')
                self.netstatus = dbus.Interface(self.solid, "org.kde.Solid.Networking")
            except:
                self.solid = None

    def registerNetwork(self):
        if self.solid:
            self.netstatus.registerNetwork("comar",0,"org.kde.plasma")
        else:
            self.init('network')

    def setState(self, state=Solid.Networking.Unknown):
        if not self.solid:
            self.registerNetwork()
            return
        self.netstatus.setNetworkStatus("comar", state)

    def handler(self, *args):
        if len(args) > 0:
            self.lastId = long(args[0])

    def notify(self, message, state, timeout=5000):
        self.setState(state)
        if self.lastMessage == message:
            return
        id = 0
        if self.lastId:
            id = self.lastId
            self.lastId = None
        if self.proxy:
            self.notifier.Notify("NM", id, "", "applications-internet", i18n("Network Manager").toString(), message, [], {}, timeout, reply_handler=self.handler, error_handler=self.handler)
        else:
            print "Notifier is not working, message was : %s" % message
            self.init()
        self.lastMessage = message

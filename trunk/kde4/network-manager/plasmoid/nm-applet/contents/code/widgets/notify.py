#!/usr/bin/python
# -*- coding: utf-8 -*-

# D-Bus
import dbus

class Notifier:

    def __init__(self, loop):
        self.bus = dbus.SessionBus(mainloop=loop)
        self.proxy = None
        self.lastMessage = ''
        self.lastId = None
        self.init()

    def init(self):
        try:
            self.proxy = self.bus.get_object('org.kde.VisualNotifications', '/VisualNotifications')
            self.notifier = dbus.Interface(self.proxy, "org.kde.VisualNotifications")
        except:
            self.proxy = None

    def handler(self, *args):
        if len(args) > 0:
            self.lastId = long(args[0])

    def notify(self, message, timeout=5000):
        if self.lastMessage == message:
            return
        if self.lastId:
            self.notifier.CloseNotification(self.lastId, reply_handler=self.handler, error_handler=self.handler)
            self.lastId = None
        if self.proxy:
            self.notifier.Notify("NM", 0, "", "applications-internet", "Network Manager", message, [], {}, timeout, reply_handler=self.handler, error_handler=self.handler)
        else:
            print "Notifier is not working, message was : %s" % message
            self.init()
        self.lastMessage = message

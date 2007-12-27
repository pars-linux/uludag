#!/usr/bin/python
# -*- coding: utf-8 -*-

import dbus
import dbus.mainloop.qt3
import traceback

from kdecore import i18n

class Notifier:
    def click_handler(self, id, button):
        if id == self.notifyid:
            print "%s clicked!" % button

    def __init__(self, icon, header, msg, pos=None):
        dbus.mainloop.qt3.DBusQtMainLoop(set_as_default=True)
        bus = dbus.SessionBus()
        try:
            object  = bus.get_object("org.freedesktop.Notifications","/org/freedesktop/Notifications")
            self.iface = dbus.Interface(object, dbus_interface='org.freedesktop.Notifications')
            object.connect_to_signal("ActionInvoked", self.click_handler, dbus_interface="org.freedesktop.Notifications")

        except dbus.DBusException:
            traceback.print_exc()

        if not pos or pos[0] < 0 or pos[1] < 0:
            self.hints = {}
        else:
            self.hints= {"x": pos[0], "y": pos[1]}

        self.icon = icon
        self.header = header
        self.msg = msg

    def show(self):
        self.notifyid = self.iface.Notify("package-manager",
                         0,
                         "file://%s" % self.icon,
                         unicode(self.header),
                         unicode(self.msg),
                         ["showupdates", unicode(i18n("Show Updates")), "ignore", unicode(i18n("Ignore"))],
                         self.hints,
                         0)

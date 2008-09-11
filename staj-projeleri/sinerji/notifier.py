#!/usr/bin/python
# -*- coding: utf-8 -*-

import dbus
import traceback
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Notifier(QObject):
    def click_handler(self, id, button):
        if id == self.notifyid:
            if button == "default" or button == "ignore":
                print "Ignore clicked"
                pass
            else:
                self.emit(SIGNAL("acceptServer"), ())

    def __init__(self):
        QObject.__init__(self)
        bus = dbus.SessionBus()
        self.notifyid = 0
        try:
            object  = bus.get_object("org.freedesktop.Notifications", "/org/freedesktop/Notifications")
            self.iface = dbus.Interface(object, dbus_interface='org.freedesktop.Notifications')
            object.connect_to_signal("ActionInvoked", self.click_handler, dbus_interface="org.freedesktop.Notifications")

        except dbus.DBusException:
            traceback.print_exc()

    def show(self, icon, header, msg, pos=None):
        if not pos or pos[0] < 0 or pos[1] < 0:
            hints = {}
        else:
            hints= {"x": pos[0], "y": pos[1]}

        # close previous notification window
        self.iface.CloseNotification(self.notifyid)

        self.notifyid = self.iface.Notify("sinerji",
                         0,
                         "file://%s" % icon,
                         unicode(header),
                         unicode(msg),
                         ["showupdates", unicode("Show Updates"), "ignore", unicode("Ignore")],
                         hints,
                         0)

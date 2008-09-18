#!/usr/bin/python
# -*- coding: utf-8 -*-

import dbus
import traceback
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Notifier(QObject):

    def __init__(self):
        QObject.__init__(self)
        bus = dbus.SessionBus()
        self.notifyid = 0
        try:
            object  = bus.get_object("org.freedesktop.Notifications", "/org/freedesktop/Notifications")
            self.iface = dbus.Interface(object, dbus_interface='org.freedesktop.Notifications')
            object.connect_to_signal("ActionInvoked", self.click_handler, dbus_interface="org.freedesktop.Notifications")
            object.connect_to_signal("NotificationClosed", self.close_handler, dbus_interface="org.freedesktop.Notifications")

        except dbus.DBusException:
            traceback.print_exc()

    def click_handler(self, id, button):
        if id == self.notifyid:
            if button == "reject":
                self.emit(SIGNAL("rejectServer"), ())
            elif button == "accept":
                self.emit(SIGNAL("acceptServer"), self.hostname)
            else:
                pass

    def close_handler(self ,id):
        #If notification popup is closed
        self.emit(SIGNAL("rejectServer"), ())

    def stopNotifier(self):
        self.iface.CloseNotification(self.notifyid)

    def show(self, icon, header, msg, time=3000, button=[]):
        """ ## If getPos do work than use it
        
        if not pos or pos[0] < 0 or pos[1] < 0:
            hints = {}
        else:
            hints= {"x": pos[0], "y": pos[1]}
        """
        # close previous notification window
        self.hostname = header
        #self.buttonList = ["accept", unicode("Accept"), "reject", unicode("Reject")]
        self.notifyid = self.iface.Notify("sinerji",
                         0,
                         icon,
                         unicode(header),
                         unicode(msg),
                         button,
                         {},
                         time)

#!/usr/bin/python
# -*- coding: utf-8 -*-

import dbus
import dbus.mainloop.qt3
import traceback

from kdecore import i18n
from qt import QObject, PYSIGNAL

class Notifier(QObject):
    def click_handler(self, id, button):
        if id == self.notifyid:
            if button == "default" or button == "ignore":
                pass
            else:
                self.emit(PYSIGNAL("showUpgrades"), ())

    def __init__(self):
        QObject.__init__(self)
        dbus.mainloop.qt3.DBusQtMainLoop(set_as_default=True)
        bus = dbus.SessionBus()
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

        self.notifyid = self.iface.Notify("package-manager",
                         0,
                         "file://%s" % icon,
                         unicode(header),
                         unicode(msg),
                         ["showupdates", unicode(i18n("Show Updates")), "ignore", unicode(i18n("Ignore"))],
                         hints,
                         0)

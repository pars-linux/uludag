#!/usr/bin/python
# -*- coding: utf-8 -*-

#! /usr/bin/python
import sys
import dbus

class KNotification:
    def Notify(self, filename, fromhost, m):
        kn = dbus.SessionBus().get_object("org.kde.knotify", "/Notify")
        i = kn.event("warning", "kde", [], m, [0,0,0,0], [], 0,
        dbus_interface="org.kde.KNotify")

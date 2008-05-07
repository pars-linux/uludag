#!/usr/bin/python
# -*- coding: utf-8 -*-

import dbus
import os

def addRepo(name, uri):
    bus = dbus.SystemBus()
    obj = bus.get_object("tr.org.pardus.comar", "/package/pisi")
    obj.addRepository(name, uri, dbus_interface="tr.org.pardus.comar.System.Manager")

def auth():
    bus = dbus.SessionBus()
    obj = bus.get_object("org.freedesktop.PolicyKit.AuthenticationAgent", "/")

    try:
        auths = obj.obtainAuthorization("tr.org.pardus.comar.addrepository", 0, os.getpid(), dbus_interface="org.freedesktop.PolicyKit.AuthenticationAgent")
    except Exception, e:
        print e


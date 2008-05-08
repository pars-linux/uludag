#!/usr/bin/python
# -*- coding: utf-8 -*-

import dbus
import os

def addRepo(name, uri):
    bus = dbus.SystemBus()
    obj = bus.get_object("tr.org.pardus.comar", "/package/pisi")
    obj.addRepository(name, uri, dbus_interface="tr.org.pardus.comar.System.Manager")

def removeRepo(name):
    bus = dbus.SystemBus()
    obj = bus.get_object("tr.org.pardus.comar", "/package/pisi")
    obj.removeRepository(name, dbus_interface="tr.org.pardus.comar.System.Manager")

def auth(action):
    bus = dbus.SessionBus()
    obj = bus.get_object("org.freedesktop.PolicyKit.AuthenticationAgent", "/")

    try:
        auths = obj.ObtainAuthorization("tr.org.pardus.comar.system.manager." + action, 0, os.getpid(), dbus_interface="org.freedesktop.PolicyKit.AuthenticationAgent")
        return auths
    except Exception, e:
        print e
        return False


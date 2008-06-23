#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2008, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

import dbus
import os

class CallHandler:
    def __init__(self, model, method, action, sysBus=None, sesBus=None):
        self.dest = "tr.org.pardus.comar"
        self.path = "/package/pisi"
        self.iface = "%s.%s" % (self.dest, model)
        self.sysBus = sysBus
        self.sesBus = sesBus
        self.method = method
        self.action = action
        self.args = None
        self.handleDone = []
        self.handleCancel = []
        self.handleError = []
        self.handleAuthError = []
        self.handleDBusError = []
        if not self.sysBus:
            self.sysBus = dbus.SystemBus()
        if not self.sesBus:
            self.sesBus = dbus.SessionBus()

    def registerDone(self, func):
        self.handleDone.append(func)

    def registerCancel(self, func):
        self.handleCancel.append(func)

    def registerError(self, func):
        self.handleError.append(func)

    def registerAuthError(self, func):
        self.handleAuthError.append(func)

    def registerDBusError(self, func):
        self.handleDBusError.append(func)

    def call(self, *args):
        self.args = args
        self.__call()

    def __call(self):
        iface = self.__getIface()
        method = getattr(iface, self.method)
        method(reply_handler=self.__handleReply, error_handler=self.__handleError, timeout=2**16-1, *self.args)

    def __getIface(self):
        """ return dbus.Interface object """
        try:
            # proxy object
            proxy = self.sysBus.get_object(self.dest, self.path, introspect=False)
            return dbus.Interface(proxy, dbus_interface=self.iface)
        except dbus.DBusException, e:
            for func in self.handleDBusError:
                func(e)

    def __handleReply(self, *args):
        for func in self.handleDone:
            func(*args)

    def __handleError(self, exception):
        name = exception._dbus_error_name
        try:
            if(name.count("DBus.Error.NoReply") != 0):
                return

            name = name.split(self.dest)[1]
            if name.startswith(".policy.auth"):
                self.__obtainAuth()
            else:
                for func in self.handleError:
                    func(exception)
        except:
            # name is like org.freedesktop.DBus.Error ..
            for func in self.handleError:
                func(exception)

    def __getAuthIface(self):
        """ Return authentication interface from policykit """
        try:
            proxy = self.sesBus.get_object("org.freedesktop.PolicyKit.AuthenticationAgent", "/")
            return dbus.Interface(proxy, "org.freedesktop.PolicyKit.AuthenticationAgent")
        except dbus.DBusException, e:
            print "exception in __getAuthIface"
            for func in self.handleDBusError:
                func(e)

    def __obtainAuth(self):
        iface = self.__getAuthIface()
        if iface.ObtainAuthorization(self.action, 0, os.getpid()):
            self.__call()
        else:
            for func in self.handleCancel:
                func()

    def __handleAuthReply(self, granted):
        if granted:
            self.__call()
        else:
            for func in self.handleCancel:
                func()

    def __handleAuthError(self, exception):
        for func in self.handleAuthError:
            func(exception)

#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

import dbus
import os

class CallHandler:
    """Asynchronous call handler.

    Usage:
      ch = CallHandler("baselayout", "User.Manager", "addUser", "polkit.action" windowID, SystemBus, SessionBus)

      # Exec func1() on success:
      # (Message reply will be passed to function)
      ch.registerDone(func1)

      # Exec func2() if user cancels authentication:
      # (No arguments will be passed to function)
      ch.registerCancel(func2)

      # Exec func3() if method return error:
      # (Exception is passed to function)
      ch.registerError(func3)

      # Exec func4() if PolicyKit returns error:
      # (Exception is passed to function)
      ch.registerError(func4)

      # Exec func5() if DBus connection error occures:
      # (Exception is passed to function)
      ch.registerError(func5)

      # Run
      ch.call(arg1, arg2, ...)
    """

    def __init__(self, package, model, method, action, windowID, busSys=None, busSes=None):
        self.dest = "tr.org.pardus.comar"
        self.path = "/package/%s" % package
        self.iface = "%s.%s" % (self.dest, model)
        self.busSys = busSys
        self.busSes = busSes
        self.window = windowID
        self.method = method
        self.action = action
        self.args = None
        self.handleDone = []
        self.handleCancel = []
        self.handleError = []
        self.handleAuthError = []
        self.handleDBusError = []
        if not self.busSys:
            self.busSys = dbus.SystemBus()
        if not self.busSes:
            self.busSes = dbus.SessionBus()
    
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
        try:
            obj = self.busSys.get_object(self.dest, self.path, introspect=False)
            return dbus.Interface(obj, dbus_interface=self.iface)
        except dbus.DBusException, e:
            for func in self.handleDBusError:
                func(e)
    
    def __handleReply(self, *args):
        for func in self.handleDone:
            func(*args)
    
    def __handleError(self, exception):
        name = exception._dbus_error_name
        name = name.split(self.dest)[1]
        if name.startswith(".policy.auth") or "Comar.PolicyKit" in name:
            self.__obtainAuth()
        else:
            for func in self.handleError:
                func(exception)
    
    def __getAuthIface(self):
        try:
            obj = self.busSes.get_object("org.freedesktop.PolicyKit.AuthenticationAgent", "/")
            return dbus.Interface(obj, "org.freedesktop.PolicyKit.AuthenticationAgent")
        except dbus.DBusException, e:
            for func in self.handleDBusError:
                func(e)
    
    def __obtainAuth(self):
        iface = self.__getAuthIface()
        if iface.ObtainAuthorization(self.action, self.window, os.getpid(), timeout=2**16-1):
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

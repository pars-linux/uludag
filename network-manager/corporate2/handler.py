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

      # Exec func1([arg1, arg2, ...], method_reply) on success:
      ch.registerDone(func1, [arg1, arg2, ...])

      # Exec func2([arg1, arg2, ...]) if user cancels authentication:
      ch.registerCancel(func2, {arg1, arg2 ...])

      # Exec func3([arg1, arg2, ...], exception) if method return error:
      ch.registerError(func3, [arg1, arg2, ...])

      # Exec func4([arg1, arg2, ...], exception) if PolicyKit returns error:
      ch.registerError(func4, [arg1, arg2, ...])

      # Exec func5([arg1, arg2, ...], exception) if DBus connection error occures:
      ch.registerError(func5, [arg1, arg2, ...])

      # Run
      ch.call(method_arg1, method_arg2, ...)
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
        self.ignore_reply = False
        self.handleDone = {}
        self.handleCancel = {}
        self.handleError = {}
        self.handleAuthError = {}
        self.handleDBusError = {}
        if not self.busSys:
            self.busSys = dbus.SystemBus()
        if not self.busSes:
            self.busSes = dbus.SessionBus()
    
    def registerDone(self, func, *args):
        self.handleDone[func] = args
    
    def registerCancel(self, func, *args):
        self.handleCancel[func] = args
    
    def registerError(self, func, *args):
        self.handleError[func] = args
    
    def registerAuthError(self, func, *args):
        self.handleAuthError[func] = args
    
    def registerDBusError(self, func, *args):
        self.handleDBusError[func] = args
    
    def callNoReply(self, *args):
        self.args = args
        self.ignore_reply = True
        self.__call()
    
    def call(self, *args):
        self.args = args
        self.__call()
    
    def __call(self):
        iface = self.__getIface()
        method = getattr(iface, self.method)
        if self.ignore_reply:
            method(ignore_reply=self.ignore_reply, *self.args)
        else:
            method(reply_handler=self.__handleReply, error_handler=self.__handleError, timeout=2**16-1, *self.args)
    
    def __getIface(self):
        try:
            obj = self.busSys.get_object(self.dest, self.path, introspect=False)
            return dbus.Interface(obj, dbus_interface=self.iface)
        except dbus.DBusException, e:
            for func, args in self.handleDBusError.iteritems():
                args = list(args)
                args.append(e)
                func(*args)
    
    def __handleReply(self, *args):
        for func, _args in self.handleDone.iteritems():
            args = list(args)
            _args = list(_args)
            _args.extend(args)
            func(*_args)
    
    def __handleError(self, exception):
        name = exception._dbus_error_name
        if name.startswith(self.dest):
            name = name.split(self.dest)[1]
        if name.startswith(".policy.auth") or name.startswith(".Comar.PolicyKit"):
            self.__obtainAuth()
        else:
            for func, args in self.handleError.iteritems():
                args = list(args)
                args.append(exception)
                func(*args)
    
    def __getAuthIface(self):
        try:
            obj = self.busSes.get_object("org.freedesktop.PolicyKit.AuthenticationAgent", "/")
            return dbus.Interface(obj, "org.freedesktop.PolicyKit.AuthenticationAgent")
        except dbus.DBusException, e:
            for func, args in self.handleDBusError.iteritems():
                args = list(args)
                args.append(e)
                func(*args)
    
    def __obtainAuth(self):
        iface = self.__getAuthIface()
        iface.ObtainAuthorization(self.action, self.window, os.getpid(), reply_handler=self.__handleAuthReply, error_handler=self.__handleAuthError, timeout=2**16-1)
    
    def __handleAuthReply(self, granted):
        if granted:
            self.__call()
        else:
            for func, args in self.handleCancel.iteritems():
                func(*args)
    
    def __handleAuthError(self, exception):
        for func, args in self.handleAuthError.iteritems():
            args = list(args)
            args.append(exception)
            func(*args)

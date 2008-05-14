#!/usr/bin/python
# -*- coding: utf-8 -*-

from qt import QMutex, SIGNAL
from kdeui import KMessageBox
from kdecore import i18n

# DBus
import dbus
import dbus.mainloop.qt3

from handler import CallHandler

class ComarIface:
    def __init__(self, handler=None, errHandler=None):
        self.errHandler = errHandler
        self.handler = handler
        # package-manager sync
        self.com_lock = QMutex()
        self.setupBusses()
        self.setupSignals()

    def setupBusses(self):
        try:
            self.sysBus = dbus.SystemBus()
            self.sesBus = dbus.SessionBus()
        except dbus.DBusException:
            print "Cant connect to dbus"
            KMessageBox.error(None, i18n("Unable to connect to DBus."), i18n("DBus Error"))
            return False
        return True

    def setupSignals(self):
        self.sysBus.add_signal_receiver(self.handleSignals, dbus_interface="tr.org.pardus.comar.System.Manager", member_keyword="signal", path_keyword="path")

    def handleSignals(self, *args, **kwargs):
        signal = kwargs["signal"]
        if self.handler:
            self.handler(signal, args)

    def busError(self, exception):
        KMessageBox.error(None, str(exception), i18n("D-Bus Error"))
        self.setupBusses()
        self.errHandler()

    def comarAuthError(self, exception):
        KMessageBox.error(None, str(exception), i18n("COMAR Auth Error"))
        self.errHandler()

    def comarError(self, exception):
        if not "urlopen error" in exception.message:
            KMessageBox.error(None, str(exception), i18n("COMAR Error"))
        self.errHandler()

    def cancelError(self):
        message = i18n("You are not authorized for this operation.")
        self.errHandler()
        KMessageBox.sorry(None, message, i18n("Error"))

    def callMethod(self, method, action, handler, handleErrors, *args):
        print "Method: %s      Action: %s" % (method, action)
        ch = CallHandler("System.Manager", method, action, self.sysBus, self.sesBus)

        if handleErrors:
            ch.registerError(self.comarError)
            ch.registerAuthError(self.comarAuthError)
            ch.registerDBusError(self.busError)
            ch.registerCancel(self.cancelError)
        if handler:
            ch.registerDone(handler)

        ch.call(*args)

    def takeSnapshot(self):
        self.com_lock.lock()
        self.callMethod("takeSnapshot", "tr.org.pardus.comar.system.manager.takesnapshot", self.handler, True)

    def takeBack(self, operation):
        self.com_lock.lock()
        self.callMethod("takeBack", "tr.org.pardus.comar.system.manager.takeback", None, True, operation)

    def cancel(self):
        obj = self.sysBus.get_object("tr.org.pardus.comar", "/", introspect=False)
        obj.cancel(dbus_interface="tr.org.pardus.comar")


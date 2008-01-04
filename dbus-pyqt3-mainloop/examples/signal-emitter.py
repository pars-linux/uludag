#!/usr/bin/env python

import dbus
import dbus.service
import dbus.mainloop.qt3

from qt import *

import sys

class TestObject(dbus.service.Object):
    def __init__(self, conn, object_path='/com/example/TestService/object'):
        dbus.service.Object.__init__(self, conn, object_path)

    @dbus.service.signal('com.example.TestService')
    def HelloSignal(self, message):
        # The signal is emitted when this method exits
        # You can have code here if you wish
        pass

    @dbus.service.method('com.example.TestService')
    def emitHelloSignal(self):
        #you emit signals by calling the signal's skeleton method
        self.HelloSignal('Hello')
        return 'Signal emitted'

    @dbus.service.method("com.example.TestService", in_signature='', out_signature='')
    def Exit(self):
        loop.quit()

if __name__ == '__main__':
    # we should create QApplication before DBus mainloop
    loop = QApplication(sys.argv)

    dbus.mainloop.qt3.DBusQtMainLoop(set_as_default=True)

    session_bus = dbus.SessionBus()
    name = dbus.service.BusName('com.example.TestService', session_bus)
    object = TestObject(session_bus)

    print "Running example signal emitter service."
    sys.exit(loop.exec_loop())

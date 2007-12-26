#!/usr/bin/env python

import sys
import traceback

import dbus
import dbus.mainloop.qt3

from qt import *

def emit_signal():
   print "Emitting signal..."

   #call the emitHelloSignal method 
   object.emitHelloSignal(dbus_interface="com.example.TestService")

   # exit after waiting a short time for the signal
   print "Emitter called. Quiting..."

   global app
   QTimer.singleShot(1000, app.quit)

   return False

def hello_signal_handler(hello_string):
    print ("Received signal (by connecting using remote object) and it says: "
           + hello_string)

def catchall_hello_signals_handler(hello_string):
    print "Received a hello signal and it says " + hello_string

if __name__ == '__main__':
    dbus.mainloop.qt3.DBusQtMainLoop(set_as_default=True)

    bus = dbus.SessionBus()
    try:
        object  = bus.get_object("com.example.TestService","/com/example/TestService/object")
        object.connect_to_signal("HelloSignal", hello_signal_handler, dbus_interface="com.example.TestService", arg0="Hello")

    except dbus.DBusException:
        traceback.print_exc()
        sys.exit(1)

    bus.add_signal_receiver(catchall_hello_signals_handler, dbus_interface = "com.example.TestService", signal_name = "HelloSignal")

    print "After 2 seconds, emitter will be called..."
    QTimer.singleShot(2000, emit_signal)

    global app
    app = QApplication(sys.argv) 

    print "Now, entering Qt main loop..."
    sys.exit(app.exec_loop()) 

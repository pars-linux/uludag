#!/usr/bin/env python

import sys
import traceback

import dbus
import dbus.mainloop.qt3

from qt import *

def click_handler(id, title):
    print "Clicked: %s" % title

    print "Quiting successfully."
    global loop
    loop.quit()

def emit_signal():
    dbus.mainloop.qt3.DBusQtMainLoop(set_as_default=True)

    bus = dbus.SessionBus()
    try:
        object  = bus.get_object("org.freedesktop.Notifications","/org/freedesktop/Notifications")
        iface = dbus.Interface(object, dbus_interface='org.freedesktop.Notifications')

        #object.connect_to_signal("NotificationClosed", click_handler, dbus_interface="org.freedesktop.Notifications")
        object.connect_to_signal("ActionInvoked", click_handler, dbus_interface="org.freedesktop.Notifications")

        iface.Notify("package-manager", 123, "aaa", "Summary", "Body", ["Dugme", "Dugme","Dugme2","Dugme2" ], [], 10000)
        print "Notify() invoked..."

        global loop
        QTimer.singleShot(5000, loop.quit)

    except dbus.DBusException:
        traceback.print_exc()
        print usage
        sys.exit(1)

if __name__ == '__main__':


    global loop
    loop = QApplication(sys.argv)

    QTimer.singleShot(0, emit_signal)

    print "Entering mainloop..."
    sys.exit(loop.exec_loop()) 


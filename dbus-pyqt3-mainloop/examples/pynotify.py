#!/usr/bin/env python

import sys
import traceback

import dbus
import dbus.mainloop.qt3

from qt import *

def click_handler(id, title):
    global notifyid

    # if the notification is the one that we created
    if notifyid == id:
        print "Clicked: %d, %s" % (id, title)

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

        global notifyid
        notifyid = iface.Notify("pynotify", # application name
                     0,               # replaces id
                     "", #icon path like file:///usr/share/icons/Tulliana-2.0/64x64/actions/ok.png",
                     "Summary",         # header of notification
                     "Body",            # message of notification
                     ["ButtonDescription1", "Button1","ButtonDescription2","Button2" ], # list of buttons as pairs of identifier and title
                     {"category": "im", "urgency": dbus.Byte(1), "x": 500, "y": 500},  # hints like category, urgency, coordinate of notification (x,y)
                     10000)             # timeout in msec

        print "Notify() invoked...\n Notifyid: %s" % notifyid

        global loop
        QTimer.singleShot(5000, loop.quit)

    except dbus.DBusException:
        traceback.print_exc()
        loop.quit()
        sys.exit(1)

if __name__ == '__main__':
    global loop
    loop = QApplication(sys.argv)

    QTimer.singleShot(0, emit_signal)

    print "Entering mainloop..."
    sys.exit(loop.exec_loop()) 


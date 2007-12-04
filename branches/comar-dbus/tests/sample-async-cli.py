#!/usr/bin/env python

import time

import dbus.bus
import dbus.mainloop.glib
import gobject

def handler(a):
    print a

def main():
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    object = bus.get_object("tr.org.pardus.comar", "/package/apache", introspect=False)
    iface = dbus.Interface(object, "System.Package")

    kwargs = {"reply_handler": handler, "error_handler": handler}
    def test(*args):
        iface.postInstall(*args, **kwargs)
        time.sleep(0.5) # don't flood

    test(1)

    loop = gobject.MainLoop()
    loop.run()

if __name__ == '__main__':
    main()

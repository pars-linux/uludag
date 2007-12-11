#!/usr/bin/env python

import dbus.bus

def main():
    bus = dbus.SystemBus()
    object = bus.get_object("tr.org.pardus.comar", "/package/mysql", introspect=False)
    iface = dbus.Interface(object, "tr.org.pardus.comar.System.Package")

    try:
        print iface.postInstall("1.0.0", "1", "2.0.0", "2")
    except Exception, e:
        print e


if __name__ == '__main__':
    main()

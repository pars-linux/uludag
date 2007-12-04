#!/usr/bin/env python

import dbus.bus

def main():
    bus = dbus.SystemBus()
    object = bus.get_object("tr.org.pardus.comar", "/package/mysql", introspect=False)
    iface = dbus.Interface(object, "System.Package")

    def test(*args):
        try:
            print iface.postInstall(*args)
        except Exception, e:
            print e

    test(1)
    test(1, [1, 2, 3])


if __name__ == '__main__':
    main()

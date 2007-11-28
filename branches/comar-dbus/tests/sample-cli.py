#!/usr/bin/env python

import dbus.bus

def main():
    bus = dbus.SystemBus()
    object = bus.get_object("tr.org.pardus.comar", "/package/mysql", introspect=False)

    args = {"a": 1, "b": 2.0, "c": "3"}
    print object.postInstall(tuple(args.items()), dbus_interface="System.Package")


if __name__ == '__main__':
    main()

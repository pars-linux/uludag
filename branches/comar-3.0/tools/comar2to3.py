#!/usr/bin/python
# -*- coding: utf-8 -*-

import dbus
import glob
import os
import time

COMAR_DB = "/var/db/comar/code"
COMAR_ADDRESS = "tr.org.pardus.comar.updated"
COMAR_IFACE = "tr.org.pardus.comar"
COMAR_TIMEOUT = 10

def main():
    if os.getuid() != 0:
        print "Must be run as root."
        return -1

    bus = dbus.SystemBus()
    obj = None

    os.system("/usr/sbin/comar3 -b %s &" % COMAR_ADDRESS)

    timeout = COMAR_TIMEOUT
    while timeout > 0:
        try:
            obj = bus.get_object(COMAR_ADDRESS, "/", introspect=False)
            break
        except dbus.exceptions.DBusException:
            pass
        time.sleep(0.2)
        timeout -= 0.2

    if not obj:
        print "Unable to start new COMAR service."
        return -2

    for filename in os.listdir(COMAR_DB):
        if filename.endswith(".py"):
            _group, _class, _app = filename.split("_", 2)
            _model = "%s.%s" % (_group, _class)
            _app = _app.rsplit(".py", 1)[0]
            obj.register(_app, _model, os.path.join(COMAR_DB, filename), dbus_interface=COMAR_IFACE)
            print filename

    return 0

if __name__ == "__main__":
    main()

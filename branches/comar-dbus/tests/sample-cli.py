#!/usr/bin/env python

import dbus.bus

def main():
    bus = dbus.bus.BusConnection(address_or_type=1)

    def test(val, sig):
        try:
            retr = bus.call_blocking('tr.org.pardus.comar', '/package/apache', 'System.Package', 'postInstall', sig, (val,))
            print "%s (%s)" % (retr, type(retr))
        except Exception, e:
            print "Error:", e

    test(123, "i")
    test("abc", "s")
    test(1.2, "d")
    test(1L, "x")
    test(["a", "b", "c"], "as")
    test([1, 2, 3], "ai")
    test([], "ai")
    test([1.2, 1.1, 1.3], "ad")
    test(("a", 1.2, (1, "2", 3.0, [1, 2, 3], {"a": 1, "b": 2})), "v")
    test({"a": 1, "b": 2}, "a{si}")
    test({"a": "A", "b": "B"}, "a{ss}")

if __name__ == '__main__':
    main()

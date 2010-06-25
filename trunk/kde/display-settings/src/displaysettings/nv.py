#!/usr/bin/python
# -*- coding: utf-8 -*-

import xcb
from xcb.xproto import *
import xcb.nvctrl

from displaysettings.device import Output

try:
    conn = xcb.connect()
    conn.nv = conn(xcb.nvctrl.key)
except xcb.ExtensionException:
    conn.nv = None

class Interface:
    def __init__(self, window=None):
        self.ready = conn.nv is not None

    def query(self):
        # dpy, screen, display_mask, attribute
        cookie = conn.nv.QueryAttribute(0, 0, 0, xcb.nvctrl.Attributes.PROBE_DISPLAYS)
        reply = cookie.reply()

        display_mask = reply.value
        mask = 1

        self.__outputs = []
        n = 0

        while mask < (1 << 24):
            if display_mask & mask:
                if mask & 0xff:
                    dtype = "CRT"
                elif mask & 0xff00:
                    dtype = "TV"
                else:
                    dtype = "DFP"

                name = "%s-%d" % (dtype, n)
                output = Output(name)
                self.__outputs.append(output)

                output.connection = Output.Connected

            mask <<= 1
            n = (n + 1) % 8

    def queryCurrent(self):
        pass

    def getOutputs(self):
        self.queryCurrent()
        return self.__outputs

    def getGeometry(self, output):
        return (0, 0, 0, 0)

if __name__ == "__main__":
    iface = Interface()

    if iface.ready:
        print "RandR extension is available"

        #iface.query()
        print iface.getOutputs()

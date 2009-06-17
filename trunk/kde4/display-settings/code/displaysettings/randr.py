#!/usr/bin/python
# -*- coding: utf-8 -*-

import xcb
from xcb.xproto import *
import xcb.randr

from displaysettings.device import Output

try:
    conn = xcb.connect()
    conn.randr = conn(xcb.randr.key)
except xcb.ExtensionException:
    conn.randr = None

class Interface:
    def __init__(self, window=None):
        self.ready = conn.randr is not None

        if window is None:
            self.window = conn.get_setup().roots[0].root
        else:
            self.window = window

    def query(self):
        cookie = conn.randr.GetScreenResources(self.window)
        self.resources = cookie.reply()

    def queryCurrent(self):
        cookie = conn.randr.GetScreenResourcesCurrent(self.window)
        self.resources = cookie.reply()

    def getOutputs(self):
        outputs = []

        self.queryCurrent()

        for rroutput in self.resources.outputs:
            cookie = conn.randr.GetOutputInfo(rroutput, self.resources.config_timestamp)
            info = cookie.reply()

            name = "".join(map(chr, info.name))
            output = Output(name)
            outputs.append(output)

            if info.connection == xcb.randr.Connection.Connected:
                output.connection = Output.Connected
            elif info.connection == xcb.randr.Connection.Disconnected:
                output.connection = Output.Disconnected
            else:
                output.connection = Output.Unknown

        return outputs

if __name__ == "__main__":
    iface = Interface()

    if iface.ready:
        print "RandR extension is available"

        #iface.query()
        print iface.getOutputs()

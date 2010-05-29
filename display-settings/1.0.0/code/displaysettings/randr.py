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
            output.randrInfo = info

            try:
                cookie = conn.randr.GetCrtcInfo(info.crtc, self.resources.config_timestamp)
                output.crtcInfo = cookie.reply()
            except xcb.randr.BadCrtc:
                output.crtcInfo = None

            if info.connection == xcb.randr.Connection.Connected:
                output.connection = Output.Connected
            elif info.connection == xcb.randr.Connection.Disconnected:
                output.connection = Output.Disconnected
            else:
                output.connection = Output.Unknown

            outputs.append(output)

        return outputs

    def getGeometry(self, output):
        i = output.crtcInfo
        return (i.width, i.height, i.x, i.y) if i else (0, 0, 0, 0)

if __name__ == "__main__":
    iface = Interface()

    if iface.ready:
        print "RandR extension is available"

        #iface.query()
        print iface.getOutputs()

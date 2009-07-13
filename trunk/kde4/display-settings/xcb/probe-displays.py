#!/usr/bin/python
# -*- coding: utf-8 -*-

import xcb
from xcb.xproto import *
import xcb.nvctrl

conn = xcb.connect()
conn.nv = conn(xcb.nvctrl.key)

cookie = conn.nv.QueryExtension()
reply = cookie.reply()
print reply.major_version, reply.minor_version

# 0 -> screen number
cookie = conn.nv.IsNv(0)
reply = cookie.reply()
print reply.isnv

# dpy, screen, display_mask, attribute
cookie = conn.nv.QueryAttribute(0, 0, 0, xcb.nvctrl.Attributes.PROBE_DISPLAYS)
reply = cookie.reply()
print reply.flags, "%08x" % reply.value

display_mask = reply.value
mask = 1

probed_displays = []
n = 0

while mask < (1 << 24):
    if display_mask & mask:
        if mask & 0xff:
            dtype = "CRT"
        elif mask & 0xff00:
            dtype = "TV"
        else:
            dtype = "DFP"

        probed_displays.append("%s-%d" % (dtype, n))

    mask <<= 1
    n = (n + 1) % 8

for d in probed_displays:
    print d

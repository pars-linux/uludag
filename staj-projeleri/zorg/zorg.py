#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2007 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

import sys
from optparse import OptionParser

import comar
from zorg import versionString
from zorg.utils import parseMode

zorg_info = " Xorg AutoConfiguration tool"

def collect(c):
    reply = c.read_cmd()
    if reply.command == "start":
        replies = []
        while True:
            reply = c.read_cmd()
            if reply.command == "end":
                return replies
            replies.append(reply)
    else:
        return [reply]

class OUT:
    def __init__(self, colorout):
        if colorout:
            self.NORMAL = '\x1b[37;0m'
            self.BOLD = '\x1b[37;01m'
            self.MARK = '\x1b[36;01m'
            self.WARN = '\x1b[35m'
            self.WARNMSG = '\x1b[35;01m'
            self.ERROR = '\x1b[31m'
            self.ERRORMSG = '\x1b[31;01m'
        else:
            self.NORMAL = ''
            self.BOLD = ''
            self.MARK = ''
            self.WARN = ''
            self.WARNMSG = ''
            self.ERROR = ''
            self.ERRORMSG = ''

        self.type_sect = "%s-> " % self.MARK
        self.type_info = "%s   " % self.NORMAL
        self.type_warn = "%sWW " % self.WARN
        self.type_error  = "%sEE " % self.ERROR

    def _write(self, type, msg):
        print "%s %s%s" % (type, msg, self.NORMAL)

    def sect(self, msg):
        self._write(self.type_sect, "%s%s" % (self.BOLD, msg))

    def info(self, msg):
        self._write(self.type_info, msg)

    def warn(self, msg):
        self._write(self.type_warn, "%s%s" % (self.WARNMSG, msg))

    def error(self, msg):
        self._write(self.type_error, "%s%s" % (self.ERRORMSG, msg))
        sys.exit(1)

def safe():
    link.Xorg.Display.safeConfigure()

def probe(opts):
    if opts.mode:
        res, depth = parseMode(opts.mode)
        if not res:
            out.error("Mode is not supported or not valid: %s" % opts.mode)
            return

    out.info("Probing devices for a single head configuration...")
    link.Xorg.Display.autoConfigure()
    reply = link.read_cmd()
    if reply.command == "result":
        out.info("Automatic configuration done.")
    else:
        out.error(reply.data)

    if opts.mode:
        setMode(opts)

def setMode(opts):
    link.Xorg.Display.screenInfo(screenNumber="0")
    reply = link.read_cmd()
    if reply.command == "result":
        scrInfo = dict(x.split("=", 1) for x in reply.data.strip().splitlines())
    else:
        out.error(reply.data)

    link.Xorg.Display.monitorInfo(monitorId=scrInfo["monitor"])
    reply = link.read_cmd()
    if reply.command == "result":
        for line in reply.data.splitlines():
            if line.startswith("resolutions="):
                resolutions = line.split("=", 1)[1].split(",")
                break;
    else:
        out.error(reply.data)

    res = opts.mode.split("-")[0]
    if res in resolutions:
        out.info("Setting mode to %s" % opts.mode)
    elif opts.force:
        out.warn("Forcing unsupported mode: %s" % opts.mode)
    else:
        out.error("Mode is not supported: %s" % opts.mode)

    link.Xorg.Display.setScreen(screenNumber="0", cardId=scrInfo["card"],
                                monitorId=scrInfo["monitor"], mode=opts.mode)

    reply = link.read_cmd()
    if reply.command == "fail":
        out.error(reply.data)

def setDriver(driver):
    link.Xorg.Display.screenInfo(screenNumber="0")
    reply = link.read_cmd()
    if reply.command == "result":
        scrInfo = dict(x.split("=", 1) for x in reply.data.strip().splitlines())
    else:
        out.error(reply.data)

    out.info("Setting card driver to %s" % driver)
    opts = "driver=%s" % driver
    link.Xorg.Display.setCardOptions(cardId=scrInfo["card"], options=opts)
    reply = link.read_cmd()
    if reply.command == "fail":
        out.error(reply.data)

def info():
    link.Xorg.Display.listCards()
    reply = collect(link)[0]
    if not reply:
        out.error("Could not retrieve card list.")
        return

    cards = {}
    monitors = {}

    for card in reply.data.splitlines():
        cardId, name = card.split(" ", 1)
        link.Xorg.Display.cardInfo(cardId=cardId)
        reply = collect(link)[0]
        info = dict(x.split("=", 1) for x in reply.data.splitlines())

        cards[cardId] = info["boardName"]

        if info["busId"]:
            out.sect("Configured a video card on %s bus %s, device %s, function %s"
                    % tuple(info["busId"].split(":")))
        else:
            out.sect("Configured a failsafe video driver")
        out.info("  PCI ID = %s:%s" % (info["vendorId"], info["deviceId"]))
        out.info("  Vendor = %s" % info["vendorName"])
        out.info("  Device = %s" % info["boardName"])
        out.info("  Driver = %s" % info["driver"])
        out.info("")
        out.info("  Monitors connected to this device:")

        monitorIds = info["monitors"].split(",")
        if not monitorIds:
            out.error("    Could not find any configured monitors for this device")
            continue

        for mon in monitorIds:
            link.Xorg.Display.monitorInfo(monitorId=mon)
            reply = collect(link)[0]
            if not reply:
                out.error("Could not get monitor info")
                continue

            info = dict(x.split("=", 1) for x in reply.data.splitlines())
            monitors[mon] = info["modelName"]
            out.info("    Vendor                = %s" % info["vendorName"])
            out.info("    Model                 = %s" % info["modelName"])
            out.info("    Supported resolutions = %s" % info["resolutions"])
            out.info("")

    for n in "0", "1":
        out.sect("Screen %s properties:" % n)
        link.Xorg.Display.screenInfo(screenNumber=n)
        reply = link.read_cmd()
        if reply.command != "result":
            out.error(reply.data)
            continue

        if not reply.data:
            out.warn("Not configured.")
            continue

        info = dict(x.split("=", 1) for x in reply.data.splitlines())

        out.info("  Video card  = %s" % cards[info["card"]])
        out.info("  Monitor     = %s" % monitors[info["monitor"]])
        out.info("  Resolution  = %s" % info["resolution"])
        out.info("  Color depth = %s" % info["depth"])
        out.info("")


if __name__ == "__main__":
    # running from command line
    parser = OptionParser(description = "%s version %s" % (zorg_info, versionString()))
    parser.add_option("-n", "--no-color", action="store_false", dest="colorout",
                      default=True, help="do not print colorized output")
    parser.add_option("-s", "--safe", action="store_true", dest="safe",
                      default=False, help="setup VESA 800x600 config without probing hardware")
    parser.add_option("-p", "--probe", action="store_true", dest="probe",
                      default=False, help="force probing all devices, even if xorg.conf exists")
    parser.add_option("-m", "--mode", action="store", type="string", dest="mode",
                      default=None, help="use MODE given in form <width>x<height>[-<depth>] if supported")
    parser.add_option("-f", "--force", action="store_true", dest="force",
                      default=False, help="force using the specified mode (use with caution)")
    parser.add_option("-d", "--driver", action="store", type="string", dest="driver",
                      default=None, help="set video card driver to DRIVER")
    parser.add_option("-i", "--info", action="store_true", dest="info",
                      default=False, help="print video, monitor and input info, no probing is done")
    parser.add_option("--intelfix", action="store_true", dest="intelfix",
                      default=False, help="run Intel BIOS bug workaround")
    parser.add_option("--intellist", action="store_true", dest="intellist",
                      default=False, help="list available BIOS modes for Intel cards")

    opts, args = parser.parse_args()
    out = OUT(opts.colorout)
    link = comar.Link()

    if opts.safe:
        safe()
    elif opts.probe:
        probe(opts)
    elif opts.mode or opts.driver:
        if opts.mode:
            setMode(opts)
        if opts.driver:
            setDriver(opts.driver)
    elif opts.info:
        info()
    elif opts.intelfix:
        out.error("Not implemented yet.")
    elif opts.intellist:
        out.error("Not implemented yet.")
    else:
        parser.print_help()

